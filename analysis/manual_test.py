# analysis/manual_test.py

from model.indobertweet import SentimentModel
from sentiment_engine import SentimentDecisionEngine


def main():
    print("=== MANUAL SENTIMENT TEST ===")
    print("Ketik 'exit' untuk keluar\n")

    model = SentimentModel()
    engine = SentimentDecisionEngine()

    while True:
        text = input("Masukkan kalimat: ").strip()
        if text.lower() == "exit":
            print("Keluar.")
            break

        rating_input = input("Masukkan rating (1–5, opsional, enter jika tidak ada): ").strip()
        rating = int(rating_input) if rating_input.isdigit() else None

        # Model inference
        model_output = model.predict(text)

        print("\n--- MODEL OUTPUT ---")
        print(f"Label     : {model_output['label']}")
        print(f"Confidence: {model_output['confidence']:.4f}")
        print(f"Probabilities:")
        for k, v in model_output["probabilities"].items():
            print(f"  {k:8s}: {v:.4f}")

        # Decision engine (jika rating ada)
        if rating is not None:
            decision = engine.decide(model_output, rating)

            print("\n--- DECISION ENGINE ---")
            print(f"Text Sentiment : {decision['text_sentiment']}")
            print(f"Rating         : {decision['rating']}")
            print(f"Final Sentiment: {decision['final_sentiment']}")
            print(f"Reason         : {decision['reason']}")

        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
