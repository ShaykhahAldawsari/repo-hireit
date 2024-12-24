import streamlit as st
from eye_contact_detector import EyeContact
from hand_movement_analyzer import HandMovementAnalyzer
from whisper_transcriber import WhisperTranscriber
from audio_classifier import AudioClassifier
import pandas as pd

# Main Page Configuration
st.set_page_config(page_title="HIREiT Beta - Analysis System", page_icon="⚙️", layout="wide")

# HIREiT Beta Functionality
def hireit_beta(video_path, transcriber_model_path, audio_model_path, eye_contact_model_path):
    results_summary = []

    # Whisper Transcriber
    try:
        transcriber = WhisperTranscriber(transcriber_model_path)
        transcription_result = transcriber.transcribe(video_path)
        detected_language = transcription_result["language"]
        transcribed_text = transcription_result["text"]
        results_summary.append(f"- The answers: {transcribed_text}")
        st.write(f"Detected Language: {detected_language}")
        st.write(f"Transcribed Text: {transcribed_text}")
    except Exception as e:
        st.error(f"Error in Whisper Transcriber: {e}")

    # Hand Movement Analyzer
    try:
        hand_analyzer = HandMovementAnalyzer(video_path)
        movement_analysis = hand_analyzer.analyze_movement()
        st.write("Hand Movement Analysis:")
        st.write(f"Total Movement: {movement_analysis['total_movement']:.2f}")
        st.write(f"Video Duration: {movement_analysis['video_duration']:.2f}s")
        st.write(f"Movement Rate: {movement_analysis['movement_rate']:.2f}")
        st.write(f"Status: {movement_analysis['movement_status']}")
        results_summary.append(f"- Status: {movement_analysis['movement_status']}")
    except Exception as e:
        st.error(f"Error in Hand Movement Analyzer: {e}")

    # Eye Contact Detector
    try:
        st.write("Initializing EyeContact...")
        eye_contact_detector = EyeContact(model_path=eye_contact_model_path, video_source=video_path)
        st.write("EyeContact initialized successfully.")

        # Run the eye contact detector
        summary, results = eye_contact_detector.run()
        st.write(f"Run Output: Summary={summary}")

        contact_percentage = summary.get('eye_contact', 0)  # Example feature: eye contact percentage

        results_summary.append(f"- Eye Contact: {contact_percentage:.2f}%")
    except Exception as e:
        st.error(f"Error in EyeContact Detector: {e}")

    # Audio Classifier
    try:
        audio_classifier = AudioClassifier(audio_model_path)
        predicted_labels = audio_classifier.classify(video_path)
        audio_classifier.print_results(predicted_labels)
        non_stutter_label = next((label for label in predicted_labels if label["label"] == "nonstutter"), None)
        if non_stutter_label:
            non_stutter_score = non_stutter_label["score"] * 100
            results_summary.append(f"- Non stutter {non_stutter_score:.0f}%")
    except Exception as e:
        st.error(f"Error in Audio Classifier: {e}")

    # Display Results
    st.write("\nFinal Combined Results:")
    st.write("\n".join(results_summary))

# Streamlit Interface for HIREiT Beta
def hireit_beta_page():
    st.title("HIREiT Beta - Analysis System")

    st.markdown("Upload a video file for analysis:")

    video_file = st.file_uploader("Upload Video", type=["mp4"])

    if video_file is not None:
        video_path = "temp_video.mp4"

        # Save uploaded file to disk
        with open(video_path, "wb") as f:
            f.write(video_file.read())

        # Define model paths
        transcriber_model_path = "../Models/whisper_medium.pt"
        audio_model_path = "../Models/distilhubert_stutter"
        eye_contact_model_path = "../Models/eye_contact.pkl"

        # Run HIREiT Beta Analysis
        hireit_beta(video_path, transcriber_model_path, audio_model_path, eye_contact_model_path)

# Display the HIREiT Beta Page
hireit_beta_page()
