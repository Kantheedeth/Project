# SessionSignal presentation guide

Target length: **14:00**, including a **2:00 live demonstration**, for **7–8 members presenting in session**. This follows the latest assignment message; the older notebook's recording instructions do not set the presentation format. The English deck has 13 slides. Open `presentation.html` in a browser and keep the Streamlit app ready in a second tab.

The [original notebook and rubric](https://colab.research.google.com/drive/1pys5EpelJBWDcHZNxpeUcDDybJnLbYTV) gives **40% to the problem** and **10% to individual contributions**. Make the user, decision and supporting facts clear. Presenter numbers below are a proposed speaking allocation, not a record of work completed. Adapt the allocation to the team's actual work.

## Run of show

| Slide | Time | End | Suggested presenter | Main talking point |
|---|---:|---:|---|---|
| 1. Title | 0:30 | 0:30 | 1 | Can browsing behavior rank purchase intent? |
| 2. Problem | 1:10 | 1:40 | 1 | The user is an ecommerce conversion analyst with limited investigation time. 84.5% of source sessions ended without purchase; external cart-abandonment figures are separate business context. |
| 3. Dataset | 1:00 | 2:40 | 2 | One row is a completed session; 12,330 rows, 17 original inputs and `Revenue` as target. |
| 4. EDA | 1:20 | 4:00 | 3 | Explain imbalance and purchase-rate differences by month and visitor type; associations are not causes. |
| 5. Evaluation | 1:05 | 5:05 | 4 | Remove 125 duplicates, exclude `PageValues`, stratify 80/20 and use four-fold training cross-validation. |
| 6. Models | 1:00 | 6:05 | 4 | Explain logistic regression, random forest, histogram gradient boosting and the no-purchase baseline. |
| 7. PyCaret | 0:50 | 6:55 | 5 | Show `setup` → `compare_models` → `predict_model`; explain that saved CV AUC uses a separate split from the main experiment. |
| 8. Comparison | 1:20 | 8:15 | 5 | Main holdout AP: 0.156 baseline, 0.331 logistic, 0.372 forest, 0.370 boosting and 0.374 tuned forest. Explain the small tuning gain. |
| 9. Tradeoffs | 1:10 | 9:25 | 6 | At 0.5, chosen precision is 37.1% and recall 46.3%. Top-scored 10% has a 43.7% purchase rate; prioritization still needs a business decision. |
| 10. Product concept | 1:10 | 10:35 | 6 | Prioritize retrospective investigation of high-score, non-purchase sessions; form a hypothesis and test a change later. |
| 11. Demo | 2:00 | 12:35 | 7 | Score an original held-out session, edit one field and distinguish the hypothetical case from its original outcome. |
| 12. Next steps | 0:55 | 13:30 | 8 | Partial-session data, later-period validation, calibration, subgroup checks, action threshold and A/B test. |
| 13. Takeaway | 0:30 | 14:00 | 8 | Ranking improves over baseline; operational value and sales impact still need testing. |

Total: **14:00**. With seven members, presenter 7 also presents slides 12–13. Keep the same total time and share preparation work according to what each person actually did.

## Suggested work areas and presentation materials

This is a suggested allocation to adapt to actual contributions. The file references show existing material to explain or review; they do not establish who created it. Each presenter should describe the work they actually did.

| Presenter | Suggested work area | Material to explain or review | Suggested slides |
|---|---|---|---|
| 1 | Problem framing and source research | [README.md](README.md), sources on slide 2 in [presentation.html](presentation.html) | 1–2 |
| 2 | Dataset audit and target definition | [online_shoppers_intention.csv](online_shoppers_intention.csv), cleaning in [train.py](train.py) | 3 |
| 3 | Exploratory data analysis | [artifacts/eda.png](artifacts/eda.png), `make_eda` in [train.py](train.py) | 4 |
| 4 | Evaluation design and model explanations | Pipelines and split in [train.py](train.py), [artifacts/results.json](artifacts/results.json) | 5–6 |
| 5 | PyCaret comparison and tuning | [pycaret_comparison.py](pycaret_comparison.py), [artifacts/pycaret_leaderboard.csv](artifacts/pycaret_leaderboard.csv), tuning in [train.py](train.py) | 7–8 |
| 6 | Evaluation tradeoffs and proposed business use | [artifacts/results.json](artifacts/results.json), business workflow in [README.md](README.md) | 9–10 |
| 7 | App and held-out demonstration | [app.py](app.py), [artifacts/demo_sessions.csv](artifacts/demo_sessions.csv), [artifacts/purchase_model.joblib](artifacts/purchase_model.joblib) | 11 |
| 8 | Limitations, improvement ideas and presentation review | Practical limits in [README.md](README.md), slides 12–13 in [presentation.html](presentation.html), this rehearsal guide | 12–13 |

For a seven-person team, presenter 7 also covers slides 12–13. Preparation and review can be shared; speaking slide numbers do not establish ownership of the underlying work.

## Thai speaker notes

### Slide 2 — problem and user

“ผู้ใช้ที่เราออกแบบให้คือ analyst ที่ดูแล conversion ของร้านค้าออนไลน์ ข้อมูลนี้มี session ที่ไม่เกิดการซื้อประมาณ 84.5% แต่ทีมงานมีเวลาตรวจสอบจำกัด คำถามจึงเป็นว่าเราจะช่วยเลือก session ที่ควรนำไปศึกษาต่อได้ไหม เราใช้พฤติกรรมการเข้าชมเพื่อจัดลำดับความตั้งใจซื้อ แล้วเสนอให้ตรวจสอบกลุ่มที่คะแนนสูงแต่ไม่ซื้อ ส่วนสถิติ cart abandonment ที่อ้างจาก Baymard เป็นบริบททางธุรกิจ ซึ่งวัดคนละเหตุการณ์กับ session ที่ไม่ซื้อใน dataset นี้”

State the external figure shown on the slide with its source. Do not treat cart abandonment and session non-purchase as interchangeable, or infer that every non-purchase session represents a recoverable sale.

### Slide 6 — explain the models

“เราเริ่มจาก baseline ที่ทายว่าไม่ซื้อทุกครั้ง เพื่อดูว่าการใช้โมเดลเพิ่มประโยชน์จากการทายกลุ่มใหญ่ได้แค่ไหน Logistic regression เป็นโมเดลเชิงเส้นและให้น้ำหนักกับคลาสที่มีน้อย Random forest รวมผลจากต้นไม้หลายต้นเพื่อจับรูปแบบที่ไม่เป็นเส้นตรง ส่วน histogram gradient boosting เพิ่มต้นไม้ทีละรอบเพื่อแก้ข้อผิดพลาดที่ยังเหลือ เราเปรียบเทียบทั้งหมดด้วยข้อมูลแบ่งชุดเดียวกัน และใช้ AP เป็นหลัก เพราะผู้ซื้อมีสัดส่วนน้อย”

### Slide 7 — PyCaret tutorial connection

“เราเชื่อมกับ tutorial ผ่าน workflow ของ PyCaret สำหรับ classification เริ่มจาก `setup` เพื่อกำหนดข้อมูลและ target ต่อด้วย `compare_models` เพื่อเปรียบเทียบโมเดล และ `predict_model` เพื่อทำนายข้อมูล holdout ในการทดลองของ PyCaret เอง ตารางที่บันทึกไว้มี cross-validation AUC ของ gradient boosting 0.7703, random forest 0.7596 และ logistic regression 0.7098 แต่ PyCaret ใช้การแบ่งข้อมูลและการตั้งค่าของตัวเอง เราจึงไม่นำคะแนนนี้ไปปนกับ AP ของ scikit-learn ในสไลด์ถัดไป โมเดลที่ใช้ในเดโมคือ scikit-learn pipeline”

For rehearsal, open `pycaret_comparison.py` and the saved leaderboard. There is no need to install or retrain PyCaret during the presentation:

```bash
cat artifacts/pycaret_leaderboard.csv
```

This command displays an existing artifact; it does not reproduce the experiment. PyCaret's `compare_models` table is training cross-validation, whereas `predict_model` in the script evaluates its own holdout. The main scikit-learn results use a separate held-out comparison.

### Slide 8 — what tuning changed

“เราเลือก family จาก AP ของ training cross-validation แล้วลอง random forest ด้วย `max_depth` เท่ากับ 8, 16 หรือไม่จำกัด และ `min_samples_leaf` เท่ากับ 2 หรือ 5 รวม 6 ชุด ค่าที่ได้คือไม่จำกัดความลึกและอย่างน้อย 5 ตัวอย่างต่อใบ AP ใน cross-validation เพิ่มจาก 0.386 เป็น 0.391 และ AP ของ test เพิ่มจาก 0.372 เป็น 0.374 จึงเป็นการปรับปรุงเล็กน้อย ไม่ใช่การเพิ่มขึ้นครั้งใหญ่ และเราไม่ได้เลือกโมเดลจากคะแนน test”

### Slide 10 — concrete business use

“ตัวอย่างการใช้งานที่เสนอคือให้ conversion analyst จัดอันดับ session ที่จบแล้วตามคะแนน จากนั้นเลือกกลุ่มคะแนนสูงแต่ไม่มีการซื้อไปตรวจสอบก่อน หากมีข้อมูลเส้นทางผู้ใช้หรือ support logs เพิ่มเติม ก็ใช้ดูว่ามีจุดใดที่ควรตั้งสมมติฐาน เช่น ขั้นตอน checkout ที่อาจสร้างความสับสน แล้วออกแบบการเปลี่ยนแปลงและทดสอบด้วย A/B test เดโมวันนี้ทำได้เฉพาะการให้คะแนนทีละ session ส่วนการจัดอันดับทั้งชุดและเครื่องมือสอบสวนยังเป็นแนวทางที่เสนอ คะแนนไม่ได้บอกสาเหตุที่คนออก และยังไม่พิสูจน์ว่ารายได้จะเพิ่มขึ้น”

The dataset does not include user paths or support logs; these would be additional sources if available. Completed-session scores support retrospective analysis. Live intervention requires partial-session training data and later validation.

## Two-minute demonstration — slide 11

1. Before speaking, run `.venv/bin/streamlit run app.py`, open its local URL and keep it ready. Select an example and use browser zoom so the controls fit.
2. **0:00–0:35:** Click **Predict purchase probability** for the original example. Explain that it is held out from training; read the model score and original recorded outcome.
3. **0:35–1:15:** Change one input, such as product-page count, and predict again. Explain that a hypothetical change can alter the score; do not promise a particular direction or claim a causal effect.
4. **1:15–1:45:** Choose another example and predict its original values. Point out that one correct or incorrect case does not summarize performance; the reported test metrics use 2,441 sessions.
5. **1:45–2:00:** State that the displayed outcome belongs to the original example, not an edited hypothetical session. The displayed probability is a model estimate; calibration remains future work. Return to slide 12.

The demo currently scores individual sessions. Do not present batch ranking, support-log inspection or A/B experimentation as existing app features.

## Rehearsal and readiness

- Adapt the suggested work areas to actual contributions, agree on speaking handovers, and confirm each person can explain their own work using the referenced materials.
- Check all 13 slides, the EDA image and source links. Keep external statistics consistent with the cited source and the deck.
- Open the app before the talk, try an original prediction, edit an input, and switch examples. Keep a screenshot of a real demo result as a presentation backup, clearly described as saved output if used.
- Keep `artifacts/pycaret_leaderboard.csv` and `pycaret_comparison.py` available; show saved results rather than installing packages on stage.
- Rehearse once with a timer, including app switching. Reach slide 4's end at **4:00**, slide 7's end at **6:55**, slide 10's end at **10:35**, finish the demo at **12:35** and finish the talk at **14:00**. This leaves one minute within the 15-minute limit for handovers or small delays.
- Confirm that every required topic is spoken: dataset/target, EDA, evidenced real-world problem, multiple models on the same main split, how predictions support a decision, and improvement ideas. Problem framing deserves particular rehearsal because it carries 40% of the rubric.

The technical artifacts and suggested script are present. Complete a timed group rehearsal to check delivery and handovers.

## Likely judge questions

**Why not accuracy?** The no-purchase baseline is 84.4% accurate on the test set but identifies zero purchasers. Purchases are about 15.6% of cleaned rows, so AP and recall provide more useful context.

**Why exclude `PageValues`?** It is a revenue-derived analytics measure and a potential leakage concern. Removing it limits one risk; it does not prove the remaining completed-session features are available for live prediction.

**Why does PyCaret rank models differently?** Its CV AUC uses its own split, preprocessing and estimator settings. The main experiment selects by training-fold AP and reports the same scikit-learn holdout for every candidate. These are separate experiments, not one interchangeable leaderboard.

**How did tuning help?** The forest's training-fold AP rose from 0.386 to 0.391; test AP rose from 0.372 to 0.374. Test recall at 0.5 rose from 34.6% to 46.3%, with lower precision. The gain is modest.

**Can you use it while a visitor is still browsing?** Not yet. These are completed-session aggregates. A live version needs timestamped partial-session examples and validation on a later period.

**Does this increase revenue or explain why someone left?** Neither is established. The proposed use is investigation prioritization. Additional evidence and a controlled intervention test are needed to estimate causes and revenue effect.

## Source notes

- [Original assignment notebook and rubric](https://colab.research.google.com/drive/1pys5EpelJBWDcHZNxpeUcDDybJnLbYTV); latest assignment message controls the 7–8 member, in-session format and 10–15 minute duration.
- [UCI dataset 468](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset): source data and field definitions. Source-data EDA uses 12,330 rows; the modeling dataset has 12,205 rows after duplicate removal, split into 9,764 training and 2,441 test rows.
- [Baymard cart-abandonment research](https://baymard.com/lists/cart-abandonment-rate): external business context, with a different population and outcome from non-purchase sessions.
- [PyCaret tutorials](https://pycaret.gitbook.io/docs/get-started/tutorials): classification workflow. Saved PyCaret results are in `artifacts/pycaret_leaderboard.csv`.
- Main model metrics and confusion matrices are in `artifacts/results.json`; the demo model is `artifacts/purchase_model.joblib`.
