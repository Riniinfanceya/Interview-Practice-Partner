PROJECT TITLE : Interview Practice Partner

An AI-powered interview practice agent that helps users prepare for job interviews using **offline voice and text input**. It conducts role-specific mock interviews, asks follow-up questions, and provides feedback with scoring.

-----------------------------------------------------------------------------------------------------------------------------

Features :

- Role-based interviews: Engineer, Sales, Retail Associate
- Voice input (offline) using SpeechRecognition + PocketSphinx
- Text input supported
- Agentic behavior: asks follow-up questions based on user responses
- Post-interview feedback: communication, technical knowledge, role-specific points
- Handles multiple demo personas:
  - Confused User
  - Efficient User
  - Chatty User
  - Edge Case User
- Session restart functionality

-----------------------------------------------------------------------------------------------------------------------------

Setup Instructions :

1. Clone the repository :

=>git clone https://github.com/Riniinfanceya/Interview-Practice-Partner.git

=>cd Interview-Practice-Partner

=>Create and activate a virtual environment:
        python -m venv venv
        venv\Scripts\activate

2. Install dependencies :

=>pip install -r requirements.txt

=>pocketsphinx and pydub are installed for offline voice transcription.

=>Run the app:
        streamlit run app.py

3. Usage :

=>Select the interview role

=>Answer questions via text or voice

=>Agent provides score, feedback, and follow-up questions

=>Restart the session using the "Restart Interview" button

-----------------------------------------------------------------------------------------------------------------------------

Architecture Notes :

=>Frontend: Streamlit for UI and interaction

=>Backend: Python logic for question handling, scoring, and feedback

=>Offline Speech Recognition: PocketSphinx via speech_recognition

=>Audio Handling: pydub for MP3 → WAV conversion

=>Session Management: st.session_state tracks question index and last response

=>Agentic Logic:
⦁	 Role-specific keyword relevance scoring
⦁	 Communication scoring based on answer length
⦁	 Follow-up questions triggered for short or incomplete answers

-----------------------------------------------------------------------------------------------------------------------------

Design Decisions :

=>Offline-first approach: avoids API dependency and ensures the demo works without internet.

=>Role-based question sets: allows realistic mock interviews for different user personas.

=>Agentic scoring: evaluates both technical relevance and communication quality.

=>Voice + Text support: ensures flexibility and better demo experience.

=>Persona handling: tests conversational adaptability for Confused, Efficient, Chatty, and Edge Case users.

-----------------------------------------------------------------------------------------------------------------------------

Demo Personas :

Persona	Expected Behavior ->    	      Agent Response->                          Example

Confused User->	                Gives short/vague answers->            Agent asks for elaboration

Efficient User->	              Gives concise answers->                Agent proceeds to next question smoothly

Chatty User->	                  Gives long/off-topic answers->	        Agent provides feedback about focus and relevance

Edge Case->	                    Empty input or gibberish->	            Agent asks for valid input

-----------------------------------------------------------------------------------------------------------------------------




