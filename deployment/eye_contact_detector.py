import cv2
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict
import mediapipe as mp


class EyeContactDetector:
    def __init__(self, model_path, device="cpu"):
        """
        Initialize the EyeContactDetector with a locally saved model.
        
        Args:
            model_path (str): Path to the trained model file.
            device (str): Device to run the model on ("cpu" or "cuda").
        """
        self.device = device
        self.model = self._load_model(model_path)
        self.class_counts = defaultdict(int)
        self.total_frames = 0

        # Initialize MediaPipe Holistic (CPU)
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils

    def _load_model(self, model_path):
        """Load the model from the specified path."""
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    def process_frame(self, frame, holistic):
        self.total_frames += 1

        # Convert frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = holistic.process(rgb_frame)

        # Extract landmarks and perform prediction
        try:
            pose = results.pose_landmarks.landmark
            face = results.face_landmarks.landmark

            # Flatten pose and face landmarks into a feature vector
            pose_row = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in pose]).flatten().tolist()
            face_row = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in face]).flatten().tolist()

            row = pose_row + face_row
            X = pd.DataFrame([row])

            # Predict class and probabilities
            body_language_class = self.model.predict(X)[0]
            body_language_prob = self.model.predict_proba(X)[0]

            # Update class counts
            self.class_counts[body_language_class] += 1

        except Exception as e:
            print(f'Error during prediction: {e}')

        return frame  # Return the frame for display

    def start_detection(self, cap, target_fps=20):
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get the original video FPS
        frame_skip = max(1, int(video_fps / target_fps))  # Calculate frame skip

        print(f"Original video FPS: {video_fps}. Processing every {frame_skip} frame(s) for {target_fps} FPS.")

        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            frame_count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Skip frames to match target FPS
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue

                frame_count += 1

                # Process the selected frame
                processed_frame = self.process_frame(frame, holistic)

                # Display the processed frame
                cv2.imshow('Eye Contact Detector (20 FPS)', processed_frame)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def run(self, video_path, target_fps=20):
        cap = cv2.VideoCapture(video_path)
        self.start_detection(cap, target_fps=target_fps)

    def print_summary(self):
        for class_name, count in self.class_counts.items():
            percentage = (count / self.total_frames) * 100
            print(f'{class_name}: {percentage:.2f}%')
