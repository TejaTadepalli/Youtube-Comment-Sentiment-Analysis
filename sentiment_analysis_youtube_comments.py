import pandas as pd
import csv
import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sepposnegcom(comment_file):
    print(f"Processing sentiment analysis for file: {comment_file}")  # Debugging

    # Check if file exists
    if not os.path.exists(comment_file):
        raise FileNotFoundError(f"File {comment_file} does not exist. Please provide a valid file.")
    
    # Reading Dataset
    dataset = pd.read_csv(comment_file, encoding_errors='ignore')
    print("Dataset loaded successfully.")
    print("Columns available in dataset:", dataset.columns.tolist())  # Debugging
    print("First few rows of the dataset:\n", dataset.head())  # Debugging

    # Check if 'Comment' column exists
    if 'Comment' not in dataset.columns:
        raise ValueError("The input dataset does not have a 'Comment' column.")

    # Sentiment analysis of comments using VADER SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)
        return 0 if scores["neg"] > scores["pos"] else 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x: vader_sentiment_result(x))
    print("Sentiment analysis completed. First few rows:\n", dataset.head())  # Debugging

    # Separating Positive and Negative Comments
    positive_comments = dataset[dataset['vader_sentiment'] == 1]
    negative_comments = dataset[dataset['vader_sentiment'] == 0]

    # Save to CSV files
    positive_file = '(1,).csv'
    negative_file = '(0,).csv'

    if not positive_comments.empty:
        positive_comments.to_csv(positive_file, index=False)
        print(f"Saved positive comments to {positive_file}.")  # Debugging
    else:
        # Create empty positive file if no comments found
        with open(positive_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Empty'])
            writer.writerow(['No Positive Comments'])
        print(f"No positive comments found. Created empty {positive_file}.")  # Debugging

    if not negative_comments.empty:
        negative_comments.to_csv(negative_file, index=False)
        print(f"Saved negative comments to {negative_file}.")  # Debugging
    else:
        # Create empty negative file if no comments found
        with open(negative_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Empty'])
            writer.writerow(['No Negative Comments'])
        print(f"No negative comments found. Created empty {negative_file}.")  # Debugging

    # Count total rows in positive and negative comments
    video_positive_comments = f"{len(positive_comments)} Comments" if not positive_comments.empty else '0 Comments'
    video_negative_comments = f"{len(negative_comments)} Comments" if not negative_comments.empty else '0 Comments'

    # Debugging final counts
    print(f"Total Positive Comments: {video_positive_comments}")
    print(f"Total Negative Comments: {video_negative_comments}")

    # Return final results
    return positive_file, negative_file, video_positive_comments, video_negative_comments
