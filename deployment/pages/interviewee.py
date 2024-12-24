import streamlit as st
from pymongo import MongoClient
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase
import av
import gridfs
import os

# MongoDB Configuration
MONGO_URI = "mongodb+srv://lshayikhah:0IPDJsxf5tkxKNIj@cluster0.dahg8.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["interview_system"]
users_collection = db["users"]
interviews_collection = db["interviews"]
fs = gridfs.GridFS(db)

# Main Page Configuration
st.set_page_config(page_title="Interviewee Portal", page_icon="🔍", layout="wide")

# Directory to save temporary recordings
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Helper Functions
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password, "role": "interviewee"})
    return user is not None

def create_account(username, password):
    if users_collection.find_one({"username": username}):
        return False
    users_collection.insert_one({"username": username, "password": password, "role": "interviewee"})
    return True

class VideoRecorder(VideoProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        self.frames.append(frame)
        return frame

    def save_recording(self, filename):
        if self.frames:
            with av.open(filename, mode="w", format="mp4") as container:
                stream = container.add_stream("h264", rate=30)
                stream.width = self.frames[0].width
                stream.height = self.frames[0].height
                stream.pix_fmt = "yuv420p"
                for frame in self.frames:
                    container.mux(frame.to_image().to_ndarray())

def process_recording(file_path):
    # Mock processing logic, to give a taste of how it works.. we had issues with recording and soring the video files
    return {
        "audio_classification": "Clear Speech",
        "audio_transcription": "Mock transcription result",
        "hand_movement_analysis": {"movement_rate": "Moderate"},
        "eye_contact": "Good"
    }

def start_interview_page(interview):
    st.title(f"Interview ID: {interview['_id']}")
    st.subheader(f"Date: {interview['date']} | Time: {interview['time']}")

    # Split the screen into two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Webcam")
        # Webcam Recorder
        webrtc_ctx = webrtc_streamer(
            key=f"webrtc_{interview['_id']}",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoRecorder,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True,
        )

        if webrtc_ctx.video_processor:
            if st.button("Stop Recording"):
                # Save recording locally
                filename = os.path.join(RECORDINGS_DIR, f"{interview['_id']}.mp4")
                webrtc_ctx.video_processor.save_recording(filename)

                # Upload to MongoDB GridFS
                with open(filename, "rb") as video_file:
                    file_id = fs.put(video_file, filename=f"{interview['_id']}.mp4")

                # Process the recording
                results = process_recording(filename)

                # Save results in MongoDB
                interviews_collection.update_one(
                    {"_id": interview["_id"]},
                    {
                        "$set": {
                            "recording_id": str(file_id),
                            "processing_results": results,
                        }
                    },
                )
                st.success("Interview completed and processed successfully!")
        else:
            st.write("Press 'Start' to begin recording.")

    with col2:
        st.subheader("Interview Questions")
        for idx, question in enumerate(interview.get("questions", []), start=1):
            st.markdown(f"**Q{idx}: {question}**")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "dashboard"

def dashboard_page():
    st.title(f"Welcome, {st.session_state['username']}")

    # Scheduled Interviews Section
    st.subheader("Scheduled Interviews")
    interviews = list(interviews_collection.find({"interviewee": st.session_state["username"]}))

    if len(interviews) > 0:
        for interview in interviews:
            st.markdown(f"- **Interview ID:** {interview['_id']} | **Due Date:** {interview['date']} | **DueTime:** {interview['time']}")
            if st.button(f"Start Interview {interview['_id']}", key=f"start_{interview['_id']}"):
                st.session_state["current_interview"] = interview
                st.session_state["page"] = "interview"
    else:
        st.write("No interviews scheduled.")

    # Logout Button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["page"] = "login"

def login_signup_page():
    st.title("Interviewee Page")
    tab = st.tabs(["Login", "Sign-Up"])

    # Login Tab
    with tab[0]:
        st.subheader("Login")
        username = st.text_input("National ID", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("Login")

        if login_btn:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["page"] = "dashboard"
            else:
                st.error("Invalid National ID or password")

    # Sign-Up Tab
    with tab[1]:
        st.subheader("Sign-Up")
        new_username = st.text_input("National ID", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        signup_btn = st.button("Sign-Up")

        if signup_btn:
            if new_password == confirm_password:
                if create_account(new_username, new_password):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("National ID already exists.")
            else:
                st.error("Passwords do not match.")

# Main Logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "current_interview" not in st.session_state:
    st.session_state["current_interview"] = None

if not st.session_state["authenticated"]:
    login_signup_page()
else:
    if st.session_state["page"] == "dashboard":
        dashboard_page()
    elif st.session_state["page"] == "interview":
        start_interview_page(st.session_state["current_interview"])
