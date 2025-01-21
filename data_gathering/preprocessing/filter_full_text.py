import pandas as pd
from nltk.tokenize import sent_tokenize
import nltk
from transformers import AutoTokenizer

# Download necessary NLTK data
nltk.download('punkt')

# Load the CSV file into a DataFrame
df = pd.read_csv("news.csv")

# Initialize the tokenizer from Hugging Face (DistilBERT in this case)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Function to extract sentences up to a limit of 512 tokens
def get_sentences_up_to_512_tokens(text):
    sentences = sent_tokenize(text)  # Tokenize the text into sentences
    token_count = 0
    selected_sentences = []
    
    # Iterate through sentences and accumulate tokens
    for sentence in sentences:
        # Tokenize each sentence
        tokens = tokenizer.encode(sentence)
        token_count += len(tokens)
        
        # If adding this sentence exceeds 512 tokens, stop
        if token_count > 512:
            break
        
        # Add sentence to the selected sentences list
        selected_sentences.append(sentence)
    
    # Join the selected sentences into a single text block
    return ' '.join(selected_sentences)

df["full_text"] = df["full_text"].fillna("")

# Apply the function to the `full_text` column
df["shortened_full_text"] = df["full_text"].apply(
    lambda x: get_sentences_up_to_512_tokens(x)
)

# Remove the 'full_text' column
df = df.drop(columns=["full_text"])

# Save the modified DataFrame to a new CSV file (optional)
df.to_csv("shortened_news.csv", index=False)

# Display the updated DataFrame
print(df["shortened_full_text"])
