"""Streamlit demonstration of the held-out shopping session classifier."""

from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
st.set_page_config(page_title="SessionSignal demo", page_icon="🛒", layout="wide")
st.title("SessionSignal")
st.caption("Proof of concept: estimate whether a browsing session ends with a purchase")

if not (OUT / "purchase_model.joblib").exists():
    st.error("Run `python train.py` first to train and save the model.")
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load(OUT / "purchase_model.joblib")

@st.cache_data
def load_data():
    return pd.read_csv(OUT / "demo_sessions.csv"), json.loads((OUT / "results.json").read_text())

model = load_model()
examples, report = load_data()
idx = st.selectbox("Choose a held-out example session", range(len(examples)), format_func=lambda i: f"Example {i+1}")
row = examples.iloc[idx].copy()
actual = bool(row.pop("Revenue"))

st.write("Edit the session information, then click **Predict**. Other fields retain the selected example's values.")
# Changing examples must also reset any edits to the previous session.
with st.form(f"predict_{idx}"):
    a, b, c = st.columns(3)
    with a:
        row["ProductRelated"] = st.number_input("Product pages visited", min_value=0, value=int(row["ProductRelated"]))
        row["ProductRelated_Duration"] = st.number_input("Time on product pages (seconds)", min_value=0.0, value=float(row["ProductRelated_Duration"]))
        row["Administrative"] = st.number_input("Administrative pages visited", min_value=0, value=int(row["Administrative"]))
    with b:
        row["Informational"] = st.number_input("Informational pages visited", min_value=0, value=int(row["Informational"]))
        row["BounceRates"] = st.number_input("Bounce rate", min_value=0.0, max_value=1.0, value=float(row["BounceRates"]), format="%.4f")
        row["ExitRates"] = st.number_input("Exit rate", min_value=0.0, max_value=1.0, value=float(row["ExitRates"]), format="%.4f")
    with c:
        visitors = ["Returning_Visitor", "New_Visitor", "Other"]
        row["VisitorType"] = st.selectbox("Visitor type", visitors, index=visitors.index(row["VisitorType"]))
        months = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        row["Month"] = st.selectbox("Month", months, index=months.index(row["Month"]))
        row["Weekend"] = st.checkbox("Weekend", value=bool(row["Weekend"]))
    with st.expander("Other model inputs"):
        for key in ["Administrative_Duration", "Informational_Duration", "SpecialDay"]:
            row[key] = st.number_input(key, min_value=0.0, value=float(row[key]))
        for key in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
            row[key] = st.number_input(key, min_value=1, value=int(row[key]))
    submitted = st.form_submit_button("Predict purchase probability", type="primary")

if submitted:
    p = float(model.predict_proba(pd.DataFrame([row]))[0, 1])
    st.metric("Estimated purchase probability", f"{p:.1%}")
    st.write(f"Observed outcome for the original example: **{'purchase' if actual else 'no purchase'}**. If you edited inputs, that outcome does not describe your hypothetical session.")
    st.progress(p)

st.divider()
st.subheader("How to interpret this demo")
st.write(f"The chosen model is **{report['chosen_model']}**. It was selected by cross-validated average precision using training data only. Its holdout average precision is **{report['results'][report['chosen_model']]['test']['average_precision']:.3f}**; the holdout purchase rate is **{report['positive_rate']:.1%}**.")
st.info("These are completed-session records from one historical dataset. A real-time intervention would require training and validating on partial sessions, then testing any action in a controlled experiment. The prediction is not evidence that an intervention will cause a purchase.")
