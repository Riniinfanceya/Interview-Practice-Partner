import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

st.set_page_config(page_title="Interview Practice Partner", layout="wide")

# -----------------------
# Helper Functions
# -----------------------

def convert_mp3_to_wav(mp3_path):
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    wav_path = mp3_path.replace(".mp3", ".wav")
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        text = "[Could not understand audio]"
    except sr.RequestError as e:
        text = f"[Recognition error: {e}]"
    return text

def agentic_response(user_text, role):
    if not user_text.strip():
        return "[No answer detected]", 0, "Please provide a valid response."

    # Role-specific keywords
    role_keywords = {
        "Engineer": ["python", "java", "c#", "project", "algorithm", "design"],
        "Sales": ["communication", "client", "negotiation", "lead", "target"],
        "Retail Associate": ["customer", "product", "inventory", "store", "sales"]
    }

    # Follow-up prompts per role
    follow_up = {
        "Engineer": "Can you elaborate on the technical details?",
        "Sales": "Could you give more examples of handling clients?",
        "Retail Associate": "Please describe specific customer interactions."
    }

    # Count relevant keywords
    keywords = role_keywords.get(role, [])
    relevance_score = sum(1 for k in keywords if k.lower() in user_text.lower())
    relevance_score = min(5, relevance_score)  # max 5 points

    # Communication score (short = low, detailed = high)
    comm_score = min(5, len(user_text.split()) / 2)  # max 5 points

    # Total score out of 10
    score = int(comm_score + relevance_score)

    # Feedback
    feedback = []
    if len(user_text.split()) < 3:
        feedback.append("Try giving more detailed responses.")
    if relevance_score == 0:
        feedback.append(f"Your answer is generic. Include {role}-related points.")
    else:
        feedback.append("Good job mentioning relevant role-specific points!")

    # Follow-up for short answers
    response = follow_up.get(role, "Please elaborate a bit more.")
    if len(user_text.split()) >= 8:
        response = "Good, let's move to the next question."

    return response, score, " | ".join(feedback)

# -----------------------
# Role-Based Questions
# -----------------------
role_questions = {
    "Engineer": [
        "Can you describe your most recent project?",
        "What programming languages are you most comfortable with?",
        "Explain a technical challenge you faced and how you solved it."
    ],
    "Sales": [
        "Tell me about a time you successfully closed a deal.",
        "How do you handle rejection from a client?",
        "Describe your strategy for meeting sales targets."
    ],
    "Retail Associate": [
        "How do you handle difficult customers?",
        "Describe a time you went above and beyond for a customer.",
        "How do you manage inventory effectively?"
    ]
}

# -----------------------
# Streamlit UI
# -----------------------

st.title("🎤 Interview Practice Partner")

# Demo Persona selection
demo_persona = st.selectbox("Choose Demo Persona", ["Confused User", "Efficient User", "Chatty User", "Edge Case User"])
st.session_state.demo_persona = demo_persona

# Role selection
role = st.selectbox("Choose Interview Role", ["Engineer", "Sales", "Retail Associate"])

# Initialize session state
if "qn_index" not in st.session_state:
    st.session_state.qn_index = 0
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Current question
current_qn_list = role_questions[role]

# Check if interview ended
if st.session_state.qn_index >= len(current_qn_list):
    persona_name = st.session_state.demo_persona if "demo_persona" in st.session_state else "Demo User"
    st.success(f"🎉 End of Interview for {persona_name}. You can restart the session below.")
    if st.button("Restart Interview"):
        st.session_state.qn_index = 0
        st.session_state.last_response = ""
        st.experimental_rerun()
else:
    current_qn = current_qn_list[st.session_state.qn_index]
    st.markdown(f"**Question:** {current_qn}")

    # Tabs: Text or Voice
    tab1, tab2 = st.tabs(["💬 Text Input", "🎤 Voice Input"])

    # ---------------- Text Input ----------------
    with tab1:
        user_text = st.text_area("Type your answer here:")

        if st.button("Submit Answer (Text)"):
            if user_text.strip():
                answer, score, feedback = agentic_response(user_text, role)
                st.session_state.last_response = f"Agentic Response: {answer}\nScore: {score}/10\nFeedback: {feedback}"
                st.success(st.session_state.last_response)

                # Move to next question
                st.session_state.qn_index += 1
                st.experimental_rerun()
            else:
                st.warning("Please type your answer.")

    # ---------------- Voice Input ----------------
    with tab2:
        uploaded_file = st.file_uploader("Upload MP3/WAV file", type=["mp3", "wav"])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Convert MP3 → WAV
            if tmp_path.endswith(".mp3"):
                tmp_path = convert_mp3_to_wav(tmp_path)

            st.audio(tmp_path, format="audio/wav")

            if st.button("Submit Answer (Voice)"):
                transcript = transcribe_audio(tmp_path)
                st.success(f"Transcribed Text: {transcript}")
                answer, score, feedback = agentic_response(transcript, role)
                st.session_state.last_response = f"Agentic Response: {answer}\nScore: {score}/10\nFeedback: {feedback}"
                st.success(st.session_state.last_response)

                # Move to next question
                st.session_state.qn_index += 1
                st.experimental_rerun()

# Display last response so it doesn’t disappear
if st.session_state.last_response:
    st.success(st.session_state.last_response)

st.markdown("---")
st.caption("Offline transcription powered by SpeechRecognition + Sphinx. Fully offline, role-aware, and demo-ready.")


