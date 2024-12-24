import cv2
import mediapipe as mp
import numpy as np


class HandMovementAnalyzer:
    def __init__(self, video_path, device="cpu"):
        """
        Initialize the HandMovementAnalyzer with the path to a video file.
        
        Args:
            video_path (str): Path to the video file.
            device (str): Device to run the analysis on ("cpu" or "gpu").
                          Note: MediaPipe Hands only runs on CPU by default.
        """
        self.video_path = video_path
        self.device = device  # Added for consistency, MediaPipe runs on CPU by default
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def analyze_movement(self):
        """
        Analyze hand movement in the video and classify movement level.
        
        Returns:
            dict: Analysis results including total movement, video duration, movement rate, and status.
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError("Error: Could not open video file.")

        # Initialize variables for tracking
        total_movement = 0
        previous_positions = {}
        frame_count = 0

        # Get video duration
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / fps  # Duration in seconds

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Convert the BGR frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Hands
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Track the index finger tip (landmark 8)
                    height, width, _ = frame.shape
                    index_finger_tip = hand_landmarks.landmark[8]
                    current_position = (int(index_finger_tip.x * width), int(index_finger_tip.y * height))

                    # Calculate movement
                    if hand_id in previous_positions:
                        prev_position = previous_positions[hand_id]
                        movement = np.linalg.norm(np.array(current_position) - np.array(prev_position))
                        total_movement += movement

                    # Update the previous position
                    previous_positions[hand_id] = current_position

        cap.release()

        # Calculate movement rate (movement per second)
        movement_rate = total_movement / video_duration

        # Classify movement
        if movement_rate < 100:
            movement_status = "Less Than Normal"
        elif 100 <= movement_rate <= 1000:
            movement_status = "Normal"
        else:  # movement_rate > 1000
            movement_status = "More Than Normal"

        return {
            "total_movement": total_movement,
            "video_duration": video_duration,
            "movement_rate": movement_rate,
            "movement_status": movement_status
        }
