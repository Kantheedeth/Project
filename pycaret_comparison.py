"""PyCaret replication of the model comparison, using the library's own workflow.

The course is built around PyCaret, so this runs the full `compare_models`
sweep rather than a hand-picked shortlist, with PyCaret's own imbalance
handling switched on. It uses the same cleaned data and the same excluded
PageValues column as train.py, but PyCaret controls its own split and
preprocessing, so read these numbers alongside — not merged into — the
scikit-learn holdout results in artifacts/results.json.

Run in a separate environment:
    python -m pip install 'pycaret==3.3.2' six
    python pycaret_comparison.py
"""

from pathlib import Path

import pandas as pd
from pycaret.classification import ClassificationExperiment


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts"
SEED = 42

df = pd.read_csv(ROOT / "online_shoppers_intention.csv").drop_duplicates()
df = df.drop(columns=["PageValues"])          # same leakage exclusion as train.py
df["Revenue"] = df["Revenue"].astype(int)
CATEGORICAL = ["Month", "OperatingSystems", "Browser", "Region", "TrafficType",
               "VisitorType", "Weekend"]
# PyCaret's imputer cannot cast a bool/int categorical to float, so hand these
# over as plain strings and let it build its own encoding.
df[CATEGORICAL] = df[CATEGORICAL].astype(str)

exp = ClassificationExperiment()
exp.setup(
    data=df, target="Revenue", train_size=0.8, session_id=SEED,
    categorical_features=CATEGORICAL, fold=4,
    fix_imbalance=True,        # purchases are 15.6% of rows; without this recall collapses
    verbose=False, html=False,
)

# Compare every classifier PyCaret ships with. PyCaret ranks by AUC here because
# average precision is not one of its sort options; the scikit-learn experiment
# remains the one that selects on AP.
best = exp.compare_models(sort="AUC", n_select=3)
leaderboard = exp.pull()
leaderboard.to_csv(OUT / "pycaret_leaderboard.csv", index=False)
print(leaderboard.to_string())

print(f"\nModels compared: {len(leaderboard)}")
print("Top 3 by AUC:", ", ".join(leaderboard["Model"].head(3)))

# Tune and evaluate the strongest model on PyCaret's own holdout.
tuned = exp.tune_model(best[0], optimize="AUC", n_iter=20, choose_better=True)
holdout = exp.predict_model(tuned)
exp.pull().to_csv(OUT / "pycaret_tuned_holdout.csv", index=False)
print("\nTuned model on PyCaret's holdout:")
print(exp.pull().to_string(index=False))
