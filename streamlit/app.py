import os
import re
import uuid
from datetime import datetime
import joblib
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- PAGE SETUP & PRIVACY NOTICE (Law N°058/2021) ---
st.set_page_config(page_title="ULK Exam & Registry Desk", page_icon="🎓")
st.title("🎓 ULK Exam & Registry Desk")
st.caption("Undergraduate Student Support — Independent University of Kigali (ULK)")
st.info(
    "**Notice (Law N°058/2021):** You are chatting with a computer program. "
    "Messages and feedback are recorded anonymously with a random session code to improve accuracy. "
    "Please do not enter your real name, phone number, or student ID number."
)

# --- PART 1: ULK DOMAIN RULES, HANDLERS & FLOW ---
BOT_NAME = "ULK Exam & Registry Desk"
USERS = "undergraduate students at the Independent University of Kigali (ULK)"
TOPICS = "exam timetables, clearance fees, transcript collection and booking a registry appointment"

RULES = [
    ("cancel", r"\bcancel\w*\b|\bcall it off\b|\bstop\b"),
    ("book", r"\bbook\w*\b|\bappointments?\b|\breserv\w*\b|\bregistry\b|\bslot\b"),
    ("timetable", r"\btimetables?\b|\bexam\w*\b|\bschedules?\b|\bwhat ?time\b|\bibizamini\b"),
    ("fees", r"\bfees?\b|\bclearance\b|\bprices?\b|\bcosts?\b|\bhow ?much\b|\bangahe\b"),
    ("transcript", r"\btranscripts?\b|\bresults?\b|\bgrades?\b|\bmarks?\b|\bamanota\b"),
]

FEES = {
    "clearance": "5,000 RWF",
    "transcript": "10,000 RWF",
    "re-sit": "15,000 RWF",
    "resit": "15,000 RWF",
    "id": "3,000 RWF",
}
FEE_ITEMS = r"\b(" + "|".join(FEES) + r")\b"
SERVICES = r"\b(clearance|transcript|re-sit|resit|id)\b"

FLOW_STEPS = [
    ("service", "Which service do you need? Clearance, transcript, resit, or ID?", SERVICES),
    ("day", "Which day? Today or tomorrow?", r"\b(today|tomorrow)\b"),
    ("session", "Morning or afternoon?", r"\b(morning|afternoon)\b"),
]

DONE = "Appointment booked: "
NOT_DONE = "No problem. No appointment has been booked."
YES = r"\b(yes|yeah|yego|correct|ok|okay)\b"
NO = r"\b(no|nope|oya|wrong)\b"
CONNECTORS = r"\band\b|\bbut\b|\balso\b|\bthen\b|[?]"
EXIT_WORDS = ("bye", "goodbye", "exit", "quit", "thanks", "murakoze")
HUMAN_WORDS = ("human", "staff", "agent", "person")

# --- PART 2: CLASSIFIER & THRESHOLD ---
THRESHOLD = 0.25
MODEL_PATH = os.path.join(os.path.dirname(__file__), "intent_classifier.joblib")

@st.cache_resource
def load_classifier():
    return joblib.load(MODEL_PATH)

classifier = load_classifier()

def classify(text):
    scores = classifier.predict_proba([text])[0]
    best = scores.argmax()
    return str(classifier.classes_[best]), float(scores[best])

# --- PART 4: DOMAIN FACTS (RETRIEVER / RAG) ---
FAQ = [
    ("Payment", "All university fees (clearance, transcript, resit, ID) are paid via Irembo or Bank of Kigali (BK). Cash is not accepted at the registry."),
    ("Location", "The Academic Registry and Examination Office is located in Block B, Room 104, Gisozi Campus, open Monday to Friday 08:00 to 17:00."),
    ("Exam Card", "Students must present a valid ULK student ID and stamped financial clearance card 15 minutes before each examination."),
    ("Resit Policy", "Supplementary/re-sit exams are scheduled two weeks after provisional results are published on the student portal."),
    ("Graduation Clearance", "Final-year clearance requires sign-off from the Library, Finance Office, Dean of Faculty, and Academic Registry."),
]
MIN_SCORE = 0.20
finder = TfidfVectorizer(stop_words="english")
passage_vectors = finder.fit_transform([t + ". " + a for t, a in FAQ])

def retrieve(question):
    q = finder.transform([question])
    scores = cosine_similarity(q, passage_vectors)[0]
    best = scores.argmax()
    return float(scores[best]), FAQ[best][1]

# --- SESSION STATE ---
if "user_code" not in st.session_state:
    st.session_state.user_code = str(uuid.uuid4())[:8]
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "flow" not in st.session_state:
    st.session_state.flow = {"step": None, "collected": {}}
if "context" not in st.session_state:
    st.session_state.context = {"name": None, "last_intent": None, "fallbacks": 0}
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Muraho! I am the {BOT_NAME} assistant, a computer program. I can help with {TOPICS}.",
            "meta": None,
        }
    ]

flow = st.session_state.flow
context = st.session_state.context

def normalise(text):
    return re.sub(r"[^\w\s:]", "", text).lower().strip()

def split_requests(message):
    return [normalise(p) for p in re.split(CONNECTORS, message.lower()) if normalise(p)]

def match_rule(text):
    for tag, pattern in RULES:
        if re.search(pattern, text):
            return tag
    return None

def start_flow():
    flow["step"] = 0
    flow["collected"] = {}
    return FLOW_STEPS[0][1]

def reset_flow():
    flow["step"] = None
    flow["collected"] = {}

def continue_flow(message):
    text = normalise(message)
    if flow["step"] == "confirm":
        if re.search(YES, text):
            booked = ", ".join(flow["collected"].values())
            reset_flow()
            return DONE + booked + ". Thank you."
        if re.search(NO, text):
            reset_flow()
            return NOT_DONE
        return "Please answer yes or no."
    name, question, pattern = FLOW_STEPS[flow["step"]]
    found = re.search(pattern, text)
    if not found:
        return question
    flow["collected"][name] = found.group()
    flow["step"] += 1
    if flow["step"] < len(FLOW_STEPS):
        return FLOW_STEPS[flow["step"]][1]
    flow["step"] = "confirm"
    return "So: " + ", ".join(flow["collected"].values()) + ". Shall I book it? Yes or no."

def handle_timetable(text):
    return "Main exams run Monday to Friday in two sessions: Morning (08:30–11:30) and Afternoon (14:00–17:00)."

def handle_fees(text):
    found = re.search(FEE_ITEMS, text)
    if found:
        item = found.group(1)
        return f"The fee for {item} is {FEES[item]}, payable via Irembo or BK."
    return "Clearance is 5,000 RWF, Transcript is 10,000 RWF, Exam Re-sit is 15,000 RWF, and Student ID replacement is 3,000 RWF."

def handle_transcript(text):
    return "Provisional transcripts are issued at the Academic Registry (Block B, Room 104) within 3 working days after clearance."

def handle_book(text):
    if flow["step"] is not None:
        return "Your appointment booking is already under way."
    reply = start_flow()
    while flow["step"] != "confirm":
        pattern = FLOW_STEPS[flow["step"]][2]
        if not re.search(pattern, text):
            break
        reply = continue_flow(text)
    return reply

def handle_cancel(text):
    if flow["step"] is not None:
        reset_flow()
        return "Your appointment booking has been cancelled. Nothing was booked."
    return "There is no appointment booking in progress to cancel."

def handle_name(text):
    found = re.search(r"\bmy name is (\w+)", text)
    if found:
        context["name"] = found.group(1).capitalize()
        return f"Nice to meet you, {context['name']}."
    return "Sorry, I did not catch your name."

def handle_greeting(text):
    if context["name"]:
        return f"Muraho, {context['name']}! How can I help?"
    return f"Muraho! I am the {BOT_NAME} assistant, a computer program. I can help with {TOPICS}."

RULES_ALL = [("name", r"\bmy name is\b")] + RULES + [("greeting", r"\bhello\b|\bhi\b|\bhey\b|\bmuraho\b|\bmwaramutse\b|\bmwiriwe\b")]
HANDLERS = {
    "name": handle_name,
    "cancel": handle_cancel,
    "timetable": handle_timetable,
    "fees": handle_fees,
    "transcript": handle_transcript,
    "book": handle_book,
    "greeting": handle_greeting,
}

def match_all_rules(text):
    for tag, pattern in RULES_ALL:
        if re.search(pattern, text):
            return tag
    return None

def route_hybrid(message):
    found = []
    best_intent, best_score, source = "none", 0.0, "fallback"
    for req in split_requests(message):
        rule_tag = match_all_rules(req)
        if rule_tag:
            tag, intent, score, src = rule_tag, rule_tag, 1.0, "rules"
        else:
            intent, score = classify(req)
            if score >= THRESHOLD and intent != "out_of_scope":
                tag, src = intent, "classifier"
            else:
                tag, src = None, "fallback"
        best_intent, best_score, source = intent, score, src
        if tag in HANDLERS and tag not in [t for t, _ in found]:
            found.append((tag, req))
    return found, best_intent, round(best_score, 3), source

def reply_to(message):
    text = normalise(message)
    if not text:
        return f"Please type a question in words. I can help with {TOPICS}.", "validation", 1.0, "rules"
    if text in EXIT_WORDS:
        name = context["name"]
        reset_flow()
        st.session_state.context = {"name": None, "last_intent": None, "fallbacks": 0}
        msg = f"Thank you, {name}. Murakoze." if name else "Thank you for contacting us. Murakoze."
        return msg, "exit", 1.0, "rules"
    if text in HUMAN_WORDS:
        reset_flow()
        return "Connecting you to a member of staff. They can see this conversation.", "handover", 1.0, "rules"
    if flow["step"] is not None:
        step_before = flow["step"]
        flow_reply = continue_flow(message)
        if flow["step"] != step_before:
            return flow_reply, "book_flow", 1.0, "flow"
        found, intent, score, src = route_hybrid(message)
        if not found:
            return flow_reply, "book_flow", 1.0, "flow"
        answers = [HANDLERS[t](r) for t, r in found if t != "book"]
        return (" ".join(answers) + " " + flow_reply).strip(), intent, score, src

    found, intent, score, src = route_hybrid(message)
    if not found and context["last_intent"] == "fees" and re.search(FEE_ITEMS, text):
        found, intent, score, src = [("fees", text)], "fees", 1.0, "rules"
    if not found:
        r_score, passage = retrieve(text)
        if r_score >= MIN_SCORE:
            return passage, "faq", round(r_score, 3), "retriever"
        context["fallbacks"] += 1
        if context["fallbacks"] >= 2:
            return f"Sorry, I still did not understand. Type 'human' for a member of staff, or ask about {TOPICS}.", intent, score, "fallback"
        return f"Sorry, I did not understand. I can help with {TOPICS}.", intent, score, "fallback"

    context["fallbacks"] = 0
    context["last_intent"] = found[-1][0]
    answers = [HANDLERS[t](r) for t, r in found if t != "book"]
    questions = [HANDLERS[t](r) for t, r in found if t == "book"]
    return " ".join(answers + questions), intent, score, src

# --- PART 5 & 7: LOGGING TO GOOGLE SHEET + CHAT UI ---
def log_turn(row):
    log_url = st.secrets.get("LOG_URL", "")
    if not log_url:
        return True
    try:
        resp = requests.post(log_url, json=row, timeout=10)
        return resp.ok and resp.text.strip() == "ok"
    except Exception:
        return False

for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            m = msg["meta"]
            st.caption(f"answered by: **{m['answered_by']}** | intent: `{m['intent']}` ({m['confidence']})")
            col1, col2, _ = st.columns([1, 1, 10])
            if col1.button("👍", key=f"up_{idx}"):
                log_turn({**m, "feedback": "👍"})
                st.toast("Feedback saved (👍)")
            if col2.button("👎", key=f"dn_{idx}"):
                log_turn({**m, "feedback": "👎"})
                st.toast("Feedback saved (👎)")

if prompt := st.chat_input("Ask about exam timetables, fees, transcripts, or book a slot..."):
    st.session_state.turn += 1
    st.session_state.messages.append({"role": "user", "content": prompt, "meta": None})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply, intent, conf, answered_by = reply_to(prompt)
    row = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": st.session_state.user_code,
        "turn": st.session_state.turn,
        "message": prompt,
        "intent": intent,
        "confidence": conf,
        "answered_by": answered_by,
        "feedback": "",
    }
    saved = log_turn(row)
    if not saved:
        st.warning("Warning: this turn could not be saved to the log.")

    st.session_state.messages.append({"role": "assistant", "content": reply, "meta": row})
    with st.chat_message("assistant"):
        st.markdown(reply)
        st.caption(f"answered by: **{answered_by}** | intent: `{intent}` ({conf})")
