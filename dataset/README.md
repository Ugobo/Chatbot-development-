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
Per source: {'rules': 15, 'local': 32, 'people': 24, 'written': 106, 'unmatched': 3}
people: 24 of at least 20
Labels not in INTENTS: []
Duplicates: []
Conflicting labels: []
Balance, largest / smallest: 1.0
