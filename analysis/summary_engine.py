# analysis/summary_engine.py

import json


INSIGHT_PATH = "data/insight/playstore_insight.json"


def load_insight(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_summary(insight: dict) -> str:
    total = insight["total_reviews"]
    dist = insight["sentiment_distribution"]

    neg = dist.get("Negative", 0)
    neu = dist.get("Neutral", 0)
    pos = dist.get("Positive", 0)

    # Ambil top keyword (jika ada)
    neg_issues = [k for k, _ in insight.get("top_negative_keywords", [])]
    pos_points = [k for k, _ in insight.get("top_positive_keywords", [])]

    sentences = []

    # Kalimat 1 — gambaran umum
    sentences.append(
        f"Dari {total} ulasan pengguna, sentimen negatif ({neg}) dan positif ({pos}) menjadi yang paling dominan, "
        f"dengan sebagian kecil ulasan bersifat netral ({neu})."
    )

    # Kalimat 2 — keluhan utama
    if neg_issues:
        issues_text = ", ".join(neg_issues[:2])
        sentences.append(
            f"Keluhan utama pengguna paling sering berkaitan dengan {issues_text}."
        )

    # Kalimat 3 — kelebihan utama
    if pos_points:
        points_text = ", ".join(pos_points[:2])
        sentences.append(
            f"Di sisi lain, pengguna banyak mengapresiasi {points_text} dari aplikasi ini."
        )

    return " ".join(sentences)


def main():
    insight = load_insight(INSIGHT_PATH)
    summary = generate_summary(insight)
    print(summary)


if __name__ == "__main__":
    main()
