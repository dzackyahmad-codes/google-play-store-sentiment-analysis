import json
import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


# -------------------------
# STOPWORDS
# -------------------------
STOPWORDS_ID = [
    "ga", "yg", "nya", "ada", "adalah", "dan", "di", "ke", "dari",
    "yang", "untuk", "dengan", "ini", "itu", "saya", "kami", "kita",
    "tidak", "ga", "gak", "aja", "udah", "udah", "banget"
]


# -------------------------
# UTIL
# -------------------------
def load_processed_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_insight(insight, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(insight, f, ensure_ascii=False, indent=2)


def sentiment_distribution(data):
    counter = Counter()
    for d in data:
        counter[d["decision"]["final_sentiment"]] += 1
    return dict(counter)


# -------------------------
# TF-IDF CORE
# -------------------------
def extract_tfidf_keywords(
    texts,
    top_n=5,
    min_df=3,
    max_df=0.9,
    ngram_range=(2, 3),
    require_phrase=True
):
    if not texts or len(texts) < min_df:
        return []

    vectorizer = TfidfVectorizer(
        stop_words=STOPWORDS_ID,
        min_df=min_df,
        max_df=max_df,
        ngram_range=ngram_range
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        return []

    if tfidf_matrix.shape[1] == 0:
        return []

    scores = tfidf_matrix.mean(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(
        zip(terms, scores),
        key=lambda x: x[1],
        reverse=True
    )

    if require_phrase:
        ranked = [(t, s) for t, s in ranked if len(t.split()) >= 2]

    return ranked[:top_n]



# -------------------------
# MAIN INSIGHT GENERATOR
# -------------------------

def rating_distribution(data):
    dist = {str(i): 0 for i in range(1, 6)}
    for d in data:
        rating = d.get("rating")
        if rating:
            dist[str(rating)] += 1
    return dist


def generate_insight(processed_path, insight_path):
    data = load_processed_data(processed_path)

    negative_texts = [
        d["text"] for d in data
        if d["decision"]["final_sentiment"] == "Negative"
    ]

    positive_texts = [
        d["text"] for d in data
        if d["decision"]["final_sentiment"] == "Positive"
    ]

    insight = {
        "total_reviews": len(data),
        "sentiment_distribution": sentiment_distribution(data),
        "rating_distribution": rating_distribution(data),
        "top_negative_keywords": extract_tfidf_keywords(negative_texts),
        "top_positive_keywords": extract_tfidf_keywords(positive_texts),
    }

    save_insight(insight, insight_path)
    return insight



# -------------------------
# MANUAL TEST
# -------------------------
if __name__ == "__main__":
    generate_insight(
        processed_path="data/processed/test_processed.json",
        insight_path="data/insight/test_insight.json"
    )
