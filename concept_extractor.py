import re
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import logging

# Download NLTK data to avoid missing resource errors
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

# Set up logging to debug extraction issues
logging.basicConfig(filename='concept_extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ConceptExtractor:
    def __init__(self, config):
        """Set up the extractor with keywords and synonyms from config."""
        self.config = config
        self.keyword_dict = config.get("keywords", {})
        self.synonyms = config.get("synonyms", {})
        self.fuzzy_threshold = config.get("fuzzy_threshold", 80)
        self.stop_words = set(stopwords.words('english'))
        # Filter out generic terms to improve keyword suggestions
        self.stop_words.update(['statement', 'statement-i', 'statement-ii', 'following', 'correct', 'above', 'consider', 'reference', 'given', 'select'])
        logging.info("ConceptExtractor initialized with config")

    def extract_concepts(self, question, options, subject):
        """Extract concepts and suggest new keywords from question and options."""
        text = question + " " + " ".join(options)
        concepts = self._keyword_based_extraction(text, subject)
        suggested_keywords = self._suggest_keywords(text, subject, concepts)

        if not concepts:
            logging.warning(f"No concepts found for question: {question[:50]}...")

        return concepts if concepts else ["Unknown"], suggested_keywords

    def _keyword_based_extraction(self, text, subject):
        """Find concepts using exact, fuzzy, and synonym matching."""
        concepts = set()
        text_lower = text.lower()

        if subject not in self.keyword_dict:
            logging.warning(f"No keywords for subject {subject}. Check config.json!")
            return []

        for keyword, concept_list in self.keyword_dict[subject].items():
            # Exact match with word boundaries
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                concepts.update(concept_list)
                logging.debug(f"Exact match: {keyword}")
            # Fuzzy match for variations
            elif fuzz.partial_ratio(keyword, text_lower) >= self.fuzzy_threshold:
                concepts.update(concept_list)
                logging.debug(f"Fuzzy match: {keyword}")
            # Synonym match
            for synonym in self.synonyms.get(subject, {}).get(keyword, []):
                if re.search(r'\b' + re.escape(synonym) + r'\b', text_lower):
                    concepts.update(concept_list)
                    logging.debug(f"Synonym match: {synonym} for {keyword}")

        return list(concepts)

    def _suggest_keywords(self, text, subject, extracted_concepts):
        """Suggest domain-specific keywords from unmapped terms."""
        text_lower = text.lower()
        existing_keywords = set(self.keyword_dict.get(subject, {}).keys())
        existing_synonyms = set()
        for synonyms in self.synonyms.get(subject, {}).values():
            existing_synonyms.update(synonyms)

        words = [w for w in word_tokenize(text_lower) if w not in self.stop_words]
        suggestions = []
        for word in words:
            if (len(word) > 3 and
                word not in existing_keywords and
                word not in existing_synonyms and
                not any(word in concept.lower() for concept in extracted_concepts)):
                score = len(word) * words.count(word)
                suggestions.append((word, score))

        # Return top 3 unique suggestions
        suggestions = [word for word, _ in sorted(suggestions, key=lambda x: x[1], reverse=True)[:3]]
        logging.debug(f"Suggested keywords: {suggestions}")
        return suggestions