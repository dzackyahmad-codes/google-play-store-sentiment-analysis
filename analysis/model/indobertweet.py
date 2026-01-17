# analysis/model/indobertweet.py

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class SentimentModel:
    def __init__(
        self,
        model_name="Aardiiiiy/indobertweet-base-Indonesian-sentiment-analysis"
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

        self.model.to(self.device)
        self.model.eval()

        # ambil label langsung dari config model
        self.id2label = self.model.config.id2label

    def predict(self, text: str) -> dict:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1).cpu().numpy()[0]

        label_id = int(probs.argmax())

        return {
            "label": self.id2label[label_id],
            "confidence": float(probs[label_id]),
            "probabilities": {
                self.id2label[i]: float(probs[i])
                for i in range(len(probs))
            }
        }
