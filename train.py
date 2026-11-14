"""Reproducible comparison for the online shopping session proof of concept."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
SEED = 42
# PageValues is a historical revenue-derived analytics metric. Excluding it makes
# this proof of concept easier to deploy without a target-derived input.
DROP = ["Revenue", "PageValues"]
CATEGORICAL = ["Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    raw = pd.read_csv(ROOT / "online_shoppers_intention.csv")
    duplicates = int(raw.duplicated().sum())
    df = raw.drop_duplicates().reset_index(drop=True)
    y = df["Revenue"].astype(int)
    X = df.drop(columns=DROP)
    numeric = [c for c in X if c not in CATEGORICAL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEED
    )
    prep = ColumnTransformer(
        [
            ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
            ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CATEGORICAL),
        ],
        sparse_threshold=0,
    )
    models = {
        "Always no purchase": DummyClassifier(strategy="prior"),
        "Logistic regression": LogisticRegression(max_iter=2000, class_weight="balanced", random_state=SEED),
        "Random forest": RandomForestClassifier(n_estimators=200, min_samples_leaf=3, class_weight="balanced_subsample", n_jobs=-1, random_state=SEED),
        "Gradient boosting": HistGradientBoostingClassifier(max_iter=160, learning_rate=0.06, max_leaf_nodes=15, l2_regularization=1.0, random_state=SEED),
    }
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    scoring = {"average_precision": "average_precision", "roc_auc": "roc_auc", "f1": "f1", "recall": "recall"}
    results = {}
    pipelines = {}
    for name, estimator in models.items():
        pipe = Pipeline([("preprocess", prep), ("model", estimator)])
        scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=1)
        results[name] = {"cv_" + k: float(np.mean(scores["test_" + k])) for k in scoring}
        pipelines[name] = pipe
        print(f"{name}: CV AP={results[name]['cv_average_precision']:.3f}", flush=True)

    # Tune the strongest non-baseline family on training folds only.
    best_base = max((n for n in models if n != "Always no purchase"), key=lambda n: results[n]["cv_average_precision"])
    grids = {
        "Logistic regression": {"model__C": [0.1, 1, 10]},
        "Random forest": {"model__max_depth": [8, 16, None], "model__min_samples_leaf": [2, 5]},
        "Gradient boosting": {"model__max_leaf_nodes": [7, 15, 31], "model__l2_regularization": [0.1, 1.0]},
    }
    search = GridSearchCV(pipelines[best_base], grids[best_base], scoring="average_precision", cv=cv, n_jobs=1, refit=True)
    search.fit(X_train, y_train)
    results[best_base + " tuned"] = {"cv_average_precision": float(search.best_score_), "best_params": search.best_params_}
    pipelines[best_base + " tuned"] = search.best_estimator_
    print(f"{best_base} tuned: CV AP={search.best_score_:.3f}", flush=True)

    # Compare every model on the same untouched 20% holdout.
    for name, pipe in pipelines.items():
        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]
        label = proba >= 0.5
        top_n = max(1, int(np.ceil(len(proba) * 0.10)))
        top_idx = np.argsort(proba)[-top_n:]
        results[name]["test"] = {
            "average_precision": float(average_precision_score(y_test, proba)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
            "accuracy": float(accuracy_score(y_test, label)),
            "precision": float(precision_score(y_test, label, zero_division=0)),
            "recall": float(recall_score(y_test, label, zero_division=0)),
            "f1": float(f1_score(y_test, label, zero_division=0)),
            "confusion_matrix": confusion_matrix(y_test, label).tolist(),
            "top_decile_purchase_rate": float(y_test.iloc[top_idx].mean()),
            "top_decile_lift": float(y_test.iloc[top_idx].mean() / y_test.mean()),
        }
        print(f"{name}: test AP={results[name]['test']['average_precision']:.3f}, ROC AUC={results[name]['test']['roc_auc']:.3f}", flush=True)

    chosen = max(pipelines, key=lambda n: results[n]["cv_average_precision"])

    # How precise are these scores? Bootstrap the test set so model differences
    # can be read against their uncertainty instead of at face value.
    probabilities = {n: p.predict_proba(X_test)[:, 1] for n, p in pipelines.items()}
    for name, proba in probabilities.items():
        lo, hi = bootstrap_ap_ci(y_test.to_numpy(), proba)
        results[name]["test"]["average_precision_ci95"] = [lo, hi]
    runner_up = max((n for n in pipelines if n not in (chosen, "Always no purchase")),
                    key=lambda n: results[n]["test"]["average_precision"])
    gap = bootstrap_ap_difference(y_test.to_numpy(), probabilities[chosen], probabilities[runner_up])
    print(f"{chosen} vs {runner_up}: AP gap {gap['mean']:+.4f} "
          f"95% CI [{gap['ci95'][0]:+.4f}, {gap['ci95'][1]:+.4f}], "
          f"chosen wins {gap['win_rate']:.1%} of resamples", flush=True)

    # A 0.5 cutoff is arbitrary for a 15% positive rate. Report two defensible ones.
    thresholds = choose_thresholds(y_test.to_numpy(), probabilities[chosen])
    print(f"best-F1 threshold {thresholds['best_f1']['threshold']:.3f} "
          f"-> F1={thresholds['best_f1']['f1']:.3f}, "
          f"capacity threshold {thresholds['review_top_10pct']['threshold']:.3f}", flush=True)

    # What did excluding PageValues actually cost? Quantify rather than assert.
    ablation = page_values_ablation(df, y, SEED)
    print(f"PageValues ablation: without={ablation['without_page_values_ap']:.3f} "
          f"with={ablation['with_page_values_ap']:.3f}", flush=True)

    # Which behaviours move the score? Permutation importance is model-agnostic
    # and measured on the untouched test set.
    importance = feature_importance(pipelines[chosen], X_test, y_test, SEED)
    make_importance_chart(importance, OUT)

    joblib.dump(pipelines[chosen], OUT / "purchase_model.joblib")
    examples = X_test.copy()
    examples["Revenue"] = y_test.values.astype(bool)
    examples.sample(n=30, random_state=SEED).to_csv(OUT / "demo_sessions.csv", index=False)

    # Every held-out session with its score, so the app can rank the whole set
    # instead of only describing what ranking would look like.
    scored = X_test.copy()
    scored["Revenue"] = y_test.values.astype(bool)
    scored["score"] = probabilities[chosen]
    scored.sort_values("score", ascending=False).to_csv(OUT / "scored_sessions.csv", index=False)
    report = {
        "source_rows": int(len(raw)), "exact_duplicates_removed": duplicates,
        "rows_used": int(len(df)), "positive_rate": float(y.mean()),
        "train_rows": int(len(X_train)), "test_rows": int(len(X_test)),
        "chosen_model": chosen, "excluded_feature": "PageValues", "results": results,
        "runner_up": runner_up, "chosen_vs_runner_up": gap,
        "thresholds": thresholds, "page_values_ablation": ablation,
        "feature_importance": importance,
    }
    (OUT / "results.json").write_text(json.dumps(report, indent=2))
    make_eda(raw, OUT)
    make_eda_detail(df, OUT)
    print(f"Saved {chosen} and report to {OUT}")


def bootstrap_ap_ci(y_true: np.ndarray, proba: np.ndarray, n: int = 2000) -> tuple[float, float]:
    """95% percentile interval for average precision, by resampling the test set."""
    rng = np.random.default_rng(SEED)
    scores = []
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        if y_true[idx].sum() == 0:
            continue
        scores.append(average_precision_score(y_true[idx], proba[idx]))
    return float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))


def bootstrap_ap_difference(y_true: np.ndarray, a: np.ndarray, b: np.ndarray, n: int = 2000) -> dict:
    """Paired bootstrap of the AP gap between two models on the same resamples."""
    rng = np.random.default_rng(SEED)
    diffs = []
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        if y_true[idx].sum() == 0:
            continue
        diffs.append(average_precision_score(y_true[idx], a[idx])
                     - average_precision_score(y_true[idx], b[idx]))
    diffs = np.asarray(diffs)
    return {
        "mean": float(diffs.mean()),
        "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "win_rate": float((diffs > 0).mean()),
        "significant": bool(np.percentile(diffs, 2.5) > 0 or np.percentile(diffs, 97.5) < 0),
    }


def choose_thresholds(y_true: np.ndarray, proba: np.ndarray) -> dict:
    """Two defensible operating points: best F1, and 'review the top 10%'."""
    precision, recall, cuts = precision_recall_curve(y_true, proba)
    f1 = np.divide(2 * precision * recall, precision + recall,
                   out=np.zeros_like(precision), where=(precision + recall) > 0)
    best = int(np.argmax(f1[:-1]))
    capacity = float(np.quantile(proba, 0.90))
    flagged = proba >= capacity
    return {
        "note": "0.5 is arbitrary for a 15.6% positive rate; these are chosen on the test set "
                "and would need a validation split before operational use.",
        "best_f1": {"threshold": float(cuts[best]), "precision": float(precision[best]),
                    "recall": float(recall[best]), "f1": float(f1[best])},
        "review_top_10pct": {
            "threshold": capacity,
            "precision": float(y_true[flagged].mean()),
            "recall": float(y_true[flagged].sum() / y_true.sum()),
            "sessions_flagged": int(flagged.sum()),
        },
    }


def page_values_ablation(df: pd.DataFrame, y: pd.Series, seed: int) -> dict:
    """Measure what excluding the revenue-derived PageValues feature costs."""
    out = {}
    for label, drop in [("without_page_values", ["Revenue", "PageValues"]),
                        ("with_page_values", ["Revenue"])]:
        X = df.drop(columns=drop)
        numeric = [c for c in X if c not in CATEGORICAL]
        prep = ColumnTransformer(
            [
                ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
                ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CATEGORICAL),
            ],
            sparse_threshold=0,
        )
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.20, stratify=y, random_state=seed)
        pipe = Pipeline([("preprocess", prep), ("model", RandomForestClassifier(
            n_estimators=200, min_samples_leaf=5, class_weight="balanced_subsample",
            n_jobs=-1, random_state=seed))])
        pipe.fit(X_tr, y_tr)
        proba = pipe.predict_proba(X_te)[:, 1]
        top = max(1, int(np.ceil(len(proba) * 0.10)))
        out[label + "_ap"] = float(average_precision_score(y_te, proba))
        out[label + "_roc_auc"] = float(roc_auc_score(y_te, proba))
        out[label + "_lift"] = float(y_te.iloc[np.argsort(proba)[-top:]].mean() / y_te.mean())
    out["note"] = ("PageValues is derived from revenue. Keeping it roughly doubles measured "
                   "performance, which is why we treat it as leakage rather than a win.")
    return out


def feature_importance(pipe: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, seed: int) -> list:
    """Permutation importance on the held-out set, in average-precision points."""
    r = permutation_importance(pipe, X_test, y_test, scoring="average_precision",
                               n_repeats=10, random_state=seed, n_jobs=-1)
    ranked = sorted(
        ({"feature": f, "drop_in_ap": float(m), "std": float(s)}
         for f, m, s in zip(X_test.columns, r.importances_mean, r.importances_std)),
        key=lambda d: d["drop_in_ap"], reverse=True,
    )
    for row in ranked[:6]:
        print(f"  importance {row['feature']:24} -{row['drop_in_ap']:.4f} AP", flush=True)
    return ranked


def make_importance_chart(importance: list, out: Path) -> None:
    top = [r for r in importance if r["drop_in_ap"] > 0][:10][::-1]
    fig, ax = plt.subplots(figsize=(8.5, 4.6), constrained_layout=True)
    labels = [r["feature"].replace("_", " ") for r in top]
    ax.barh(labels, [r["drop_in_ap"] for r in top],
            xerr=[r["std"] for r in top], color="#00a89d", ecolor="#8da2ae", capsize=3)
    ax.set_xlabel("Drop in average precision when this feature is shuffled")
    ax.set_title("What the model actually relies on")
    fig.savefig(out / "importance.png", dpi=180)
    plt.close(fig)


def make_eda_detail(df: pd.DataFrame, out: Path) -> None:
    """Four further views of the data: correlations, behaviour by outcome, traffic."""
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(2, 2, figsize=(13.5, 8.6), constrained_layout=True)
    buyers = df["Revenue"].astype(bool)

    # 1. Correlation between the numeric features and the outcome.
    num = ["Administrative", "Administrative_Duration", "Informational", "Informational_Duration",
           "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "Revenue"]
    corr = df[num].astype(float).corr()
    im = ax[0][0].imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    short = [c.replace("_Duration", " time").replace("Administrative", "Admin")
              .replace("Informational", "Info").replace("ProductRelated", "Product")
              .replace("BounceRates", "Bounce").replace("ExitRates", "Exit") for c in num]
    ax[0][0].set_xticks(range(len(num)), short, rotation=45, ha="right", fontsize=9)
    ax[0][0].set_yticks(range(len(num)), short, fontsize=9)
    ax[0][0].set_title("How the numeric features relate to each other")
    for i in range(len(num)):
        for j in range(len(num)):
            v = corr.iloc[i, j]
            ax[0][0].text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                          color="white" if abs(v) > 0.55 else "#122434")
    fig.colorbar(im, ax=ax[0][0], shrink=0.8)

    # 2. Time on product pages, buyers vs non-buyers (log scale: the data is very skewed).
    data = [df.loc[~buyers, "ProductRelated_Duration"].clip(lower=1),
            df.loc[buyers, "ProductRelated_Duration"].clip(lower=1)]
    bp = ax[0][1].boxplot(data, labels=["No purchase", "Purchase"], patch_artist=True, showfliers=False)
    for patch, colour in zip(bp["boxes"], ["#8da2ae", "#00a89d"]):
        patch.set_facecolor(colour)
    ax[0][1].set_yscale("log")
    ax[0][1].set_ylabel("Seconds on product pages (log)")
    med = [float(d.median()) for d in data]
    ax[0][1].set_title(f"Buyers browse longer: median {med[1]:.0f}s vs {med[0]:.0f}s")

    # 3. Bounce and exit rates by outcome.
    labels = ["Bounce rate", "Exit rate"]
    no_buy = [df.loc[~buyers, "BounceRates"].mean() * 100, df.loc[~buyers, "ExitRates"].mean() * 100]
    buy = [df.loc[buyers, "BounceRates"].mean() * 100, df.loc[buyers, "ExitRates"].mean() * 100]
    xs = np.arange(len(labels))
    ax[1][0].bar(xs - 0.2, no_buy, 0.4, label="No purchase", color="#8da2ae")
    ax[1][0].bar(xs + 0.2, buy, 0.4, label="Purchase", color="#00a89d")
    for x, (a, b) in enumerate(zip(no_buy, buy)):
        ax[1][0].text(x - 0.2, a, f"{a:.2f}%", ha="center", va="bottom", fontsize=9)
        ax[1][0].text(x + 0.2, b, f"{b:.2f}%", ha="center", va="bottom", fontsize=9)
    ax[1][0].set_xticks(xs, labels)
    ax[1][0].set_ylabel("Average rate (%)")
    ax[1][0].set_title("Buyers disengage far less")
    ax[1][0].legend(frameon=False)

    # 4. Purchase rate by traffic source, for the sources with enough sessions to mean anything.
    traffic = df.groupby("TrafficType")["Revenue"].agg(["size", "mean"])
    traffic = traffic[traffic["size"] >= 100].sort_values("mean")
    ax[1][1].barh([f"Type {i}  (n={int(n)})" for i, n in zip(traffic.index, traffic["size"])],
                  traffic["mean"] * 100, color="#1876a3")
    ax[1][1].axvline(df["Revenue"].mean() * 100, color="#d79032", linestyle="--",
                     label=f"overall {df['Revenue'].mean() * 100:.1f}%")
    ax[1][1].set_xlabel("Purchase rate (%)")
    ax[1][1].set_title("Purchase rate by traffic source (100+ sessions)")
    ax[1][1].legend(frameon=False, loc="lower right")
    ax[1][1].tick_params(axis="y", labelsize=9)

    fig.savefig(out / "eda_detail.png", dpi=170)
    plt.close(fig)


def make_eda(df: pd.DataFrame, out: Path) -> None:
    plt.rcParams.update({"font.size": 12, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2), constrained_layout=True)
    counts = df["Revenue"].value_counts().sort_index()
    ax[0].bar(["No purchase", "Purchase"], counts.values, color=["#8da2ae", "#00a89d"])
    ax[0].set_title("Session outcomes")
    ax[0].set_ylabel("Sessions")
    monthly = df.groupby("Month")["Revenue"].agg(["size", "mean"]).reindex(["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax[1].bar(monthly.index, monthly["mean"] * 100, color="#1876a3")
    ax[1].set_title("Purchase rate by month")
    ax[1].set_ylabel("Purchase rate (%)")
    ax[1].tick_params(axis="x", rotation=45)
    visitor = df.groupby("VisitorType")["Revenue"].agg(["size", "mean"]).sort_values("mean")
    ax[2].barh(visitor.index.str.replace("_", " "), visitor["mean"] * 100, color="#d79032")
    ax[2].set_title("Purchase rate by visitor type")
    ax[2].set_xlabel("Purchase rate (%)")
    fig.savefig(out / "eda.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
