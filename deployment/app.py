import streamlit as st
from audio_classifier import AudioClassifier
from whisper_transcriber import WhisperTranscriber
from hand_movement_analyzer import HandMovementAnalyzer
from eye_contact_detector import EyeContactDetector
import os

# Main Page Configuration
st.set_page_config(page_title="Interview Automation System", page_icon="🔍", layout="wide")

# Custom CSS to Hide Default Streamlit Header, Footer, and Multipage List
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;} /* Hides the hamburger menu */
    header {visibility: hidden;} /* Hides the Streamlit header */
    footer {visibility: hidden;} /* Hides the Streamlit footer */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
selected = st.sidebar.radio(
    "Go to",
    options=["Main Page", "About Us", "FAQs", "Contact Us", "AI Processing"]
)

# Navigation Logic
if selected == "Main Page":
    from pages.main import main_page
    main_page()

elif selected == "About Us":
    from pages.about import about_page
    about_page()

elif selected == "FAQs":
    from pages.faqs import faqs_page
    faqs_page()

elif selected == "Contact Us":
    from pages.contact_us import contact_us_page
    contact_us_page()

elif selected == "AI Processing":
    # AI Processing Logic
    st.title("AI Processing Tasks")
    st.subheader("Upload a file to process AI tasks")

    uploaded_file = st.file_uploader("Choose a video file (MP4 format)", type=["mp4"])
    if uploaded_file is not None:
        st.write("Processing file...")

        # Save file locally for processing
        temp_file_path = "temp_video.mp4"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # AI Processing Tasks
        st.write("Running AI tasks...")
        results = {}

        try:
            # Task 1: Audio Classification
            st.write("Task 1: Audio Classification")
            classifier = AudioClassifier("./Models/distilhubert_stutter")
            results["audio_classification"] = classifier.classify(temp_file_path)

        except Exception as e:
            st.error(f"Audio Classification failed: {e}")

            '''try:
            # Task 2: Audio Transcription
            st.write("Task 2: Audio Transcription")
            transcriber = WhisperTranscriber("./Models/whisper_medium.pt")
            results["audio_transcription"] = transcriber.transcribe(temp_file_path)'''

        except Exception as e:
            st.error(f"Audio Transcription failed: {e}")

        try:
            # Task 3: Hand Movement Analysis
            st.write("Task 3: Hand Movement Analysis")
            analyzer = HandMovementAnalyzer(temp_file_path)
            results["hand_movement_analysis"] = analyzer.analyze_movement()

        except Exception as e:
            st.error(f"Hand Movement Analysis failed: {e}")

        try:
            # Task 4: Eye Contact Detection
            st.write("Task 4: Eye Contact Detection")
            detector = EyeContactDetector("./Models/eye_contact.pkl", device="cpu")
            eye_contact_results = detector.run(video_path=temp_file_path, target_fps=20)
            results["eye_contact_detection"] = eye_contact_results

        except Exception as e:
            st.error(f"Eye Contact Detection failed: {e}")

        # Display Results
        st.write("Processing Complete!")
        st.json(results)

        # Cleanup temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
