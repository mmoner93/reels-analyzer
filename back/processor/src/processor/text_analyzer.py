import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect
import re

class TextAnalyzerService:
    def __init__(self):
        # Ensure necessary NLTK data is downloaded
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('punkt')
            nltk.download('punkt_tab')
            
    def detect_language(self, text: str) -> str:
        """Detect the language of the text."""
        try:
            return detect(text)
        except Exception:
            return "unknown"
    
    def extract_topics(self, text: str) -> list[str]:
        """Extract key topics from text using NLTK for better filtering."""
        try:
            # Detect language to use appropriate stopwords
            lang = self.detect_language(text)
            lang_map = {
                'en': 'english',
                'es': 'spanish',
                'fr': 'french',
                'de': 'german',
                'it': 'italian',
                'pt': 'portuguese'
            }
            nltk_lang = lang_map.get(lang, 'english')
            
            # Clean text: remove punctuation and lower case
            text = re.sub(r'[^\w\s]', '', text.lower())
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Filter stop words and short/meaningless words
            stop_words = set(stopwords.words(nltk_lang))
            # Additional custom stop words
            custom_stops = {'video', 'reel', 'instagram', 'post', 'like', 'share', 'follow'}
            stop_words.update(custom_stops)
            
            filtered_tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
            
            # Frequency analysis
            word_freq = {}
            for word in filtered_tokens:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, _ in sorted_words[:5]]
            
        except Exception:
            # Fallback to simple method if NLTK fails
            words = re.sub(r'[^\w\s]', '', text.lower()).split()
            simple_stops = {'the', 'and', 'this', 'that', 'with', 'from', 'for'}
            words = [w for w in words if w not in simple_stops and len(w) > 3]
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            return [word for word, _ in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]]
