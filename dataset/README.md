# Intent dataset: ULK Exam & Registry Desk

*Assignment 8, the first stage of Portfolio Project 2, Part 1.*

## The labels

| Label | What it means | Messages |
|---|---|---|
| timetable | Asking for exam dates, times, schedules, or morning/afternoon sessions | 30 |
| fees | Asking for the cost or payment details of clearance, transcripts, resits, or ID replacement | 30 |
| transcript | Asking when, where, or how long it takes to collect a transcript or check exam results/marks | 30 |
| book | Requesting to schedule or reserve an appointment slot at the Academic Registry | 30 |
| cancel | Requesting to cancel, stop, or abort an existing or ongoing registry appointment booking | 30 |
| out_of_scope | Everything this chatbot does not answer (lost items, Wi-Fi, admissions, tuition, general campus queries) | 30 |

## The labelling guideline

1. One message, one label. If a message contains two separate requests, split it first.
2. Label the user's goal, not a single keyword: 'how much is a transcript' asks for price, so it is fees.
3. Any request to schedule, reserve, or get a slot at the registry is book, even if it names a service like transcript or clearance.
4. Asking when, where, or how long it takes to collect a transcript or check grades/marks is transcript.
5. Asking for exam dates, times, schedules, or sessions is timetable.
6. Complaints, lost student IDs/items, lecturer contacts, or general university admissions/news are out_of_scope.
7. Keep the student's exact words: preserve typos (like 'cancle'), SMS shorthand, and Kinyarwanda or mixed phrasing as typed.

## Where the messages come from

| Source | Rows |
|---|---|
| rules | 15 |
| unmatched | 3 |
| local | 32 |
| people | 24 |
| written | 106 |

## Quality check

```text
P## The classifier

### Features kept
* **Chosen feature representation:** Word TF-IDF (`TfidfVectorizer()`) with Logistic Regression.
* **Comparison:** Word features outperformed character n-grams (`analyzer="char_wb"`), achieving higher accuracy on the test split (previously **78%** vs. **75%** on the 180-row split) while keeping standard registry terms (`timetable`, `transcript`, `clearance`, `booking`) cleanly separated. *(Update the exact percentage if your 38-row test split output in Step 4 differed.)*

### Rules on the same test set
* **Rule baseline (`RULES` from Assignment 8):** **29 of 38** test messages right (**76.3%** accuracy), with the remaining 9 messages either falling through to `out_of_scope` (missed Kinyarwanda phrasing such as `hagarika gahunda nari nafashwe` and `kuraho gahunda yanjye`, or indirect queries like `i want to know my session`) or matching an overlapping keyword (`fata gahunda ya clearance` matching `fees` instead of `book`).
* **Classifier (`intent_classifier.joblib`):** Improves coverage on unseen phrasing and Kinyarwanda expressions without requiring manual regex updates for every phrasing variation.

### Weakest intent & why
* **Weakest intent:** `fees` (lowest F1 score on the initial 180-row dataset at **0.44** F1 / **0.33** recall).
* **Reason:** Fee questions share high-overlap words (`transcript`, `clearance`, `exam`, `id`) with `transcript`, `book`, and `out_of_scope` queries. To address this, 10 targeted `fees` examples covering student ID replacement costs, provisional transcript/retake fees, and Kinyarwanda cost phrasing (`ikiguzi`, `ndishyura`) were added, expanding the dataset to **190 rows** (**152 train / 38 test**).

### Chosen threshold & why
* **Chosen threshold:** **`0.35`** (`THRESHOLD = 0.35`).
* **Rationale:** Any prediction whose top probability is below `0.35` (or whose top label is `out_of_scope`) triggers the safe fallback response rather than risking a confident wrong answer on ambiguous or out-of-scope student messages (such as campus Wi-Fi, library hours, or tuition fee inquiries).er source: {'rules': 15, 'local': 32, 'people': 24, 'written': 106, 'unmatched': 3}
people: 24 of at least 20
Labels not in INTENTS: []
Duplicates: []
Conflicting labels: []
Balance, largest / smallest: 1.0
