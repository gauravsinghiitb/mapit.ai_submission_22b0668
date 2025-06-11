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
    nltk.download('punkt_tab')  # Needed for newer NLTK versions
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
        logging.info("ConceptExtractor ready to go with config")

    def extract_concepts(self, question, options, subject):
        """Extract concepts and suggest new keywords from question and options."""
        # Combine question and options for richer context
        text = question + " " + " ".join(options)
        concepts = self._keyword_based_extraction(text, subject)
        suggested_keywords = self._suggest_keywords(text, subject, concepts)

        # Fallback to simulated LLM if no concepts found
        if not concepts:
            concepts = self._simulate_llm_call(question, options, subject)
            logging.info(f"Fell back to simulated LLM for question: {question[:50]}...")

        return concepts if concepts else ["Unknown"], suggested_keywords

    def _keyword_based_extraction(self, text, subject):
        """Find concepts using exact, fuzzy, and synonym matching."""
        concepts = set()
        text_lower = text.lower()

        if subject not in self.keyword_dict:
            logging.warning(f"No keywords for subject {subject}. Check config.json!")
            return []

        # Look for matches in keywords and synonyms
        for keyword, concept_list in self.keyword_dict[subject].items():
            # Exact match with word boundaries
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                concepts.update(concept_list)
                logging.debug(f"Got an exact match for keyword: {keyword}")
            # Fuzzy match for close variations
            elif fuzz.partial_ratio(keyword, text_lower) >= self.fuzzy_threshold:
                concepts.update(concept_list)
                logging.debug(f"Fuzzy match for keyword: {keyword}")
            # Check synonyms too
            for synonym in self.synonyms.get(subject, {}).get(keyword, []):
                if re.search(r'\b' + re.escape(synonym) + r'\b', text_lower):
                    concepts.update(concept_list)
                    logging.debug(f"Synonym match: {synonym} for keyword {keyword}")

        return list(concepts)

    def _suggest_keywords(self, text, subject, extracted_concepts):
        """Suggest new keywords from unmapped terms in the text."""
        text_lower = text.lower()
        existing_keywords = set(self.keyword_dict.get(subject, {}).keys())
        existing_synonyms = set()
        for synonyms in self.synonyms.get(subject, {}).values():
            existing_synonyms.update(synonyms)

        # Tokenize and filter out stopwords for better suggestions
        words = [w for w in word_tokenize(text_lower) if w not in self.stop_words]
        suggestions = []
        for word in words:
            if (len(word) > 3 and
                word not in existing_keywords and
                word not in existing_synonyms and
                not any(word in concept.lower() for concept in extracted_concepts)):
                # Score words by length and frequency
                score = len(word) * words.count(word)
                suggestions.append((word, score))

        # Pick top 3 suggestions by score
        suggestions = [word for word, _ in sorted(suggestions, key=lambda x: x[1], reverse=True)[:3]]
        logging.debug(f"Suggested keywords: {suggestions}")
        return suggestions

    def _simulate_llm_call(self, question, options, subject):
        """Fake an LLM call with pre-defined responses for testing."""
        full_text = f"{question} Options: {'; '.join(options)}"
        logging.debug(f"Simulating LLM for: {full_text[:100]}...")

        # Mock responses based on manual testing
        simulated_responses = {
            "Which of the following was a feature of the Harappan civilization": [
                "Harappan Civilization", "Urban Planning", "Archaeological Sites"
            ],
            "Consider the following pairs: Eripatti": [
                "Revenue Systems", "Village Institutions", "Temple Education", "Brahmadeya"
            ],
            "With reference to the scientific progress of Ancient India": [
                "History of Indian Science", "Chronological Reasoning", "Scientific Advancements"
            ],
            "Burzahom: Rock-cut shrines": [
                "Archaeological Sites", "Material Culture", "Chalcolithic Sites"
            ],
            "Which of the following is a measure of national income": [
                "Macroeconomics", "National Income"
            ],
            "What is the primary tool used by the central bank to control inflation": [
                "Monetary Policy", "Economic Policy"
            ],
            "What is the derivative of x^2 with respect to x": [
                "Calculus", "Differentiation"
            ],
            "Which of Newton's laws explains the concept of inertia": [
                "Classical Mechanics", "Newton's Laws"
            ]
        }

        # Return matching concepts or empty list
        for q, concepts in simulated_responses.items():
            if q in question:
                logging.info(f"Matched simulated response for question: {question[:50]}...")
                return concepts
        logging.warning(f"No simulated response for question: {question[:50]}...")
        return []