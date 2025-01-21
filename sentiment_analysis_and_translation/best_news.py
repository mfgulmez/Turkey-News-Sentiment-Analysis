import pandas as pd

# Load your CSV file into a DataFrame
df = pd.read_csv('news_with_sentiment.csv')  # Replace with your actual file

# Filter positive and negative sentiment rows
positive_df = df[df['sentiment_label'] == 'POSITIVE']
negative_df = df[df['sentiment_label'] == 'NEGATIVE']

# Sort each DataFrame by sentiment_score in descending order
positive_df_sorted = positive_df.sort_values(by='sentiment_score', ascending=False)
negative_df_sorted = negative_df.sort_values(by='sentiment_score', ascending=False)

# Get the top 500 positive and top 500 negative rows based on sentiment_score
top_positive = positive_df_sorted.head(500)
top_negative = negative_df_sorted.head(500)

# Concatenate the two DataFrames
result_df = pd.concat([top_positive, top_negative])

# Save the resulting DataFrame to a new CSV file
result_df.to_csv('best_news.csv', index=False)

# Optionally, print the first few rows to verify
print(result_df.head())
