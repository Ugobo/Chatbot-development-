
# Assignment 5: Library Chatbot v2
Course: AITCD001 Chatbots Development  
Student Name: Ugobo Eteng  

---

## Overview
This assignment upgrades the Assignment 4 library chatbot using three Week 5 techniques:
1. A Router of Handler Functions: Mapping intents to dedicated Python handler functions.
2. Several Requests in One Message:** Splitting messages on connectors (`and`, `but`, `also`, `then`, `?`), routing each piece, and assembling responses (with questions placed last).
3. Memory Across Turns:** Storing user names and last-intent contexts, enabling follow-up shorthand (e.g., *"and for 10 days?"*) and seamless side questions during a multi-turn study room booking flow.

---

## Part B Measurement Figures
Running the test set evaluation in Section 10 produced the following metrics:
* **One tag per message (Assignment 4): 32 of 35
* **Routed (Assignment 5): 33 of 35

---

## Part D: Test Conversations

### Provided Test Set (Conversations 1–8)
1. Two requests joined by "and":** Both hours and printing prices answered in order. (Pass)
2. One request that matches two intents:** Only the renewal reply was given due to table precedence. (Pass)
3. The question goes last:** Opening hours provided first, followed by the booking prompt. (Pass)
4. Remembering a name:** Acknowledged name (`Grace`) and used it in the exit greeting. (Pass)
5. A follow-up with no intent of its own: Correctly computed the 3-day fine and followed up with the 10-day fine using context. (Pass)
6. A side question during a booking: Answered the closing time query and successfully resumed the room booking flow. (Pass)
7. Two questions with no connecting word:Failed because the lack of a connector kept them as a single string. (Fail — Expected)
8. An answer that is also a question: Failed due to state machine interruption when a side question was embedded inside a booking step. (Fail — Expected)*

### Student-Designed Tests (Conversations 9 & 10)
9. Memory Test:**
Turns:`["my name is ugobo", "how many books can i take", "bye"]`
Expected Behaviour: Acknowledges the name, states the borrowing limit, and says goodbye using `"Ugobo"`.
10. Breaking Test:
Turns: `["can i reserve a room", "maybe next week", "and how much are fines?"]`
Expected Behaviour: Disrupts the strict expected date/slot/size sequence of the room booking flow.

---

## Written Answers

1. Which test message from Assignment 4 does routing fix, and which still fail? Why can routing not fix those?
   Routing fixes messages containing multiple requests joined by connectors (e.g., *"how many books can i take and what are the fines"*). Messages like abbreviations (`"rnw my bk"`) or out-of-vocabulary rephrasings (`"can i extend my deadline"`) still fail because regex pattern matching relies on explicit keyword presence rather than semantic understanding.

2. For conversations 7 and 8: the cause of each failure, and the part of the chatbot responsible.
   Conversation 7 fails because two questions are written without a connecting word in `CONNECTORS`, causing `split_requests` to treat them as a single string, failing the regex table. Conversation 8 fails because answering with a side question inside a booking step interferes with the strict expected sequence of the booking flow state machine.

3. Choose one failure. What change would fix it, and could that change break a conversation that currently passes?
   To fix conversation 7, we could expand `CONNECTORS` or update `split_requests` to split on implicit boundaries or whitespace heuristics between intents. However, this change could break existing single-request queries that contain multiple words or stop words, incorrectly segmenting them into unintended multi-requests.

```
