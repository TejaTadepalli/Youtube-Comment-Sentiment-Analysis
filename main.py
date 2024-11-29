from flask import Flask, render_template, request
import os
import pyfile_web_scraping
import sentiment_analysis_youtube_comments
import delete_files
import pandas as pd
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap_comments():
    # Get YouTube URL from the form
    url = request.form.get('youtube url')
    print(f"Received YouTube URL: {url}")  # Debugging
    
    # Call the web scraping function
    try:
        file_and_detail = pyfile_web_scraping.scrapfyt(url)
        print(f"Scraped details: {file_and_detail}")  # Debugging
    except Exception as e:
        print(f"Error in scraping YouTube data: {e}")  # Debugging
        return f"Error: Unable to scrape data from the provided URL. {e}"

    # Perform sentiment analysis
    try:
        sentiment = sentiment_analysis_youtube_comments.sepposnegcom("Full Comments.csv")
        print(f"Sentiment analysis results: {sentiment}")  # Debugging
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")  # Debugging
        return f"Error: Sentiment analysis failed. {e}"

    # Check if sentiment files were created
    pos_file = '(1,).csv'
    neg_file = '(0,).csv'
    print(f"Checking if sentiment files exist in the current directory:")
    print(f"Positive file exists: {os.path.exists(pos_file)}")
    print(f"Negative file exists: {os.path.exists(neg_file)}")

    if not os.path.exists(pos_file) or not os.path.exists(neg_file):
        print("Error: Sentiment files not found after analysis!")  # Debugging
        return "Error: Sentiment analysis files are missing."

    # Read sentiment files
    try:
        pos_comments_csv = pd.read_csv(pos_file)
        neg_comments_csv = pd.read_csv(neg_file)
        print("Positive comments DataFrame (first few rows):")  # Debugging
        print(pos_comments_csv.head())  # Debugging
        print("Negative comments DataFrame (first few rows):")  # Debugging
        print(neg_comments_csv.head())  # Debugging
    except Exception as e:
        print(f"Error reading sentiment files: {e}")  # Debugging
        return f"Error: Unable to read sentiment files. {e}"

    # Extract video details
    try:
        list_file_and_detail = list(file_and_detail)
        video_title, video_owner, video_comment_with_replies, video_comment_without_replies = list_file_and_detail[1:]
        print(f"Video details extracted: Title: {video_title}, Owner: {video_owner}")  # Debugging
    except Exception as e:
        print(f"Error extracting video details: {e}")  # Debugging
        return f"Error: Failed to extract video details. {e}"

    # Extract sentiment data
    try:
        list_sentiment = list(sentiment)
        video_positive_comments, video_negative_comments = list_sentiment[-2:]
        print(f"Video sentiment summary: Positive: {video_positive_comments}, Negative: {video_negative_comments}")  # Debugging
    except Exception as e:
        print(f"Error extracting sentiment summary: {e}")  # Debugging
        return f"Error: Failed to extract sentiment summary. {e}"

    # Clean up temporary files
    print("Deleting temporary files...")  # Debugging
    try:
        delete_files.file_delete()
        print("Temporary files deleted.")  # Debugging
    except Exception as e:
        print(f"Error deleting temporary files: {e}")  # Debugging

    # Prepare success message
    after_complete_message = "Below is the analysis of the video:"
    return render_template(
        "index.html",
        after_complete_message=after_complete_message,
        title=video_title,
        owner=video_owner,
        comment_w_replies=video_comment_with_replies,
        comment_wo_replies=video_comment_without_replies,
        positive_comment=video_positive_comments,
        negative_comment=video_negative_comments,
        pos_comments_csv=[pos_comments_csv.to_html()],
        neg_comments_csv=[neg_comments_csv.to_html()]
    )

if __name__ == "__main__":
    print("Starting Flask application...")  # Debugging
    app.run()