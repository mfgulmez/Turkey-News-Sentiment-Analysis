# Turkey-News-Sentiment-Analysis
This project integrates a pipeline for sentiment analysis on news that are targetted on Turkey
The pipeline consists of 5 sub-tasks:</br>
1.Data Gathering
2.Translation of the Data
3.Training and Testing of Sentiment Analysis Model

## Data Gathering
Approximately 2000 news from 4 foreign sources (The New York Times, Aljazeera, The Guardian and BBC) are gathered using web scrapping.
Bodies of the news are filtered and selected sentences or pharagraphs that contains certain keywords (Turkey, Istanbul or Ankara)
Then they are preprocessed before the translation process.

## Preprocessing
Every news from the news dataset are standardized to contain at most 512 tokens per news, this enables a more coherent translation on each sentence.

## Translation
News are translated using The Helsinki model.

## Training and Testing
3 Models (Logistic Regression, Linear SVC and Random Forest) are trained with Zero-Shot Learning


![image](https://github.com/user-attachments/assets/d463e4f8-8fe8-4d6e-834c-ddc0fb9d84cd)
