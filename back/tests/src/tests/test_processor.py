import pytest

from processor.text_analyzer import TextAnalyzerService


def test_detect_language():
    analyzer = TextAnalyzerService()
    
    # Test English
    text = "This is a test in English"
    language = analyzer.detect_language(text)
    assert language == "en"


def test_extract_topics():
    analyzer = TextAnalyzerService()
    
    text = "Python programming language is great for development. Python is easy to learn and Python has many libraries."
    topics = analyzer.extract_topics(text)
    
    assert "python" in topics
    assert len(topics) <= 5


def test_extract_topics_empty():
    analyzer = TextAnalyzerService()
    
    text = ""
    topics = analyzer.extract_topics(text)
    
    assert len(topics) == 0
