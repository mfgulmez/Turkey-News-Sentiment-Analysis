import pandas as pd
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Load your CSV file into a DataFrame
df = pd.read_csv('shortened_news.csv')  # Replace 'shortened_file.csv' with the actual path to your file

# Function to apply sentiment analysis and return both label and score
def get_sentiment(text):
    result = sentiment_pipeline(str(text))
    sentiment_label = result[0]["label"]
    sentiment_score = result[0]["score"]
    return sentiment_label, sentiment_score

# Apply sentiment analysis to the 'shortened_full_text' column and get both label and score
df["sentiment_label"], df["sentiment_score"] = zip(*df["shortened_full_text"].apply(lambda x: get_sentiment(x) if isinstance(x, str) else ("UNKNOWN", 0.0)))

# Count the occurrences of positive and negative sentiments
sentiment_counts = df["sentiment_label"].value_counts()

# Print the sentiment counts
print(sentiment_counts)

# Optionally, print the first few rows to verify
print(df.head())

# Save the updated DataFrame with sentiment labels and scores to a new CSV file
df.to_csv("news_with_sentiment.csv", index=False)
