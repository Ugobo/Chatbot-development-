# Assignment 8: Intent Dataset for Exam Attendance Tracker

This folder contains the intent dataset, splitting scripts, and quality verification report for the **Exam Attendance Tracker** chatbot developed for Portfolio Project 1.

---

## 1. Chatbot Overview
* **Chatbot Name:** Exam Attendance Tracker
* **Domain:** Academic examination management and student presence verification at the Independent University of Kigali (ULK).
* **Total Intents:** 6 (`sign_in`, `sign_out`, `check_status`, `venue_location`, `help`, `out_of_scope`)

---

## 2. Labelling Guidelines
To ensure consistency and accuracy when classifying messages, the following rules were established before labelling:
1. **One message, one label:** If a message contains two distinct requests, split it into separate entries first.
2. **Label the goal, not just keywords:** Asking *"Where do I sign in for my exam?"* is about finding the venue (`venue_location`), not the sign-in action itself.
3. **Arrival Action:** Any action regarding arriving or entering an exam hall is classified as `sign_in`.
4. **Departure Action:** Any action regarding leaving or finishing an exam session is classified as `sign_out`.
5. **Out of Scope:** System errors, general help, complaints, or external/non-exam queries must be marked as `out_of_scope`.
6. **Student Phrasing:** Keep the student's exact words as typed, including typos, SMS shorthand, and Kinyarwanda expressions.

---

## 3. Dataset Summary & Sources
The dataset consists of **180 total rows** (30 messages per label), perfectly balanced (balance score of `1.0`), ensuring robust representation across multiple input styles:
Total Rows: 180
Training Set: 144 rows (80%)
Test Set: 36 rows (20%)
Sources Breakdown:**
rules : 12 messages
people`: 30 messages (collected from real peers/classmates)
local : 30 messages (Kinyarwanda phrasing)
  * `written`: 84 messages
  * `unmatched`: 24 messages


## 4. Baseline Rules & Performance
Regex pattern matching rules were established for each intent to serve as the evaluation baseline for the test set:
* **Baseline Score:** **20 of 36 test messages correct**


5. Extracted Entities
Using spaCy with a custom `entity_ruler`, domain-specific entities were tracked across the dataset:
BUILDING`**: Exam halls and blocks (e.g., *block a*, *block b*, *hall a*, *hall b*)
DAY : Temporal indicators (e.g., *today*, *tomorrow*, *monday*, etc.)

6. Files Included
* `Assignment_8_Home_Intent_Dataset.ipynb`: The complete Google Colab notebook containing code, guidelines, quality reports, and evaluation splits.
* `intents.csv`: The finalized CSV file containing all 180 labelled dataset entries split into training and test partitions.
