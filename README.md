# SessionSignal: online purchase intent proof of concept

This project uses the supplied `online_shoppers_intention.csv` from the [UCI Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset). It predicts whether a completed browsing session ended in a purchase (`Revenue`).

## Run the demonstration

Use Python 3.10 or 3.11. From this folder:

```bash
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python train.py
.venv/bin/streamlit run app.py
```

Open the local URL printed by Streamlit. Select a held-out example, edit some inputs, and click **Predict purchase probability**. The app shows the recorded outcome for the original example so judges can compare prediction and reality. The slide deck is [presentation.html](presentation.html); open it in a browser and use the arrow keys or click to advance. Browser print can produce a PDF. Presenter notes and a 12-minute run of show are in [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md).

The already trained model and results are in `artifacts/`. You can run the app without retraining after installing dependencies. Results are deterministic with seed 42, subject to library and platform versions.

## Method and results

- 12,330 source sessions, 18 columns including target; 125 exact duplicate rows removed.
- `PageValues` is excluded because it is a revenue-derived analytics measure. This leaves 16 input features.
- Stratified 80/20 train/test split: 9,764 training rows and 2,441 held-out test rows.
- Four-fold training cross-validation compares a no-purchase baseline, weighted logistic regression, random forest and histogram gradient boosting. The strongest family by training-fold average precision is tuned with a small grid search. The test set is evaluated once per candidate.
- The tuned random forest is selected by training-fold average precision (0.391). On the test set it scores **0.374 average precision**, **0.787 ROC AUC**, **37.1% precision** and **46.3% recall** at a 0.5 threshold. Its top-scored 10% of sessions has a **43.7% purchase rate**, compared with **15.6% overall**.
- The full comparison and confusion matrices are in [artifacts/results.json](artifacts/results.json). Re-run `train.py` to reproduce the saved model, EDA chart and report.

Accuracy is misleading here: predicting no purchase for everyone gives 84.4% test accuracy and zero purchase recall. Average precision measures how well a model ranks rare purchases. A higher score does not imply an intervention will cause sales.

## PyCaret tutorial connection

The original linked workshop uses the removed `pycaret.nlp` module. The current [PyCaret classification tutorial](https://pycaret.gitbook.io/docs/get-started/tutorials) supports this tabular problem. [pycaret_comparison.py](pycaret_comparison.py) demonstrates `ClassificationExperiment.setup`, `compare_models` and `predict_model` with the same cleaned CSV. Its verified comparison is saved in [artifacts/pycaret_leaderboard.csv](artifacts/pycaret_leaderboard.csv). It uses PyCaret's own split and manual one-hot encoding, so its metrics should be read separately from the main scikit-learn holdout comparison. The reproducible model powering the live app is a scikit-learn pipeline. Install PyCaret separately if you want to run the companion script:

```bash
.venv/bin/python -m pip install 'pycaret==3.3.2'
.venv/bin/python pycaret_comparison.py
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
