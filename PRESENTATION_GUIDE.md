# SessionSignal presentation guide

**Length:** 10–15 minutes at normal (1×) speed, demonstration included. **Our run of show is timed to 14:00.**
**Deck:** `presentation.html` — **17 slides**. Also `SessionSignal.pptx` (editable) and `SessionSignal_slides.pdf` (backup).
**Team:** 7 members. Every member presents their own section.

> **Delivery mode — confirm with the lecturer.** The notebook says *submit as a YouTube video*; the class message says *present live in the last session*. The deck wording works for both. Use the matching checklist at the bottom.

## Where each mark is earned

| Category | Criteria | Ratio | Where |
|---|---|---:|---|
| Problem statement | Objective | 10% | Slide 3 — objective stated explicitly |
| | Problem importance | 15% | Slide 2 — $6.42T market, 70.22% abandonment, 84.5% non-purchase |
| | Clarity | 15% | Slide 3 — user, situation, question, success measure, out of scope |
| Implementation | Model identification | 10% | Slide 8 — four approaches; slide 9 — 14 more via PyCaret |
| | Solution | 10% | Slide 13 + the **Find lost sales** tab — a working worklist, not a proposal |
| | Model comparison | 10% | Slides 9–10 — same holdout, 14-model sweep, confidence intervals |
| | Improvement and tuning | 5% | Slide 12 — threshold beat hyperparameters, and we show why |
| | Demonstration | 5% | Slide 14 — live app on held-out data |
| Presentation | Charismatic presentation | 10% | Delivery — rehearse; do not read the slides aloud |
| | Contribution of each member | 10% | Slide 16 + each member presenting their own section |

Problem statement is **40% of the grade**. Slides 2–3 get 1:55 of the 14:00 — do not rush them.

## Team

| Student ID | Name | Contribution | Slides |
|---|---|---|---|
| 6622782298 | Sirawich Narakulsookpipat | Problem research and framing | 1, 2, 3, 17 |
| 6622780342 | Chaitawat Boonkitticharoen | Dataset audit and target definition | 4 |
| 6622782215 | Bhuchi Kumprakob | Exploratory data analysis | 5, 6 |
| 6622780276 | Nonthaphat Chuathong | Evaluation design and model selection | 7, 8 |
| 6622770657 | Kamin Sirisuwapong | PyCaret comparison, results and interpretation | 9, 10, 11 |
| 6622772455 | Poonnawit Wongprateepwilai | Improvement and business solution | 12, 13 |
| 6622790267 | Choltawat Jullakasevi | Streamlit app, demonstration and limitations | 14, 15 |

On slide 16 each member says one line: name, ID, what they did. **Confirm this table matches reality before presenting** and edit it here and on slide 16 if it does not.

## Run of show — 14:00

| # | Slide | Time | Ends | Speaker |
|---|---|---:|---:|---|
| 1 | Title | 0:20 | 0:20 | Sirawich |
| 2 | Problem importance | 1:00 | 1:20 | Sirawich |
| 3 | Problem statement | 0:55 | 2:15 | Sirawich |
| 4 | Dataset and target | 0:40 | 2:55 | Chaitawat |
| 5 | EDA — outcomes, month, visitor type | 0:45 | 3:40 | Bhuchi |
| 6 | EDA — correlations, behaviour, traffic | 0:50 | 4:30 | Bhuchi |
| 7 | Evaluation design | 0:45 | 5:15 | Nonthaphat |
| 8 | Models | 0:45 | 6:00 | Nonthaphat |
| 9 | PyCaret — 14 models | 0:50 | 6:50 | Kamin |
| 10 | Held-out results and intervals | 1:05 | 7:55 | Kamin |
| 11 | What the model relies on | 0:50 | 8:45 | Kamin |
| 12 | Improvement — threshold | 0:55 | 9:40 | Poonnawit |
| 13 | Solution — score to worklist | 0:45 | 10:25 | Poonnawit |
| 14 | **Live demonstration** | 2:00 | 12:25 | Choltawat |
| 15 | Next steps | 0:35 | 13:00 | Choltawat |
| 16 | Team and contributions | 0:40 | 13:40 | All, one line each |
| 17 | Takeaway | 0:20 | 14:00 | Sirawich |

Rehearsal checkpoints: slide 3 ends **2:15**, slide 8 ends **6:00**, slide 11 ends **8:45**, demo ends **12:25**, finish **14:00**.

## Demonstration script — slide 14 (2:00)

Open the app first: `.venv/bin/streamlit run app.py`. Two tabs, two minutes.

### Part 1 — Score a session (1:15)

Pick each from the **Choose a held-out example session** dropdown. The score updates live; there is no button to press. Read the visitor's behaviour off the controls **before** pointing at the score.

| Example | App shows | Actual | What you say |
|---|---:|---|---|
| **27** | **68%** | bought | "12 product pages, nearly 13 minutes, never bounced. 68% — and this shopper did buy. The app says: *caught a buyer*." |
| **9** | **1%** | did not buy | "One page, zero seconds, bounced straight out. One percent. The ranking works at both ends." |
| **8** | **64%** | **did not buy** | "38 product pages. 64 minutes. Zero bounce. The model says 64% — and this person bought nothing." |

**Pause after "bought nothing."** Then: *"That is not a model failure. Somebody shopped for an hour and left empty-handed. **This is the session our analyst opens first.**"*

Optional if time allows: drag **Product pages viewed** down to ~2 on example 8. The score falls to ~46% and the verdict flips live to *correctly set aside*. Say the session is now hypothetical, then press **↺ Reset edits**.

### Part 2 — Find lost sales (0:45)

Switch to the **🔎 Find lost sales** tab. All 2,441 held-out sessions, ranked.

- Leave capacity at **50**. Read out: **25 real buyers found, versus about 8 expected at random — 3.2×.**
- Scroll to the investigate list: **25 high-intent sessions that bought nothing.**
- Say: *"This is the actual output. Not a score for one visitor — a worklist an analyst starts their Monday with."*

Then move to slide 15.

## Thai speaker notes

### Slide 2 — problem importance
"ก่อนอื่นขอให้เห็นภาพขนาดของปัญหา ยอดขายอีคอมเมิร์ซทั่วโลกในปี 2025 อยู่ที่ประมาณ 6.42 ล้านล้านดอลลาร์ คิดเป็นราว 20.5% ของค้าปลีกทั้งหมด ขณะเดียวกัน Baymard Institute รวบรวมงานวิจัย 50 ชิ้นระหว่างปี 2006 ถึง 2025 พบว่าอัตราการละทิ้งตะกร้าสินค้าเฉลี่ยอยู่ที่ 70.22% และแทบไม่เปลี่ยนมาสองทศวรรษ แปลว่านี่เป็นปัญหาเชิงโครงสร้าง ไม่ใช่ความผันผวนชั่วคราว ในชุดข้อมูลของเราเอง 84.5% ของ session จบลงโดยไม่มีการซื้อ ประเด็นคือร้านค้าไล่ดูทุก session ที่เสียไปด้วยมือไม่ได้ ทรัพยากรที่ขาดแคลนจริง ๆ คือเวลาของ analyst และนั่นคือสิ่งที่เราตั้งใจแก้"

### Slide 3 — problem statement
"ผู้ใช้ของเราคือ conversion analyst ของร้านค้าออนไลน์ สถานการณ์คือมี session จำนวนมากที่จบโดยไม่ซื้อ แต่ตรวจสอบได้เพียงไม่กี่รายการ คำถามคือควรเริ่มดูอันไหนก่อน วัตถุประสงค์ของเราคือจัดอันดับ session ที่จบแล้วตามความน่าจะเป็นในการซื้อ โดยใช้พฤติกรรมการเข้าชมเท่านั้น เราวัดความสำเร็จจากการที่ผู้ซื้อจริงถูกรวมอยู่ในกลุ่มคะแนนสูง ใช้ average precision เป็นตัวชี้วัดหลัก เพราะมีเพียง 15.5% ที่ซื้อจริง ถ้าใช้ accuracy โมเดลที่ทายว่าไม่ซื้อทุกครั้งก็ได้คะแนนสูงโดยไม่มีประโยชน์ และขอระบุให้ชัดว่าอะไรอยู่นอกขอบเขต เราไม่ได้อธิบายสาเหตุที่ลูกค้าออก ไม่ได้รับประกันว่ารายได้จะเพิ่ม และยังทำงานแบบ real-time ไม่ได้"

### Slide 6 — deeper EDA
"จากการสำรวจข้อมูลเพิ่มเติม เราพบว่าผู้ที่ซื้อใช้เวลาบนหน้าสินค้านานกว่าประมาณสองเท่า ค่ามัธยฐาน 1,110 วินาที เทียบกับ 526 วินาที และมีสัญญาณการเลิกสนใจต่ำกว่าชัดเจน exit rate เฉลี่ย 1.96% เทียบกับ 4.55% ใน correlation heatmap จะเห็นว่า exit rate เป็นตัวแปรเชิงตัวเลขที่สัมพันธ์กับการซื้อมากที่สุด ที่ค่า −0.20 ส่วน bounce rate กับ exit rate สัมพันธ์กันเองสูงถึง 0.90 แปลว่าให้ข้อมูลซ้ำกันพอสมควร และเมื่อดูตามแหล่งที่มาของ traffic อัตราการซื้อต่างกันมาก ตั้งแต่ประมาณ 6% ถึง 27% ทั้งหมดนี้เป็นความสัมพันธ์ ไม่ใช่เหตุและผล"

### Slide 9 — PyCaret
"เราเชื่อมกับ tutorial ผ่าน workflow ของ PyCaret เริ่มจาก `setup` โดยเปิด `fix_imbalance` เพราะผู้ซื้อมีสัดส่วนน้อย ต่อด้วย `compare_models` ซึ่งรอบนี้เราไม่ได้เลือกแค่สามโมเดล แต่ให้เปรียบเทียบทั้งหมด 14 โมเดลที่ PyCaret มีให้ แล้วปิดท้ายด้วย `tune_model` และ `predict_model` ผลที่ได้ LightGBM นำที่ AUC 0.7732 ตามด้วย gradient boosting และ random forest ส่วน dummy baseline อยู่ที่ 0.5 ตามคาด เทียบกับฝั่ง scikit-learn ของเราที่ได้ 0.787 ถือว่าใกล้เคียงกัน ข้อสรุปจากสองเครื่องมือตรงกันคือไม่มีโมเดลไหนนำแบบชัดเจน"

### Slide 10 — the intervals
"จุดนี้สำคัญ เราไม่ได้ดูแค่ตัวเลขดิบ แต่ทำ bootstrap 2,000 ครั้งเพื่อหาช่วงความเชื่อมั่น ผลคือ tuned random forest นำอยู่ 0.0028 แต่ช่วงความเชื่อมั่น 95% อยู่ระหว่าง −0.008 ถึง +0.014 ซึ่งคร่อมศูนย์ และชนะเพียง 68% ของการสุ่มซ้ำ แปลว่าความต่างนี้ไม่มีนัยสำคัญทางสถิติ เราจึงไม่ประกาศว่าโมเดลไหนชนะ สิ่งที่พูดได้คือทุกโมเดลจริงชนะ baseline อย่างชัดเจน แต่ระหว่างกันเองแยกไม่ออก"

### Slide 11 — interpretation
"เราตรวจสอบว่าโมเดลใช้ตัวแปรไหนจริง ๆ ด้วย permutation importance บนชุดทดสอบ ผลที่ได้น่าสนใจและต้องพูดตามตรง ตัวแปรที่สำคัญที่สุดคือ Month ไม่ใช่พฤติกรรมการเข้าชม รองลงมาคือเวลาบนหน้าสินค้าและ exit rate การที่ Month มาเป็นอันดับหนึ่งแปลว่าโมเดลเรียนรู้ฤดูกาลของร้านค้าแห่งเดียวในปีเดียวไปด้วย ซึ่งเป็นข้อจำกัดที่เราค้นพบเองจากการตรวจสอบ และเป็นเหตุผลว่าทำไมขั้นตอนถัดไปอันดับแรกของเราคือการทดสอบกับข้อมูลช่วงเวลาอื่น"

### Slide 12 — improvement
"ในส่วนของการปรับปรุงโมเดล เราลอง grid search ปรับ hyperparameter ได้ AP เพิ่มขึ้นเพียง 0.002 ซึ่งจากสไลด์ก่อนหน้าเรารู้แล้วว่าอยู่ในระดับ noise แต่สิ่งที่ได้ผลจริงคือการปรับ threshold ค่า 0.5 เป็นค่าตั้งต้นที่ไม่เหมาะกับข้อมูลที่ไม่สมดุล เมื่อเราหาค่าที่ให้ F1 สูงสุดคือ 0.446 recall เพิ่มจาก 46.3% เป็น 62.3% และ F1 เพิ่มจาก 0.412 เป็น 0.444 โดยไม่ต้องเทรนใหม่เลย และอีกค่าหนึ่งคือ 0.607 ซึ่งตรงกับกำลังการตรวจสอบ 10% แรก"

### Slide 13 — the solution
"ขั้นตอนที่เสนอมีสี่ข้อ ให้คะแนนทุก session จัดอันดับ ดึงกลุ่มคะแนนสูงที่ไม่ซื้อออกมา แล้วนำไปตั้งสมมติฐานและทดสอบ ตัวเลขจริงจากชุดทดสอบคือ ถ้า analyst ตรวจ 50 session แรกตามคะแนน จะเจอผู้ซื้อจริง 25 ราย เทียบกับการสุ่มที่คาดว่าจะเจอประมาณ 8 ราย คิดเป็น 3.2 เท่า และใน 50 รายการนั้นมี 25 session ที่คะแนนสูงแต่ไม่ซื้อ ซึ่งคือ worklist ที่เป็นตัวผลิตภัณฑ์จริง สามขั้นตอนแรกทำงานได้แล้วในแอป ส่วนขั้นที่สี่ต้องใช้ข้อมูลเส้นทางผู้ใช้และการทดลองจริง"

### Slide 16 — contributions
Each member, five seconds: "ผม/ดิฉัน [ชื่อ] รหัส [ID] รับผิดชอบ [งาน]"

## Likely judge questions

**Why is your AUC only 0.79? Online notebooks get 0.93.** Because they keep `PageValues`, which is computed from revenue. We measured it: keeping it takes AP from **0.374 to 0.723**. We dropped it anyway — a score that good is a warning sign, not an achievement.

**Is the random forest really the best model?** No, and we tested rather than assumed. It leads by 0.0028, with a 95% interval of −0.008 to +0.014 that crosses zero, winning only 68% of resamples. **Our models are statistically indistinguishable.** All of them beat the baseline decisively.

**Why is `Month` the most important feature?** Seasonality is genuinely predictive here — November converts at 25.4%, February at 1.6%. But it means the model has partly learned one store in one year, which is why later-period validation is our first next step. We found this by checking, not by assuming.

**Did your tuning actually help?** Hyperparameter tuning added +0.002 AP, which is noise. **Threshold tuning was the real improvement:** 0.5 to 0.446 lifted recall from 46.3% to 62.3% and F1 from 0.412 to 0.444, at no training cost.

**Why 14 models in PyCaret but 5 in scikit-learn?** PyCaret's `compare_models` is a fast, broad sweep on its own split — good for confirming nothing was missed. The scikit-learn experiment is the controlled one: one split, every model scored once on the same untouched test set. They agree.

**Why not accuracy?** The no-purchase baseline is 84.4% accurate and finds zero buyers. Purchases are 15.6% of rows, so we use average precision.

**Can you run it live while someone is browsing?** Not yet — these are completed-session aggregates. A live version needs timestamped partial sessions and prospective validation.

**Does it increase revenue?** Unproven, and we do not claim it. It prioritises investigation. A controlled A/B test would be needed to estimate revenue effect.

**What is "Operating System 3"?** Unknown — the publishers anonymised those codes. The model can still use them, because what matters is that code 3 behaves differently from code 2, not what it is called.

## Before you present

**Both modes:**
- [ ] Contribution table matches what each person actually did.
- [ ] Each member can explain their own section without reading the slide.
- [ ] One full timed run-through lands at 14:00 ± 30s.
- [ ] All 17 slides render; `eda.png`, `eda_detail.png` and `importance.png` all appear.
- [ ] App opens and both demo tabs work: `.venv/bin/streamlit run app.py`
- [ ] `SessionSignal_slides.pdf` saved as a fallback.

**If recording a video:**
- [ ] Slides in one tab, app in another; pre-select example 27.
- [ ] Record 1920x1080, microphone plus system audio (OBS or QuickTime).
- [ ] **Do not speed up the footage** — the rubric requires 1x speed.
- [ ] Upload **Unlisted or Public**, never Private. Names and IDs in the description.

**If presenting live:**
- [ ] Test the room laptop: deck opens, app runs, resolution does not clip the slides.
- [ ] Carry the PDF and a screen recording of a working demo on a USB stick.
- [ ] Agree who drives the laptop and where the handovers happen.
- [ ] Confirm port 8501 is free on the venue machine.

## Sources

- [Assignment notebook and rubric](https://colab.research.google.com/drive/1pys5EpelJBWDcHZNxpeUcDDybJnLbYTV)
- [eMarketer](https://www.emarketer.com/content/ecommerce-account-more-than-20--of-worldwide-retail-sales-despite-slowdown): global retail ecommerce $6.42T in 2025, 20.5% of retail.
- [Baymard Institute](https://baymard.com/lists/cart-abandonment-rate): 70.22% cart abandonment, unweighted average of 50 studies 2006–2025, range 55–84%.
- [UCI dataset 468](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset): 12,330 source rows; 12,205 after duplicate removal; 9,764 train / 2,441 test.
- [PyCaret tutorials](https://pycaret.gitbook.io/docs/get-started/tutorials). Saved sweep: `artifacts/pycaret_leaderboard.csv`.
- All model numbers come from `artifacts/results.json`, regenerated by `python train.py`.
