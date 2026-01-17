# analysis/batch_inference.py

import json
from analysis.model.indobertweet import SentimentModel
from analysis.sentiment_engine import SentimentDecisionEngine



def load_raw_reviews(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_processed_results(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_batch_inference(input_path, output_path):
    reviews = load_raw_reviews(input_path)

    model = SentimentModel(
        model_name="Aardiiiiy/indobertweet-base-Indonesian-sentiment-analysis"
    )
    engine = SentimentDecisionEngine(confidence_threshold=0.6)

    processed_results = []

    total = len(reviews)
    for i, r in enumerate(reviews, start=1):
        text = r.get("text", "")
        rating = r.get("rating")

        if not text or rating is None:
            continue

        model_output = model.predict(text)
        decision = engine.decide(model_output, rating)

        processed_results.append({
            "review_id": r.get("review_id"),
            "text": text,
            "rating": rating,
            "timestamp": r.get("at"),
            "model_output": model_output,
            "decision": decision
        })

        # 🔹 progress log (penting untuk UI nanti)
        if i % 50 == 0 or i == total:
            print(f"Processed {i}/{total} reviews")

    save_processed_results(processed_results, output_path)
    print(f"✔ Processed {len(processed_results)} reviews → {output_path}")

    return processed_results


# 🔹 masih bisa dijalankan manual (opsional)
if __name__ == "__main__":
    RAW_PATH = "data/raw/playstore_reviews.json"
    OUTPUT_PATH = "data/processed/playstore_sentiment_results.json"
    run_batch_inference(RAW_PATH, OUTPUT_PATH)