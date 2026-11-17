# ULK Exam & Registry Desk

A rule-based customer service assistant that helps undergraduate students at the Independent University of Kigali (ULK) check exam timetables, look up clearance and document fees, review transcript procedures, and book Academic Registry appointments.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ugobo/Chatbot-development-/blob/main/week%207/ulk_exam_desk_chatbot.ipynb)

![A conversation with the ULK Exam & Registry Desk chatbot](Screenshot%20.png.png)

## The problem it solves

Undergraduate students at the Independent University of Kigali (ULK) frequently need quick answers about exam schedules, clearance charges, provisional transcript collection, and Academic Registry appointment slots. Without this chatbot, students must walk to Block B (Room 104) or queue at the registry desk just to ask routine questions before knowing what fees to pay via Irembo or BK. This chatbot provides instant 24/7 answers in English and Kinyarwanda and lets students reserve a registry slot in advance.

## What it can do

| Intent | A customer might type | The chatbot replies |
| :--- | :--- | :--- |
| `greeting` | `muraho` / `hello` | Greets the student by name (if known) and lists the four services the assistant can help with. |
| `name` | `my name is ugobo` | Remembers the student's name for the rest of the conversation (`Nice to meet you, Ugobo.`). |
| `timetable` | `when are exams` / `ibizamini ni ryari` | Gives the main exam schedule: Monday to Friday in Morning (`08:30–11:30`) and Afternoon (`14:00–17:00`) sessions. |
| `fees` | `how much is clearance` / `and transcript?` | Looks up the requested item in a `FEES` dictionary and returns the exact RWF amount and payment method (Irembo or BK). |
| `transcript` | `how do I get my transcript` / `amanota` | Explains that provisional transcripts are issued at the Academic Registry (Block B, Room 104) within 3 working days after clearance. |
| `book` | `book a transcript appointment` | Guides the student through a 3-step appointment booking flow (service, day, session) and asks for confirmation (`yes` / `yego`) before booking. |
| `cancel` | `cancel` / `call it off` | Stops an active appointment booking immediately without saving anything. |

## How it works

* **Recognising requests:** The chatbot checks a priority-ordered list of regular expression patterns (`RULES`). `name` and `cancel` are placed at the top so a user can always introduce themselves or abort a booking mid-way, and `book` is placed above `timetable`, `fees`, and `transcript` so a phrase like *"book a transcript appointment"* triggers the booking flow rather than general transcript information.
* **Answering:** Once `route()` splits a message on connectors (`and`, `but`, `also`, `then`, `?`) and matches each request to an intent tag, `respond()` looks up the matching function in the `HANDLERS` dictionary. `handle_fees()` reads the message against the `FEES` dictionary to calculate the exact fee for clearance (`5,000 RWF`), transcript (`10,000 RWF`), re-sit (`15,000 RWF`), or ID replacement (`3,000 RWF`), while replies that ask a question (`ASKS`) are placed last.
* **Conversation:** Starting a booking enters a 3-step guided flow (`FLOW_STEPS`: `service` → `day` → `session`) managed by `continue_flow()`. Invalid answers re-ask the current question, side questions (like asking for a fee mid-booking) are answered without losing progress, `cancel` aborts at any time, and nothing is booked until the user confirms with `yes` (`yego`).
* **Memory:** A `context` dictionary stores the user's `name`, their `last_intent` (so a follow-up like *"and transcript?"* continues the previous `fees` question), and consecutive `fallbacks`, alongside a `flow` dictionary tracking the current booking step and collected answers.
* **When things go wrong:** `validate()` rejects empty, punctuation-only, or overly long (>300 characters) messages before routing. Unrecognised inputs are recorded in `UNMATCHED` and count toward `fallbacks`—after two consecutive misunderstandings, the bot offers a human staff handover (`human` / `staff`). Any unexpected runtime error inside a handler is caught by `safe_handle()`, logged with a timestamp in `ERROR_LOG`, and replaced with a polite apology instead of crashing.

## Try it

1. Click **Open In Colab** at the top of this page.
2. Run the cells in order, from the top (**Runtime > Run all**).
3. Run the `chat()` cell (Step 11) on its own and type a question (type `bye` or `murakoze` to finish).

## Testing

Ten test conversations, written before they were run:

* **Passed:** 9 of 10 (initial run); 10 of 10 after Step 9 refinement.
* **The ones that failed, and why:**

| Conversation | What happened | Why |
| :--- | :--- | :--- |
| **Test 10:** `['book a transcript appointment']` | On the initial run, the bot either matched `transcript` instead of `book` or asked *"Which service do you need?"* even though `transcript` was already stated. | `transcript` appeared before `book` in `RULES`, and the initial `handle_book()` started at step `0` without checking whether the opening message already answered any `FLOW_STEPS` questions. |

## A bug found and fixed

* **What happened:** In Test 10 (`"book a transcript appointment"`), the chatbot failed to use the service already provided in the opening request and initially routed to the wrong intent.
* **What caused it:** `"transcript"` was ordered above `"book"` in `RULES`, and `handle_book()` always returned `start_flow()` without scanning the initial message for answers to `FLOW_STEPS`.
* **What was changed:** Moved `("book", ...)` above `"transcript"` in `RULES` (Step 2) and updated `handle_book(text)` in Step 9 with a `while` loop that checks each step's pattern against the incoming message and advances via `continue_flow(text)` whenever an answer is already present. Re-running Test 10 confirmed the bot skipped the service question and replied directly with *"Which day? Today or tomorrow?"*.

## Known limitations

Taken from the `UNMATCHED` log (`['asdfgh', 'qwerty', 'cancle']` — 1 of 6 real phrasings missed in Step 10):

* **`cancle` (misspellings and heavy SMS typos):** Common spelling mistakes like `cancle` instead of `cancel` do not match the `\bcancel\w*\b` word-boundary regex and fall into `UNMATCHED`.
* **Fixed booking windows:** Appointment slots only accept `today` or `tomorrow` and `morning` or `afternoon`, rather than specific calendar dates or exact hours.
* **In-memory session only:** Booked appointments are confirmed in chat only and are not saved to a persistent university database or calendar.

## What comes next

* Replace regex keyword matching with a trained machine learning intent classifier (such as TF-IDF + Logistic Regression or LinearSVC) to handle spelling variations like `cancle` and broader Kinyarwanda phrasing automatically.
* Connect the appointment booking confirmation to a SQLite database or Google Sheets/Telegram bot interface so registry staff can view booked student slots in real time.

## Built with

Python 3 · the `re` module · Google Colab

## About

Built by **UGOBO ETENG** for the Chatbots Development module (AITCD001), AI Technology Certification, United African Institute of Technology, Kigali. November 2026.
