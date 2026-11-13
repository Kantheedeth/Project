# SessionSignal: online purchase intent proof of concept

DES423 group assignment — predictive modeling pitch.

| Student ID | Name | Main contribution |
|---|---|---|
| 6622782298 | Sirawich Narakulsookpipat | Problem research and framing |
| 6622780342 | Chaitawat Boonkitticharoen | Dataset audit and target definition |
| 6622782215 | Bhuchi Kumprakob | Exploratory data analysis |
| 6622780276 | Nonthaphat Chuathong | Evaluation design and model selection |
| 6622770657 | Kamin Sirisuwapong | PyCaret comparison and hyperparameter tuning |
| 6622772455 | Poonnawit Wongprateepwilai | Results analysis and business solution |
| 6622790267 | Choltawat Jullakasevi | Streamlit app, demonstration and limitations |

This project uses the supplied `online_shoppers_intention.csv` from the [UCI Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset). It predicts whether a completed browsing session ended in a purchase (`Revenue`).

The proposed user is an ecommerce conversion analyst. The business question is which completed sessions deserve investigation when analyst time is limited. A proposed workflow ranks sessions by model score, examines high-score sessions with no recorded purchase, and reviews user paths or support logs where those are available. The analyst can then form a checkout or support hypothesis and test a change in an A/B experiment. The current demo implements individual session scoring; batch ranking, investigation tools and experiments are proposed next steps. The model does not establish causes of abandonment or a revenue increase.

## Run the demonstration

Use Python 3.10 or 3.11. From this folder:

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python train.py
.venv/bin/streamlit run app.py
```

Open the local URL printed by Streamlit. The app has four tabs:

- **Predict** — pick a held-out session, see what that visitor did, and get an estimated chance of buying. The app labels the outcome automatically: *caught a buyer*, *correctly set aside*, or **worth investigating** when a high-scoring session did not convert.
- **How it works** — the four modelling steps, what the model looks at, and why accuracy is the wrong measure.
- **Results** — model comparison on the same held-out test set, the 2.79× top-decile lift, and the EDA charts.
- **About** — the problem with sources, the dataset, the team, and the honest limitations.

The theme is pinned in `.streamlit/config.toml` so the app renders identically on any machine, which matters when recording.

For the demonstration use examples **27** (score 68%, bought), **9** (1%, did not buy) and **8** (64%, did **not** buy — the session an analyst should investigate).

## Presentation files

| File | What it is |
|---|---|
| [presentation.html](presentation.html) | The 15-slide deck. Open in a browser, arrow keys to advance. |
| [SessionSignal.pptx](SessionSignal.pptx) | The same deck as editable PowerPoint, for import into Canva. |
| [SessionSignal_slides.pdf](SessionSignal_slides.pdf) | Flattened slides, as a presenting backup. |
| [SessionSignal_Project_Summary.pdf](SessionSignal_Project_Summary.pdf) | Plain-language summary of the whole project. |
| [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) | Run of show, speaker allocation, Thai notes, demo script, recording steps. |

The submission is a **YouTube video, 10–15 minutes at 1× speed**, with the demonstration included; the run of show is timed to **14:00**.

The already trained model and results are in `artifacts/`. You can run the app without retraining after installing dependencies. Results are deterministic with seed 42, subject to library and platform versions.

## Method and results

- 12,330 source sessions, 18 columns including target; 125 exact duplicate rows removed.
- `PageValues` is excluded because it is a revenue-derived analytics measure. This leaves 16 input features.
- Stratified 80/20 train/test split: 9,764 training rows and 2,441 held-out test rows.
- Four-fold training cross-validation compares a no-purchase baseline, weighted logistic regression, random forest and histogram gradient boosting. The strongest family by training-fold average precision is tuned with a small grid search. The test set is evaluated once per candidate.
- The tuned random forest is selected by training-fold average precision (0.391). On the test set it scores **0.374 average precision**, **0.787 ROC AUC**, **37.1% precision** and **46.3% recall** at a 0.5 threshold. Its top-scored 10% of sessions has a **43.7% purchase rate**, compared with **15.6% overall**.
- The forest tuning grid is `max_depth=[8, 16, None]` and `min_samples_leaf=[2, 5]`. The selected values are `None` and `5`. Training-fold AP improves from 0.386 to 0.391 and test AP from 0.372 to 0.374: a modest improvement.
- The full comparison and confusion matrices are in [artifacts/results.json](artifacts/results.json). Re-run `train.py` to reproduce the saved model, EDA chart and report.

Accuracy is misleading here: predicting no purchase for everyone gives 84.4% test accuracy and zero purchase recall. Average precision measures how well a model ranks rare purchases. A higher score does not imply an intervention will cause sales.

## PyCaret tutorial connection

The original linked workshop uses the removed `pycaret.nlp` module. The current [PyCaret classification tutorial](https://pycaret.gitbook.io/docs/get-started/tutorials) supports this tabular problem. [pycaret_comparison.py](pycaret_comparison.py) demonstrates the sequence `ClassificationExperiment.setup` → `compare_models` → `predict_model` with the same cleaned CSV. The saved comparison is in [artifacts/pycaret_leaderboard.csv](artifacts/pycaret_leaderboard.csv): four-fold cross-validation AUC is **0.7703** for gradient boosting, **0.7596** for random forest and **0.7098** for logistic regression. PyCaret uses its own split, manual one-hot encoding and different estimator settings; these CV AUC values are separate from the main scikit-learn holdout/AP comparison.

Artifact roles are distinct:

- `artifacts/pycaret_leaderboard.csv`: saved PyCaret training cross-validation comparison for the tutorial connection.
- `artifacts/results.json`: main scikit-learn cross-validation and held-out evaluation report.
- `artifacts/purchase_model.joblib`: fitted scikit-learn pipeline powering the Streamlit demo.
- `artifacts/demo_sessions.csv`: 30 held-out examples used by the demo; `artifacts/eda.png`: descriptive charts.

To show the existing PyCaret results during rehearsal, no PyCaret installation or retraining is needed:

```bash
cat artifacts/pycaret_leaderboard.csv
```

Displaying this file does not rerun the experiment. To reproduce the companion experiment, use a separate Python 3.10 or 3.11 environment so its dependency requirements do not change the demo environment, then run:

```bash
python -m pip install 'pycaret==3.3.2'
python pycaret_comparison.py
```

On macOS, PyCaret's optional LightGBM import may require `libomp`. If it fails before setup, install the OpenMP runtime for your platform or remove the optional `lightgbm` package; this script compares only PyCaret's built-in `lr`, `rf` and `gbc` models.

## Practical limit

The UCI rows describe completed sessions. The demonstration is a retrospective classifier, not a validated real-time recommender. To intervene while a visitor is still active, collect timestamped partial-session features, retrain and test on a later time period, then run an A/B experiment for any proposed action. `PageValues` was excluded to limit a potential source of target leakage, but this alone does not validate real-time availability of every remaining feature.

## Sources

- **Dataset attribution:** Sakar, C. & Kastro, Y. (2018). *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. [DOI: 10.24432/C5F88Q](https://doi.org/10.24432/C5F88Q). The included `online_shoppers_intention.csv` is the original source file; cleaning is performed in code. UCI publishes it under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- [UCI dataset description and citation](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
- [Baymard Institute cart abandonment study list](https://baymard.com/lists/cart-abandonment-rate) — business context only; cart abandonment differs from non-purchase sessions
- [Current PyCaret tutorials](https://pycaret.gitbook.io/docs/get-started/tutorials)
- [PyCaret classification quickstart](https://pycaret.gitbook.io/docs/get-started/quickstart)
- [Original assignment notebook and rubric](https://colab.research.google.com/drive/1pys5EpelJBWDcHZNxpeUcDDybJnLbYTV) — presentation logistics follow the latest 7–8 member, in-session assignment.
