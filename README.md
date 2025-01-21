# Turkey-News-Sentiment-Analysis
This project integrates a pipeline for sentiment analysis on news that are targetted on Turkey</br>
The pipeline consists of 5 sub-tasks:</br>

1.Data Gathering</br>
2.Translation of the Data</br>
3.Training and Testing of Sentiment Analysis Model</br>

## Data Gathering
Approximately 2000 news from 4 foreign sources (The New York Times, Aljazeera, The Guardian and BBC) are gathered using web scrapping.
Bodies of the news are filtered and selected sentences or pharagraphs that contains certain keywords (Turkey, Istanbul or Ankara)
Then they are preprocessed before the translation process.

## Preprocessing
Every news from the news dataset are standardized to contain at most 512 tokens per news, this enables a more coherent translation on each sentence.

## Translation
News are translated using The Helsinki model.

## Training and Testing
Some Models  are trained with Zero-Shot Learning

### Metrics of Performance on some of models:
![image](https://github.com/user-attachments/assets/d463e4f8-8fe8-4d6e-834c-ddc0fb9d84cd)

### Word Cloud on Sentiments:
![image](https://github.com/user-attachments/assets/382edfd3-b015-4867-ac1e-8d59b062a010)

### Performance Metrics on Bart(Zero-Shot):
![image](https://github.com/user-attachments/assets/d54b93e9-9b93-4c2d-93b6-d9d0f5caf9bc)

### Word Cloud of Sentiments With Bart:
![image](https://github.com/user-attachments/assets/d5b51452-ad80-4f52-a47b-b8205ec515b7)




