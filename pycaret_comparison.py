"""Optional PyCaret replication of the model-comparison workflow.

Run in a Python environment with PyCaret installed. This uses the same cleaned
dataset and excludes PageValues, but PyCaret controls its own preprocessing.
The independently evaluated sklearn results in artifacts/results.json power
the demo and slides.
"""

from pathlib import Path
import pandas as pd
from pycaret.classification import ClassificationExperiment


ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "online_shoppers_intention.csv").drop_duplicates().drop(columns=["PageValues"])
df["Revenue"] = df["Revenue"].astype(int)
categorical = ["Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]
df = pd.get_dummies(df, columns=categorical, dtype=int)
exp = ClassificationExperiment()
exp.setup(data=df, target="Revenue", train_size=0.8, session_id=42,
          preprocess=False, fold=4, verbose=False, html=False)
best = exp.compare_models(include=["lr", "rf", "gbc"], sort="AUC", n_select=3)
leaderboard = exp.pull()
leaderboard.to_csv(ROOT / "artifacts" / "pycaret_leaderboard.csv", index=False)
print(leaderboard.to_string(index=False))
for model in best:
    print(type(model).__name__)
    predictions = exp.predict_model(model)
    print(predictions[["Revenue", "prediction_label", "prediction_score"]].tail(3).to_string(index=False))
