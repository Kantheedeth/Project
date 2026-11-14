"""SessionSignal — Streamlit demonstration of the held-out shopping session classifier."""

from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"

st.set_page_config(page_title="SessionSignal", page_icon="🛒", layout="wide")

TEAL, INK, MUTED, SAND = "#008e87", "#122434", "#516477", "#d79032"

st.markdown(
    f"""
    <style>
      .block-container {{padding-top:2.2rem;padding-bottom:3rem;max-width:1180px}}
      #MainMenu, footer {{visibility:hidden}}
      .ss-head {{background:#102e3e;border-radius:14px;padding:1.5rem 1.8rem;margin-bottom:1.4rem}}
      .ss-head h1 {{color:#fff;font-size:2.1rem;margin:0;letter-spacing:-.5px}}
      .ss-head p {{color:#9fc6c4;margin:.35rem 0 0;font-size:1.02rem}}
      .ss-card {{background:#f4f8f8;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:.9rem}}
      .ss-card h4 {{margin:0 0 .6rem;font-size:.82rem;letter-spacing:.09em;
                    text-transform:uppercase;color:{TEAL};font-weight:700}}
      .ss-kv {{display:flex;justify-content:space-between;padding:.3rem 0;
               border-bottom:1px solid #e2eceb;font-size:.95rem}}
      .ss-kv:last-child {{border-bottom:none}}
      .ss-kv span:last-child {{font-weight:700;color:{INK}}}
      .ss-score {{font-size:4.2rem;font-weight:800;line-height:1;letter-spacing:-2px}}
      .ss-bar {{height:16px;background:#dce7e9;border-radius:8px;overflow:hidden;margin:.7rem 0 .3rem}}
      .ss-bar > i {{display:block;height:100%;border-radius:8px}}
      .ss-note {{font-size:.86rem;color:{MUTED};line-height:1.5}}
      .ss-flag {{border-radius:12px;padding:1rem 1.2rem;margin:.6rem 0;font-size:1rem;line-height:1.5}}
      .ss-flag.hit  {{background:#e3f6ef;border-left:5px solid {TEAL}}}
      .ss-flag.look {{background:#fdf3e3;border-left:5px solid {SAND}}}
      .ss-flag.miss {{background:#eef2f5;border-left:5px solid #8da2ae}}
      .ss-step {{display:flex;gap:.9rem;align-items:flex-start;margin:.55rem 0}}
      .ss-step b {{color:{TEAL};font-size:1.05rem;min-width:1.4rem}}
      .stTabs [data-baseweb="tab-list"] {{gap:.4rem}}
      .stTabs [data-baseweb="tab"] {{padding:.55rem 1.1rem;font-weight:600}}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ss-head"><h1>SessionSignal</h1>'
    "<p>Which online shopping visits were close to a purchase — and which ones deserve a second look?</p></div>",
    unsafe_allow_html=True,
)

if not (OUT / "purchase_model.joblib").exists():
    st.error("Run `python train.py` first to train and save the model.")
    st.stop()


@st.cache_resource
def load_model():
    return joblib.load(OUT / "purchase_model.joblib")


@st.cache_data
def load_data():
    return pd.read_csv(OUT / "demo_sessions.csv"), json.loads((OUT / "results.json").read_text())


@st.cache_data
def load_scored():
    return pd.read_csv(OUT / "scored_sessions.csv")


model = load_model()
examples, report = load_data()
res = report["results"]
chosen = report["chosen_model"]
test = res[chosen]["test"]

tab_predict, tab_find, tab_how, tab_results, tab_about = st.tabs(
    ["🔮  Score a session", "🔎  Find lost sales", "⚙️  How it works", "📊  Results", "📄  About"]
)


# ───────────────────────────── Predict ─────────────────────────────


with tab_predict:
    st.markdown(
        "Pick a **held-out** shopping session — one the model never saw while training. "
        "Every control is live: change one and the estimate updates instantly."
    )

    if "nonce" not in st.session_state:
        st.session_state.nonce = 0

    choose, clear = st.columns([4, 1], gap="medium")
    with choose:
        idx = st.selectbox(
            "Choose a held-out example session",
            range(len(examples)), index=26,
            format_func=lambda i: f"Example {i + 1}",
        )
    with clear:
        st.markdown('<div style="height:1.85rem"></div>', unsafe_allow_html=True)
        if st.button("↺ Reset edits", width="stretch",
                     help="Restore this session's original values"):
            st.session_state.nonce += 1
            st.rerun()

    row = examples.iloc[idx].copy()
    actual = bool(row.pop("Revenue"))
    k = f"{idx}_{st.session_state.nonce}"      # fresh widgets per session and per reset

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown(f"**What visitor #{idx + 1} did**")
        a, b = st.columns(2, gap="medium")
        with a:
            row["ProductRelated"] = st.slider(
                "Product pages viewed", 0, 210, int(row["ProductRelated"]), key=f"pr_{k}")
            row["BounceRates"] = st.slider(
                "Bounce rate (%)", 0.0, 20.0, round(float(row["BounceRates"]) * 100, 2),
                step=0.1, key=f"br_{k}") / 100
            visitors = ["Returning_Visitor", "New_Visitor", "Other"]
            row["VisitorType"] = st.radio(
                "Visitor type", visitors, index=visitors.index(row["VisitorType"]),
                format_func=lambda v: v.replace("_", " "), key=f"vt_{k}")
        with b:
            row["ProductRelated_Duration"] = st.slider(
                "Time on product pages (minutes)", 0.0, 160.0,
                round(float(row["ProductRelated_Duration"]) / 60, 1), step=0.5,
                key=f"prd_{k}") * 60
            row["ExitRates"] = st.slider(
                "Exit rate (%)", 0.0, 20.0, round(float(row["ExitRates"]) * 100, 2),
                step=0.1, key=f"er_{k}") / 100
            months = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            row["Month"] = st.selectbox(
                "Month", months, index=months.index(row["Month"]), key=f"mo_{k}")
            row["Weekend"] = st.toggle("Weekend", value=bool(row["Weekend"]), key=f"we_{k}")

        with st.expander("Other inputs (rarely needed)"):
            c, d = st.columns(2, gap="medium")
            with c:
                row["Administrative"] = st.number_input(
                    "Administrative pages", 0, value=int(row["Administrative"]), key=f"ad_{k}")
                row["Informational"] = st.number_input(
                    "Informational pages", 0, value=int(row["Informational"]), key=f"in_{k}")
                row["SpecialDay"] = st.number_input(
                    "Special day", 0.0, 1.0, value=float(row["SpecialDay"]), key=f"sd_{k}")
                row["Administrative_Duration"] = st.number_input(
                    "Administrative seconds", 0.0,
                    value=float(row["Administrative_Duration"]), key=f"add_{k}")
            with d:
                row["Informational_Duration"] = st.number_input(
                    "Informational seconds", 0.0,
                    value=float(row["Informational_Duration"]), key=f"ind_{k}")
                for code, label in [("OperatingSystems", "Operating system"), ("Browser", "Browser"),
                                    ("Region", "Region"), ("TrafficType", "Traffic source")]:
                    row[code] = st.number_input(
                        label, 1, value=int(row[code]), key=f"{code}_{k}")

    with right:
        p = float(model.predict_proba(pd.DataFrame([row]))[0, 1])
        colour = TEAL if p >= 0.5 else ("#b58324" if p >= 0.25 else MUTED)
        st.markdown(
            f'<div class="ss-card"><h4>Estimated chance of buying</h4>'
            f'<div class="ss-score" style="color:{colour}">{p:.0%}</div>'
            f'<div class="ss-bar"><i style="width:{max(p * 100, 1.5):.1f}%;background:{colour}"></i></div>'
            f'<div class="ss-note">0% &nbsp;—&nbsp; certainly no purchase &nbsp;·&nbsp; '
            f'100% &nbsp;—&nbsp; certainly a purchase</div></div>',
            unsafe_allow_html=True,
        )

        predicted_buy = p >= 0.5
        if predicted_buy and actual:
            st.markdown(
                '<div class="ss-flag hit"><b>✅ The model caught a buyer.</b><br>'
                "It scored this session as high intent, and this visitor really did buy.</div>",
                unsafe_allow_html=True)
        elif not predicted_buy and not actual:
            st.markdown(
                '<div class="ss-flag miss"><b>✅ Correctly set aside.</b><br>'
                "Low score, and this visitor did not buy. The analyst never has to open it.</div>",
                unsafe_allow_html=True)
        elif predicted_buy and not actual:
            st.markdown(
                '<div class="ss-flag look"><b>🔎 Worth investigating.</b><br>'
                "This visitor behaved like a buyer but left with nothing. "
                "<b>This is exactly the session SessionSignal exists to surface</b> — "
                "something may have gone wrong for them.</div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="ss-flag miss"><b>↪️ A quiet buyer the model missed.</b><br>'
                "Low score, but this visitor did buy. No model catches every case — "
                "the reported metrics summarise all 2,441 test sessions.</div>",
                unsafe_allow_html=True)

        st.markdown(
            f'<div class="ss-note">Recorded outcome for the original session '
            f'<b>#{idx + 1}</b>: <b>{"purchase" if actual else "no purchase"}</b>. '
            "If you changed any control this is now a hypothetical visitor, and that "
            "recorded outcome no longer describes them.</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────── Find lost sales ───────────────────────────
with tab_find:
    scored = load_scored()
    st.subheader("Rank every held-out session, then open the promising ones")
    st.markdown(
        f"The model scored all **{len(scored):,}** sessions it had never seen. An analyst cannot "
        "review them all, so the question is simply: **how far down the ranking can you afford to go?**"
    )

    capacity = st.slider(
        "How many sessions can your team review?", 10, 500, 50, step=10,
        help="The model ranks by score; you review from the top down.")

    top = scored.head(capacity)
    found = int(top["Revenue"].sum())
    base_rate = float(scored["Revenue"].mean())
    expected_random = base_rate * capacity

    c1, c2, c3 = st.columns(3)
    c1.metric("Buyers found in your top sessions", f"{found}")
    c2.metric("Expected if reviewed at random", f"{expected_random:.0f}")
    c3.metric("Improvement", f"{found / expected_random:.2f}×" if expected_random else "—")

    st.markdown(
        f'<div class="ss-flag hit">Reviewing the top <b>{capacity}</b> sessions surfaces '
        f'<b>{found} real buyers</b>. Picking {capacity} at random would be expected to surface about '
        f'<b>{expected_random:.0f}</b>. Same effort, <b>{found / expected_random:.2f}× the signal</b>.</div>'
        if expected_random else "", unsafe_allow_html=True)

    st.divider()
    missed = top[~top["Revenue"]].copy()
    st.subheader(f"🔎 The investigate list — {len(missed)} high-intent sessions that did not buy")
    st.markdown(
        "These visitors behaved like buyers and left with nothing. **This is the output an analyst "
        "actually works from** — the starting point for asking what went wrong."
    )
    view = pd.DataFrame({
        "Score": (missed["score"] * 100).round(0).astype(int).astype(str) + "%",
        "Product pages": missed["ProductRelated"].astype(int),
        "Minutes browsing": (missed["ProductRelated_Duration"] / 60).round(1),
        "Exit rate": (missed["ExitRates"] * 100).round(2).astype(str) + "%",
        "Visitor": missed["VisitorType"].str.replace("_", " "),
        "Month": missed["Month"],
    })
    st.dataframe(view, hide_index=True, width="stretch", height=330)
    st.caption(
        "Sorted by score, highest first. The dataset has no journey or support logs, so the next "
        "step — working out *why* each visitor left — needs data this project does not include."
    )

# ──────────────────────────── How it works ────────────────────────────
with tab_how:
    st.subheader("How SessionSignal makes a prediction")
    st.markdown(
        "The model reads **how someone browsed** and returns one number: the estimated chance "
        "that the visit ended in a purchase. It never sees the shopping cart or any money."
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="ss-card"><h4>The four steps</h4>', unsafe_allow_html=True)
        for n, text in [
            ("1", "<b>Clean the data.</b> Remove 125 duplicate rows, leaving 12,205 real visits."),
            ("2", "<b>Drop <code>PageValues</code>.</b> It is calculated from revenue, so keeping it "
                  "would be letting the model peek at the answer."),
            ("3", "<b>Split 80/20.</b> 9,764 visits to learn from, 2,441 locked away for testing."),
            ("4", "<b>Train, tune, then test once.</b> Everything is chosen using training data only."),
        ]:
            st.markdown(f'<div class="ss-step"><b>{n}</b><span>{text}</span></div>',
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ss-card"><h4>What it looks at</h4>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ss-note">'
            "<b>Browsing depth</b> — how many product, informational and account pages were opened.<br><br>"
            "<b>Time spent</b> — seconds on each kind of page.<br><br>"
            "<b>Engagement quality</b> — bounce rate and exit rate from the store's analytics.<br><br>"
            "<b>Context</b> — new or returning visitor, month, weekend, device, region, traffic source."
            "</div></div>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Why we do not use accuracy")
    st.markdown(
        f"Only **{report['positive_rate']:.1%}** of visits end in a purchase. A lazy model that always "
        f"says *“nobody will buy”* scores **{res['Always no purchase']['test']['accuracy']:.1%} accuracy** "
        "— and finds **zero** buyers. So we judge models on **average precision**, which rewards putting "
        "real buyers at the top of the ranking."
    )

    st.subheader("What it cannot do")
    st.markdown(
        "- It does **not** explain *why* a visitor left.\n"
        "- It does **not** prove the store will earn more money.\n"
        "- It works on **completed** visits only — not live, while someone is still shopping."
    )


# ────────────────────────────── Results ──────────────────────────────
with tab_results:
    st.subheader("We compared four models on exactly the same test data")

    order = ["Always no purchase", "Logistic regression", "Random forest",
             "Gradient boosting", "Random forest tuned"]
    nice = {"Always no purchase": "Always say “no purchase” (baseline)",
            "Random forest tuned": "Random forest, tuned  ← chosen"}
    best = max(res[m]["test"]["average_precision"] for m in order)
    for m in order:
        ap = res[m]["test"]["average_precision"]
        is_chosen, is_base = m == chosen, m == "Always no purchase"
        bar = "#8da2ae" if is_base else TEAL
        ci = res[m]["test"].get("average_precision_ci95")
        ci_txt = f"[{ci[0]:.3f}&ndash;{ci[1]:.3f}]" if ci else ""
        st.markdown(
            f'<div style="display:grid;grid-template-columns:17rem 1fr 3.4rem 7rem;gap:.8rem;'
            f'align-items:center;margin:.45rem 0;font-weight:{700 if is_chosen else 400}">'
            f"<span>{nice.get(m, m)}</span>"
            f'<span class="ss-bar" style="margin:0"><i style="width:{ap / best * 100:.1f}%;'
            f'background:{bar}"></i></span>'
            f"<span>{ap:.3f}</span>"
            f'<span class="ss-note" style="font-size:.78rem">{ci_txt}</span></div>',
            unsafe_allow_html=True,
        )
    st.caption("Average precision on the same untouched 2,441-session test set, with 95% "
               "bootstrap intervals. Higher is better.")

    gap = report.get("chosen_vs_runner_up")
    if gap:
        st.markdown(
            f'<div class="ss-flag look"><b>Read the intervals, not the ranking.</b><br>'
            f'{chosen} beats {report["runner_up"]} by just <b>{gap["mean"]:+.4f}</b> '
            f'(95% CI {gap["ci95"][0]:+.3f} to {gap["ci95"][1]:+.3f}, winning only '
            f'{gap["win_rate"]:.0%} of resamples). The interval crosses zero, so '
            f'<b>this difference is not statistically real</b> — our models are equivalent, '
            f'and we say so rather than claiming a winner.</div>',
            unsafe_allow_html=True)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Buyers in the top-scored 10%", f"{test['top_decile_purchase_rate']:.1%}")
    c2.metric("Buyers if picked at random", f"{report['positive_rate']:.1%}")
    c3.metric("Improvement", f"{test['top_decile_lift']:.2f}×")
    st.markdown(
        '<div class="ss-flag hit">An analyst reviewing the model’s top 10% finds '
        f"<b>{test['top_decile_lift']:.2f}× more real buyers</b> than reviewing sessions at random "
        "— the same hour of work, far better targeted.</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("What the model actually relies on")
    st.image(str(OUT / "importance.png"), width="stretch")
    imp = report.get("feature_importance", [])
    if imp:
        st.markdown(
            f'<div class="ss-flag look"><b>Worth being honest about:</b> the strongest single '
            f'feature is <b>{imp[0]["feature"]}</b>, not a browsing behaviour. The model has partly '
            "learned the seasonality of one store in one year, which is exactly why we say it needs "
            "validating on a later time period before anyone relies on it.</div>",
            unsafe_allow_html=True)

    st.divider()
    st.subheader("Improving it: the threshold mattered more than the hyperparameters")
    th = report.get("thresholds")
    if th:
        base = res[chosen]["test"]
        st.dataframe(pd.DataFrame({
            "Operating point": ["0.500 — the default", f"{th['best_f1']['threshold']:.3f} — best F1",
                                f"{th['review_top_10pct']['threshold']:.3f} — review top 10%"],
            "Precision": [f"{base['precision']:.1%}", f"{th['best_f1']['precision']:.1%}",
                          f"{th['review_top_10pct']['precision']:.1%}"],
            "Recall": [f"{base['recall']:.1%}", f"{th['best_f1']['recall']:.1%}",
                       f"{th['review_top_10pct']['recall']:.1%}"],
            "F1": [f"{base['f1']:.3f}", f"{th['best_f1']['f1']:.3f}", "—"],
        }), hide_index=True, width="stretch")
        st.markdown(
            f"Hyperparameter tuning moved average precision by **+0.002**, which the intervals above "
            f"show is noise. Moving the decision threshold from 0.5 to "
            f"**{th['best_f1']['threshold']:.3f}** lifted recall from **{base['recall']:.1%}** to "
            f"**{th['best_f1']['recall']:.1%}** and F1 from **{base['f1']:.3f}** to "
            f"**{th['best_f1']['f1']:.3f}** — a real gain, for free.")
        st.caption("Thresholds were selected on the test set, so they would need a separate "
                   "validation split before operational use.")

    st.divider()
    st.subheader("Why our AUC is 0.79 and not 0.93")
    ab = report.get("page_values_ablation")
    if ab:
        a, b = st.columns(2)
        a.metric("Without PageValues — our model", f"AP {ab['without_page_values_ap']:.3f}",
                 f"ROC AUC {ab['without_page_values_roc_auc']:.3f}", delta_color="off")
        b.metric("With PageValues", f"AP {ab['with_page_values_ap']:.3f}",
                 f"ROC AUC {ab['with_page_values_roc_auc']:.3f}", delta_color="off")
        st.markdown(
            "Published notebooks on this dataset usually score higher because they keep "
            "`PageValues`. It is computed from revenue, so a model using it is partly reading the "
            "answer. **We measured the difference rather than guessing, then dropped it anyway** — "
            "a score that good is a warning sign, not an achievement.")

    st.divider()
    st.subheader("PyCaret: the same question asked across 14 models")
    try:
        lb = pd.read_csv(OUT / "pycaret_leaderboard.csv")
        st.dataframe(
            lb[["Model", "Accuracy", "AUC", "Recall", "Prec.", "F1"]],
            hide_index=True, width="stretch", height=300)
        st.caption(
            f"PyCaret `compare_models()` over its full classifier list with `fix_imbalance=True`, "
            f"four-fold CV on its own split. Best AUC {lb['AUC'].max():.4f} "
            f"({lb.loc[lb['AUC'].idxmax(), 'Model']}) against our scikit-learn "
            f"{test['roc_auc']:.3f} — the same conclusion from a different toolchain: no model "
            "pulls clearly ahead.")
    except FileNotFoundError:
        st.info("Run `pycaret_comparison.py` to regenerate the PyCaret leaderboard.")

    st.divider()
    st.subheader("What the data looks like")
    st.image(str(OUT / "eda.png"), width="stretch")
    st.caption(
        "New visitors bought in 24.9% of sessions versus 13.9% for returning visitors. "
        "November reached 25.4%; February was 1.6%. These are associations, not causes."
    )
    st.image(str(OUT / "eda_detail.png"), width="stretch")
    st.caption(
        "Buyers spend about twice as long on product pages (median 1,110s vs 526s) and disengage "
        "far less (exit rate 1.96% vs 4.55%). Bounce and exit rates move together (r = 0.90), and "
        "exit rate is the single numeric feature most related to buying (r = −0.20)."
    )

    with st.expander("Full metrics for every model"):
        st.dataframe(
            pd.DataFrame({
                "Model": [nice.get(m, m) for m in order],
                "Avg. precision": [f"{res[m]['test']['average_precision']:.3f}" for m in order],
                "ROC AUC": [f"{res[m]['test']['roc_auc']:.3f}" for m in order],
                "Accuracy": [f"{res[m]['test']['accuracy']:.1%}" for m in order],
                "Precision": [f"{res[m]['test']['precision']:.1%}" for m in order],
                "Recall": [f"{res[m]['test']['recall']:.1%}" for m in order],
            }),
            hide_index=True, width="stretch",
        )
        st.caption("Threshold metrics use a 0.5 cutoff. Full report: `artifacts/results.json`.")


# ─────────────────────────────── About ───────────────────────────────
with tab_about:
    st.subheader("The problem")
    c1, c2, c3 = st.columns(3)
    c1.metric("Global ecommerce, 2025", "$6.42T", help="eMarketer — 20.5% of all retail sales")
    c2.metric("Average cart abandonment", "70.22%", help="Baymard Institute — 50 studies, 2006–2025")
    c3.metric("Visits here with no purchase", "84.5%", help="UCI Online Shoppers dataset")
    st.markdown(
        "Most people who visit an online store leave without buying, and that has barely changed "
        "in twenty years. Stores cannot hand-review every lost visit — **analyst attention is the "
        "scarce resource.** SessionSignal ranks completed visits so the team knows which ones to "
        "open first."
    )

    st.divider()
    st.subheader("The dataset")
    c1, c2, c3 = st.columns(3)
    c1.metric("Shopping sessions", f"{report['source_rows']:,}")
    c2.metric("Used after cleaning", f"{report['rows_used']:,}")
    c3.metric("Ended in a purchase", f"{report['positive_rate']:.1%}")
    st.markdown(
        "Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*, "
        "UCI Machine Learning Repository ([DOI 10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q)), "
        "published under CC BY 4.0. Each row is one completed visit to an online store."
    )

    st.divider()
    st.subheader("The team")
    st.dataframe(
        pd.DataFrame(
            [["6622782298", "Sirawich Narakulsookpipat", "Problem research and framing"],
             ["6622780342", "Chaitawat Boonkitticharoen", "Dataset audit and target definition"],
             ["6622782215", "Bhuchi Kumprakob", "Exploratory data analysis"],
             ["6622780276", "Nonthaphat Chuathong", "Evaluation design and model selection"],
             ["6622770657", "Kamin Sirisuwapong", "PyCaret comparison and hyperparameter tuning"],
             ["6622772455", "Poonnawit Wongprateepwilai", "Results analysis and business solution"],
             ["6622790267", "Choltawat Jullakasevi", "Streamlit app, demonstration and limitations"]],
            columns=["Student ID", "Name", "Main contribution"],
        ),
        hide_index=True, width="stretch",
    )

    st.divider()
    st.subheader("Honest limitations")
    st.info(
        "These are completed-session records from one historical dataset. A real-time version would "
        "need timestamped partial sessions, validation on a later time period, and a controlled A/B "
        "test before anyone could claim it increases sales. The model finds associations — it does "
        "not explain why a visitor left.",
        icon="⚠️",
    )
    st.caption(
        f"Model in use: **{chosen}** · held-out average precision **{test['average_precision']:.3f}** · "
        f"ROC AUC **{test['roc_auc']:.3f}** · trained with seed 42 and reproducible via `train.py`."
    )
