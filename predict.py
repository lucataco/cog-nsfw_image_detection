# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

MODEL_NAME = "Falconsai/nsfw_image_detection"
MODEL_CACHE = "model-cache"

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        self.model = AutoModelForImageClassification.from_pretrained(
            MODEL_NAME,
            cache_dir=MODEL_CACHE,
        )
        self.processor = ViTImageProcessor.from_pretrained(
            MODEL_NAME
        )

    def predict(
        self,
        image: Path = Input(description="Input image"),
    ) -> str:
        """Run a single prediction on the model"""
        img = Image.open(image)
       
        with torch.no_grad():
            inputs = self.processor(images=img, return_tensors="pt")
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_label = logits.argmax(-1).item()
        output = self.model.config.id2label[predicted_label]
        return output
