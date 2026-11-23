# ULK Exam & Registry Desk — Telegram Chatbot

An NLP-powered academic registry assistant for undergraduate students at the Independent University of Kigali (ULK), deployed on Telegram (`@ulk_exam_registry_2026_bot`). It combines rule-based matching with a TF-IDF + Logistic Regression intent classifier (`intent_classifier.joblib`) to answer questions about exam timetables, clearance/service fees, and transcript collection, as well as handle multi-step registry appointment bookings per chat session.

## On Telegram

| Item | Details |
| :--- | :--- |
| **The bot** | `@ulk_exam_registry_2026_bot` (ULK Exam & Registry Desk) |
| **Three classified intents** | 1. **`timetable`** — Phrasing missed by rules: `"time table"` (contains a space, whereas `\btimetables?\b` only matches one word). Caught by the classifier (`intent_timetable.png`).<br>2. **`fees`** — Phrasing missed by rules: `"hw mch 4 lost id replacement"` (SMS shorthand with no fee keywords). Caught by the classifier (`intent_fees.png`).<br>3. **`book`** — Phrasing missed by rules: `"ndashaka gufata gahunda ku ishuri"` (Kinyarwanda phrasing using `gahunda` instead of English `appointment`/`book`). Caught by the classifier (`intent_book.png`). |
| **The fallback** | Sent out-of-scope messages `"where is the campus cafeteria"` and `"Social security"`; the bot triggered the fallback (`"Sorry, I did not understand..."`) and escalated to `'human'` on the second consecutive miss (`fallback.png`). |
| **Two chats** | Tested two separate Telegram sessions simultaneously (`two_chats.png`), confirming that each `chat_id` maintains independent `flow` and `context` memory (e.g., remembering `"Ugobo"` in one chat while running an appointment booking flow in the other). |
| **Threshold** | `0.25` (chosen in Part 1). On Telegram, phrasings scoring at or above `0.25` were routed to their respective handlers, while out-of-scope queries either matched `out_of_scope` or scored below `0.25` and fell cleanly to the fallback. |
| **One thing that failed** | Sending `"No"` outside an active booking flow (or a single-word typo like `"cancle"`) triggered the fallback instead of cancelling, because `NO` is only checked when `flow["step"] == "confirm"`, and short typos/single words fall below the `0.25` threshold or classify as `out_of_scope`. |

## Files in This Folder

* `README.md` — Project overview and Telegram test summary.
* `Portfolio_Project_2_Part_2_Telegram.ipynb` — Complete notebook integrating the ULK chatbot, intent classifier, and `python-telegram-bot` handlers.
* `intent_classifier.joblib` — Trained TF-IDF (`char_wb` 2–4 n-grams) + Logistic Regression intent classifier.
* `*.png` — Screenshots demonstrating classified intents, fallback handling, and concurrent multi-chat sessions on Telegram.
