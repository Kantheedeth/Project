# SessionSignal presentation guide

Target length: **12–13 minutes**, including the live demonstration. Open `presentation.html` in a browser and advance with the right arrow. Open the Streamlit app in a second browser tab before presenting. The talk follows the rubric in the linked notebook while using the updated **7–8 member, in-session** format in the assignment message.

| Slide | Time | Suggested presenter | Main talking point |
|---|---:|---|---|
| 1. Title | 0:30 | 1 | State the question: can session behavior predict a purchase? |
| 2. Problem | 1:10 | 1 | 84.5% of UCI sessions had no purchase. Baymard's 70.22% cart abandonment figure is related business context, but it is a different measure. |
| 3. Dataset | 1:00 | 2 | Explain one row, 17 original inputs, and `Revenue` as the target. |
| 4. EDA | 1:20 | 3 | Point to the imbalance, November and February rates, and new versus returning visitors. Rates are descriptive, not causal. |
| 5. Evaluation | 1:05 | 4 | Describe duplicate removal, excluded `PageValues`, split and training-only cross-validation. |
| 6. Models | 1:15 | 4 or 5 | Give one sentence each for logistic regression, forest, boosting and baseline. |
| 7. Comparison | 1:20 | 5 | AP on the same test set: 0.156 baseline, 0.331 logistic, 0.372 forest, 0.370 boosting, 0.374 tuned forest. |
| 8. Tradeoffs | 1:10 | 6 | The chosen forest has 37.1% precision and 46.3% recall at 0.5. Top-decile ranking is stronger than a hard cutoff for prioritization. |
| 9. Product concept | 0:55 | 6 | Investigate high-intent non-purchase segments, then test changes. Do not promise recovered sales. |
| 10. Demo | 2:00 | 7 | Follow the script below. |
| 11. Next steps | 0:55 | 8 | Partial sessions, time validation, calibration, business threshold, A/B test. |
| 12. Takeaway | 0:30 | 8 | State improvement and the need for intervention testing. |

Total: **13:10**. With seven members, presenter 7 also takes slide 11–12. Replace presenter numbers with names and have each member describe their actual contribution. Suggested work allocation: problem research, dataset audit, EDA, modeling, tuning, evaluation, app/demo and slides/presentation.

## Two-minute demonstration

1. Before the talk, run `.venv/bin/streamlit run app.py` and open its local URL. Keep the page loaded in a second tab. Use browser zoom so the controls fit on screen.
2. On slide 10, switch to the app. Select a held-out example session. Explain that it was not in the training set.
3. Ask the judges whether more product-page visits should raise the purchase score. Change the product-page count and click **Predict purchase probability**. Read the score aloud.
4. Reset by choosing another example (or reload), click **Predict purchase probability**, and compare the score with the actual outcome shown. An individual mistake is expected; the reported metrics summarize 2,441 examples.
5. State that edited sessions are hypothetical. The recorded outcome belongs to the original example. Switch back to slide 11.

## Likely judge questions

**Why not accuracy?** The no-purchase baseline is 84.4% accurate on the test set, but finds zero purchasers. Purchases are 15.6% of cleaned rows, so AP and recall are more useful.

**Why did you exclude `PageValues`?** UCI defines it using average value before an ecommerce transaction. It may be difficult to make available without revenue information from the same evaluation period, so we remove it for a more defensible proof of concept.

**How did tuning help?** The forest's training-fold AP rose from 0.386 to 0.391; test AP rose from 0.372 to 0.374. Test recall at 0.5 rose from 34.6% to 46.3%, with lower precision. This is a modest improvement, not a breakthrough.

**Can you run it during a live session?** Not yet. The dataset contains completed-session aggregates. A live version needs timestamped partial-session training examples and a prospective test.

**Does it increase revenue?** The current experiment measures prediction only. A controlled intervention test would be required to estimate revenue effect.

## Source notes

Dataset counts and field definitions: [UCI dataset 468](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset). Cart abandonment context: [Baymard Institute](https://baymard.com/lists/cart-abandonment-rate). Current classification workflow: [PyCaret tutorials](https://pycaret.gitbook.io/docs/get-started/tutorials). All model metrics and EDA rates come from the supplied CSV and `artifacts/results.json`.
