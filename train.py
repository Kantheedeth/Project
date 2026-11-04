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
    precision_score,
    recall_score,
    roc_auc_score,
)
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
    joblib.dump(pipelines[chosen], OUT / "purchase_model.joblib")
    examples = X_test.copy()
    examples["Revenue"] = y_test.values.astype(bool)
    examples.sample(n=30, random_state=SEED).to_csv(OUT / "demo_sessions.csv", index=False)
    report = {
        "source_rows": int(len(raw)), "exact_duplicates_removed": duplicates,
        "rows_used": int(len(df)), "positive_rate": float(y.mean()),
        "train_rows": int(len(X_train)), "test_rows": int(len(X_test)),
        "chosen_model": chosen, "excluded_feature": "PageValues", "results": results,
    }
    (OUT / "results.json").write_text(json.dumps(report, indent=2))
    make_eda(raw, OUT)
    print(f"Saved {chosen} and report to {OUT}")


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
