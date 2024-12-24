from transformers import pipeline

class AudioClassifier:
    def __init__(self, model_path, device=-1):  # Default to CPU
        """
        Initialize the AudioClassifier with a locally saved model.
        
        Args:
            model_path (str): Path to the locally saved model.
            device (int): Device to run the model on (-1 for CPU, 0+ for GPU).
        """
        self.model_path = model_path
        self.model = pipeline("audio-classification", model=model_path, device=device)

    def classify(self, audio_file_path):
        """
        Classify an audio file using the preloaded model.
        
        Args:
            audio_file_path (str): Path to the audio file.
            
        Returns:
            list: A list of predicted labels with scores.
        """
        predicted_labels = self.model(audio_file_path)
        return predicted_labels

    def print_results(self, predicted_labels):
        """
        Print the classification results in a readable format.
        
        Args:
            predicted_labels (list): The classification results.
        """
        print("Predicted Labels:")
        for label in predicted_labels:
            print(f"Label: {label['label']}, Score: {label['score']:.4f}")
