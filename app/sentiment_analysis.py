from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text: str) -> str:
    analyzer = SentimentIntensityAnalyzer()
    
    score = analyzer.polarity_scores(text)
    
    if score['compound'] > 0.05:
        return "Positive"
    elif score['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"
