import torch

class WhisperTranscriber:
    def __init__(self, model_path, device="cpu"):
        """
        Initialize the WhisperTranscriber with a locally saved model.
        
        Args:
            model_path (str): Path to the locally saved Whisper model.
            device (str): Device to run the model on ("cpu" or "cuda").
        """
        self.model_path = model_path
        self.device = device
        self.model = self._load_model()

    def _load_model(self):
        """
        Load the Whisper model from the specified path on the specified device.
        
        Returns:
            model: The loaded Whisper model.
        """
        model = torch.load(self.model_path, map_location=self.device)
        model = model.to(self.device)
        model.eval()
        return model

    def transcribe(self, audio_file_path):
        """
        Transcribe an audio file using the loaded Whisper model.
        
        Args:
            audio_file_path (str): Path to the audio file.
            
        Returns:
            dict: Transcription results including language and text.
        """
        result = self.model.transcribe(audio_file_path)
        return result

    def print_transcription(self, result):
        """
        Print the transcription results in a readable format.
        
        Args:
            result (dict): The transcription result.
        """
        print("Detected Language:", result["language"])
        print("Transcribed Text:")
        print(result["text"])
