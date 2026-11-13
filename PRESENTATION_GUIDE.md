# SessionSignal presentation guide

**Submission:** YouTube video, **10–15 minutes at normal (1×) speed**, with the demonstration included.
**Target runtime: 14:00** — one minute of headroom under the limit.
**Deck:** `presentation.html`, **15 slides**. Open in a browser, advance with the right arrow or a click.
**Team:** 7 members. Every member speaks.

## Scoring criteria and where each mark is earned

| Category | Criteria | Ratio | Where we earn it |
|---|---|---:|---|
| Problem statement | Objective | 10% | Slide 3 — objective stated explicitly |
| | Problem importance | 15% | Slide 2 — $6.42T market, 70.22% abandonment, 84.5% non-purchase |
| | Clarity of problem statement | 15% | Slide 3 — user, situation, question, success measure, out of scope |
| Implementation | Model identification | 10% | Slide 7 — four approaches explained |
| | Solution | 10% | Slide 11 — analyst workflow built on the ranking |
| | Model comparison | 10% | Slides 8–10 — same holdout, plus PyCaret leaderboard |
| | Model improvement and tuning | 5% | Slide 9 — grid search, honest 0.386 → 0.391 |
| | Demonstration | 5% | Slide 12 — live Streamlit app on held-out data |
| Presentation | Charismatic presentation | 10% | Delivery — rehearse, do not read slides aloud |
| | Contribution of each member | 10% | Slide 14 + each member narrating their own section |

Problem statement is **40% of the grade**. Slides 2 and 3 get 2:10 of the 14:00 — do not rush them.

## Team

| Student ID | Name | Main contribution | Speaks |
|---|---|---|---|
| 6622782298 | Sirawich Narakulsookpipat | Problem research and framing | 1, 2, 3, 15 |
| 6622780342 | Chaitawat Boonkitticharoen | Dataset audit and target definition | 4 |
| 6622782215 | Bhuchi Kumprakob | Exploratory data analysis | 5 |
| 6622780276 | Nonthaphat Chuathong | Evaluation design and model selection | 6, 7 |
| 6622770657 | Kamin Sirisuwapong | PyCaret comparison and hyperparameter tuning | 8, 9 |
| 6622772455 | Poonnawit Wongprateepwilai | Results analysis and business solution | 10, 11 |
| 6622790267 | Choltawat Jullakasevi | Streamlit app, demonstration and limitations | 12, 13 |

On slide 14 each member says one line: name, student ID, what they did. That is the clearest evidence for the 10% contribution mark.

**Before recording, confirm this table matches what each person actually did** and edit both this file and slide 14 if it does not. The allocation below is a proposal, not a record.

## Run of show — 14:00

| Slide | Topic | Time | Ends at | Speaker |
|---|---|---:|---:|---|
| 1 | Title | 0:25 | 0:25 | Sirawich |
| 2 | Problem importance | 1:10 | 1:35 | Sirawich |
| 3 | Problem statement | 1:00 | 2:35 | Sirawich |
| 4 | Dataset and target | 0:50 | 3:25 | Chaitawat |
| 5 | EDA | 1:05 | 4:30 | Bhuchi |
| 6 | Evaluation design | 1:00 | 5:30 | Nonthaphat |
| 7 | Models | 0:55 | 6:25 | Nonthaphat |
| 8 | PyCaret comparison | 0:50 | 7:15 | Kamin |
| 9 | Held-out results | 1:05 | 8:20 | Kamin |
| 10 | Tradeoffs | 0:55 | 9:15 | Poonnawit |
| 11 | Product concept / solution | 1:00 | 10:15 | Poonnawit |
| 12 | **Live demonstration** | 1:50 | 12:05 | Choltawat |
| 13 | Next steps | 0:45 | 12:50 | Choltawat |
| 14 | Team and contributions | 0:40 | 13:30 | All, one line each |
| 15 | Takeaway | 0:30 | 14:00 | Sirawich |

Checkpoints while rehearsing: slide 3 ends **2:35**, slide 7 ends **6:25**, slide 11 ends **10:15**, demo ends **12:05**, finish **14:00**.

## Recording the video

1. Train/record on a machine where the app already runs. Verify first:
   ```bash
   .venv/bin/streamlit run app.py
   ```
2. Open `presentation.html` in one browser tab and the Streamlit app in a second tab. Pre-select the demo example so nothing is typed live.
3. Record the screen at 1920×1080 with the slides full-screen. OBS Studio or QuickTime screen recording both work. Record system audio plus microphone.
4. Each member records their own narration, or the team records in one continuous call — either is acceptable as long as every member is heard.
5. **Do not speed up the video.** The rubric requires 10–15 minutes at 1× speed.
6. Upload to YouTube as **Unlisted** or **Public** (not Private — judges must be able to open it). Title it `SessionSignal — DES423 Group Presentation`.
7. Put the student IDs and names in the video description as a backup for the contribution mark.

## Demonstration script — slide 12 (1:50)

The demo is worth 5% and proves the model is real. Rehearse it until it is boring.

**Use these three examples in this order.** Scores are verified against the saved model — do not pick at random on camera. Read the session's behaviour off the screen before you click Predict; that is what makes the score land.

| Step | Time | Example | App shows | Actual | Session behaviour visible on screen |
|---|---:|---|---:|---|---|
| 1 | 0:00–0:35 | **27** | **68%** | bought | 12 product pages, 12.6 min, 0% bounce, new visitor |
| 2 | 0:35–1:00 | **9** | **1%** | did not buy | 1 product page, 0 seconds, 20% bounce, returning |
| 3 | 1:00–1:40 | **8** | **64%** | **did not buy** | **38 product pages, 64.5 min, 0% bounce, 0.27% exit** |
| 4 | 1:40–1:50 | — | — | — | Closing caveat, then slide 13 |

What to say at each step:

1. **Example 27 — the model catches a buyer.** "Twelve product pages, nearly thirteen minutes, never bounced. The model gives it 68%, and this shopper did buy. The app confirms it on screen: **the model caught a buyer**."
2. **Example 9 — the model ignores a non-starter.** "One product page, zero seconds, bounced straight out. One percent. The ranking works at both ends, so analysts are not handed noise."
3. **Example 8 — the reason the product exists.** "Thirty-eight product pages. Sixty-four minutes on site. A zero percent bounce rate. The model scores it 64% — and this person did not buy. That is not a model failure, that is the single most interesting session in the dataset. Somebody spent an hour shopping and left empty-handed. **This is the session our analyst opens first.**"

Step 3 is the emotional peak of the talk. Pause after "did not buy" before explaining. Do not apologise for the prediction being "wrong" — the whole product is built on finding exactly these sessions.

Say at the start that all three are held-out sessions the model never trained on. Example 8 is the strongest moment in the talk — it turns a "wrong" prediction into the product's reason for existing, so land it deliberately rather than apologising for it.

If you want to show the interactive side, edit one input on example 27 and predict again, but say clearly that the session is now hypothetical and the recorded outcome no longer describes it. Do not promise the score will move in a particular direction.

Close by noting that one case proves nothing on its own — the reported metrics summarise 2,441 held-out sessions — and that the probability is an estimate whose calibration is future work.

Only 3 of the 30 rows in `artifacts/demo_sessions.csv` are actual purchases (examples 13, 20 and 27), which is why the selection above is fixed.

**Record a backup.** Keep a screen recording of a successful demo. If the live app misbehaves during the final take, cut to the backup and say clearly that it is a saved run.

## Thai speaker notes

### Slide 2 — problem importance

"ก่อนอื่นขอให้เห็นภาพขนาดของปัญหา ยอดขายอีคอมเมิร์ซทั่วโลกในปี 2025 อยู่ที่ประมาณ 6.42 ล้านล้านดอลลาร์ คิดเป็นราว 20.5% ของค้าปลีกทั้งหมด ขณะเดียวกัน Baymard Institute รวบรวมงานวิจัย 50 ชิ้นระหว่างปี 2006 ถึง 2025 พบว่าอัตราการละทิ้งตะกร้าสินค้าเฉลี่ยอยู่ที่ 70.22% และตัวเลขนี้แทบไม่เปลี่ยนมาตลอดสองทศวรรษ แปลว่านี่เป็นปัญหาเชิงโครงสร้าง ไม่ใช่ความผันผวนชั่วคราว ในชุดข้อมูลของเราเอง 84.5% ของ session จบลงโดยไม่มีการซื้อ ประเด็นสำคัญคือร้านค้าไม่สามารถไล่ดูทุก session ที่เสียไปได้ด้วยมือ ทรัพยากรที่ขาดแคลนจริง ๆ คือเวลาของ analyst และนั่นคือสิ่งที่เราตั้งใจแก้"

Say the external figures with their sources. Do not treat cart abandonment and session non-purchase as the same measure, and do not imply every non-purchase session is a recoverable sale.

### Slide 3 — problem statement and objective

"ผู้ใช้ของเราคือ conversion analyst ของร้านค้าออนไลน์ สถานการณ์คือมี session จำนวนมากที่จบโดยไม่ซื้อ แต่ตรวจสอบได้เพียงไม่กี่รายการ คำถามคือควรเริ่มดูอันไหนก่อน วัตถุประสงค์ของเราคือจัดอันดับ session ที่จบแล้วตามความน่าจะเป็นในการซื้อ โดยใช้พฤติกรรมการเข้าชมเท่านั้น เราวัดความสำเร็จจากการที่ผู้ซื้อจริงถูกรวมอยู่ในกลุ่มคะแนนสูง และใช้ average precision เป็นตัวชี้วัดหลัก เพราะมีเพียง 15.5% ที่ซื้อจริง ถ้าใช้ accuracy เฉย ๆ โมเดลที่ทายว่าไม่ซื้อทุกครั้งก็จะได้คะแนนสูงโดยไม่มีประโยชน์ และขอระบุให้ชัดว่าอะไรอยู่นอกขอบเขต เราไม่ได้อธิบายสาเหตุที่ลูกค้าออก ไม่ได้รับประกันว่ารายได้จะเพิ่ม และยังทำงานแบบ real-time ระหว่าง session ไม่ได้"

### Slide 7 — explain the models

"เราเริ่มจาก baseline ที่ทายว่าไม่ซื้อทุกครั้ง เพื่อดูว่าการใช้โมเดลเพิ่มประโยชน์จากการทายกลุ่มใหญ่ได้แค่ไหน Logistic regression เป็นโมเดลเชิงเส้นและให้น้ำหนักกับคลาสที่มีน้อย Random forest รวมผลจากต้นไม้หลายต้นเพื่อจับรูปแบบที่ไม่เป็นเส้นตรง ส่วน histogram gradient boosting เพิ่มต้นไม้ทีละรอบเพื่อแก้ข้อผิดพลาดที่ยังเหลือ เราเปรียบเทียบทั้งหมดบนข้อมูลชุดแบ่งเดียวกัน และใช้ AP เป็นหลัก เพราะผู้ซื้อมีสัดส่วนน้อย"

### Slide 8 — PyCaret tutorial connection

"เราเชื่อมกับ tutorial ผ่าน workflow ของ PyCaret สำหรับ classification เริ่มจาก `setup` เพื่อกำหนดข้อมูลและ target ต่อด้วย `compare_models` เพื่อเปรียบเทียบโมเดล และ `predict_model` เพื่อทำนายข้อมูล holdout ในการทดลองของ PyCaret เอง ตารางที่บันทึกไว้มี cross-validation AUC ของ gradient boosting 0.7703, random forest 0.7596 และ logistic regression 0.7098 แต่ PyCaret ใช้การแบ่งข้อมูลและการตั้งค่าของตัวเอง เราจึงไม่นำคะแนนนี้ไปปนกับ AP ของ scikit-learn ในสไลด์ถัดไป โมเดลที่ใช้ในเดโมคือ scikit-learn pipeline"

Show the saved leaderboard rather than installing anything on camera:

```bash
cat artifacts/pycaret_leaderboard.csv
```

### Slide 9 — what tuning changed

"เราเลือก family จาก AP ของ training cross-validation แล้วลอง random forest ด้วย `max_depth` เท่ากับ 8, 16 หรือไม่จำกัด และ `min_samples_leaf` เท่ากับ 2 หรือ 5 รวม 6 ชุด ค่าที่ได้คือไม่จำกัดความลึกและอย่างน้อย 5 ตัวอย่างต่อใบ AP ใน cross-validation เพิ่มจาก 0.386 เป็น 0.391 และ AP ของ test เพิ่มจาก 0.372 เป็น 0.374 จึงเป็นการปรับปรุงเล็กน้อย ไม่ใช่การเพิ่มขึ้นครั้งใหญ่ และเราไม่ได้เลือกโมเดลจากคะแนน test"

### Slide 11 — the solution

"ตัวอย่างการใช้งานที่เสนอคือให้ conversion analyst จัดอันดับ session ที่จบแล้วตามคะแนน จากนั้นเลือกกลุ่มคะแนนสูงแต่ไม่มีการซื้อไปตรวจสอบก่อน จุดสำคัญคือ 10% ที่คะแนนสูงสุดมีผู้ซื้อจริง 43.7% เทียบกับค่าเฉลี่ยทั้งชุด 15.6% หรือประมาณ 2.79 เท่า แปลว่าเวลาตรวจสอบเท่าเดิมได้เจอ session ที่เกี่ยวข้องมากขึ้นเกือบสามเท่า หากมีข้อมูลเส้นทางผู้ใช้หรือ support logs เพิ่มเติม ก็ใช้ดูว่ามีจุดใดที่ควรตั้งสมมติฐาน เช่น ขั้นตอน checkout ที่อาจสร้างความสับสน แล้วออกแบบการเปลี่ยนแปลงและทดสอบด้วย A/B test เดโมวันนี้ทำได้เฉพาะการให้คะแนนทีละ session ส่วนการจัดอันดับทั้งชุดยังเป็นแนวทางที่เสนอ คะแนนไม่ได้บอกสาเหตุที่คนออก และยังไม่พิสูจน์ว่ารายได้จะเพิ่มขึ้น"

### Slide 14 — contributions

Each member, one line: "ผม/ดิฉัน [ชื่อ] รหัส [ID] รับผิดชอบ [งาน]". Keep it to five seconds each.

## Rehearsal checklist

- [ ] Confirm the contribution table matches what each person actually did.
- [ ] Each member can explain their own section without reading the slide text.
- [ ] Two demo examples chosen and their numbers written down.
- [ ] Backup screen recording of a working demo saved.
- [ ] One full timed run-through, including tab switching, lands at 14:00 ± 30s.
- [ ] All 15 slides render and `artifacts/eda.png` appears on slide 5.
- [ ] PDF export saved (browser print → Save as PDF) as a fallback.
- [ ] Video uploaded Unlisted or Public, names and IDs in the description.

## Likely judge questions

**Why not accuracy?** The no-purchase baseline is 84.4% accurate on the test set but identifies zero purchasers. Purchases are about 15.6% of cleaned rows, so AP and recall are more informative.

**Why exclude `PageValues`?** It is a revenue-derived analytics measure and a leakage risk. Removing it limits that risk; it does not prove the remaining completed-session features would be available live.

**Why does PyCaret rank models differently?** Its CV AUC uses its own split, preprocessing and estimator settings. The main experiment selects by training-fold AP and reports the same scikit-learn holdout for every candidate. Two separate experiments, not one leaderboard.

**How did tuning help?** Training-fold AP rose 0.386 → 0.391; test AP 0.372 → 0.374. Test recall at 0.5 rose from 34.6% to 46.3%, at lower precision. A modest gain, honestly reported.

**Can you use it while a visitor is still browsing?** Not yet. These are completed-session aggregates. A live version needs timestamped partial-session examples and validation on a later period.

**Does this increase revenue or explain why someone left?** Neither is established. The proposed use is prioritising investigation. A controlled experiment would be needed to estimate revenue effect.

## Source notes

- [Assignment notebook and rubric](https://colab.research.google.com/drive/1pys5EpelJBWDcHZNxpeUcDDybJnLbYTV).
- [eMarketer](https://www.emarketer.com/content/ecommerce-account-more-than-20--of-worldwide-retail-sales-despite-slowdown): global retail ecommerce $6.42 trillion in 2025, 20.5% of total retail.
- [Baymard Institute](https://baymard.com/lists/cart-abandonment-rate): 70.22% average cart abandonment, unweighted average of 50 studies published 2006–2025, range 55%–84%. Different population and event from session non-purchase.
- [UCI dataset 468](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset): source data and field definitions. EDA uses the 12,330 source rows; modeling uses 12,205 rows after duplicate removal, split 9,764 train / 2,441 test.
- [PyCaret tutorials](https://pycaret.gitbook.io/docs/get-started/tutorials): classification workflow. Saved results in `artifacts/pycaret_leaderboard.csv`.
- Model metrics and confusion matrices: `artifacts/results.json`. Demo model: `artifacts/purchase_model.joblib`.
