# analysis/model/sentiment_engine.py

class SentimentDecisionEngine:
    def __init__(self, confidence_threshold=0.6):
        self.confidence_threshold = confidence_threshold

    def decide(self, model_output: dict, rating: int) -> dict:
        text_label = model_output["label"]          # e.g. "Negative"
        confidence = model_output["confidence"]

        # Mapping rating → sentiment kasar
        if rating <= 2:
            rating_sentiment = "negative"
        elif rating == 3:
            rating_sentiment = "neutral"
        else:
            rating_sentiment = "positive"

        # ✅ DEFAULT decision: ikut teks
        final_sentiment = text_label
        reason = "text sentiment"

        # Conflict handling
        if rating_sentiment.lower() != text_label.lower():
            if confidence < self.confidence_threshold:
                final_sentiment = rating_sentiment
                reason = "rating overrides low-confidence text"
            else:
                reason = "text overrides rating due to high confidence"

        # ✅ Normalisasi casing DI AKHIR
        final_sentiment = final_sentiment.title()
        rating_sentiment = rating_sentiment.title()
        text_label = text_label.title()

        return {
            "text_sentiment": text_label,
            "rating": rating,
            "rating_sentiment": rating_sentiment,
            "final_sentiment": final_sentiment,
            "confidence": confidence,
            "reason": reason
        }
