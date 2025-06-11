# 22b0668 Gaurav Singh
# Concept Extraction from Competitive Exam Questions

## What's This About?
This Python tool analyzes competitive exam questions (e.g., UPSC Ancient History, Economics, Math, Physics) to extract key concepts like "Harappan Civilization" or "Monetary Policy." Designed for flexibility, it handles multiple subjects and is prepared for future integration with a large language model (LLM) like Anthropic's Claude. It currently leverages smart keyword matching with NLP techniques to deliver accurate concept extraction.

## Cool Features
- **Smart Keyword Matching**: Identifies concepts using exact matches, fuzzy matching for close variations, and synonyms for broader coverage.
- **Context-Aware**: Analyzes both questions and answer options to pinpoint relevant concepts.
- **Keyword Suggestions**: Detects new terms in questions to expand the keyword list.
- **Multi-Subject Support**: Configurable for Ancient History, Economics, Math, Physics, and more via a single `config.json`.
- **LLM-Ready**: Structured to integrate with LLMs in the future, with placeholder logic for now.
- **Logging**: Records extraction details in `concept_extraction.log` for easy debugging.
- **Output**: Generates concepts in the console and `output_concepts.csv`, plus suggested keywords for refinement.

## File Structure
- `main.py`: Entry point for running the tool.
- `concept_extractor.py`: Core logic for concept extraction.
- `csv_reader.py`: Handles CSV input for questions.
- `config.json`: Defines keywords and synonyms for all subjects.
- `requirements.txt`: Lists dependencies (e.g., `nltk`, `fuzzywuzzy`).
- `resources/`: Contains question CSVs (`ancient_history.csv`, `economics.csv`, `math.csv`, `physics.csv`).
- `concept_extraction.log`: Logs extraction details.
- `output_concepts.csv`: Output file with extracted concepts.
- 
# the outputs- 
<small>
Loaded 20 Questions for Subject: Physics


**Question 1: Electrostatics**  
Suggested Keywords: charges, charges, charges  

**Question 2: Electrostatics**  
Suggested Keywords: constant, infinite, metal  

**Question 3: Electrostatics**  
Suggested Keywords: electric, electric, electric  

**Question 4: Electrostatics**  
Suggested Keywords: _____________, positive, electric  

**Question 5: Unknown**  
Suggested Keywords: silk, silk, silk  

**Question 6: Magnetism; Electrostatics**  
Suggested Keywords: rotating, magnetic, formula  

**Question 7: Magnetism**  
Suggested Keywords: magnetic, magnetic, ________  

**Question 8: Unknown**  
Suggested Keywords: north-south, south-west, north-west  

**Question 9: AC Circuits**  
Suggested Keywords: pure, pure, pure  

**Question 10: AC Circuits**  
Suggested Keywords: voltage, voltage, voltage  

**Question 11: Wave Optics**  
Suggested Keywords: decreasing, decreasing, reducing  

**Question 12: Wave Optics**  
Suggested Keywords: light, light, light  

**Question 13: Wave Optics**  
Suggested Keywords: fashionable, sunglasses, intensity  

**Question 14: Wave Optics; Photoelectric Effect**  
Suggested Keywords: diffraction, explain, theory  

**Question 15: Electromagnetic Waves**  
Suggested Keywords: conserved, interfere, intensity  

**Question 16: Wave Optics**  
Suggested Keywords: spherical, spherical, originates  

**Question 17: Nuclear Physics**  
Suggested Keywords: particle, daughter, isotopes  

**Question 18: Nuclear Physics**  
Suggested Keywords: excess, excess, undergoes  

**Question 19: Nuclear Physics**  
Suggested Keywords: electrons, neutrons, protons  

**Question 20: Electromagnetic Waves; Magnetism; Wave Optics; Electrostatics**  
Suggested Keywords: difference, electric, fields  

</small>



## How to Set It Up
1. **Grab the Code**:
   ```bash
   git clone https://github.com/your-repo/concept-extraction.git
   cd concept-extraction
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.8+. Then:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add CSV Files**:
   Drop your subject CSV files (like `ancient_history.csv`) into the `resources/` folder. They should look like:
   ```csv
   Question Number,Question,Option A,Option B,Option C,Option D,Answer
   1,Which of the following was a feature of the Harappan civilization?,City planning,Iron tools,Vedic rituals,Temple worship,A
   ```

4. **Tweak the Config**:
   Check `config.json` to update keywords, synonyms, or the fuzzy matching threshold.

5. **Run It**:
   ```bash
   python main.py --subject=ancient_history
   ```
   This processes the CSV, prints concepts, and saves results to `output_concepts.csv`.

## Example Output
Run:
```bash
python main.py --subject=ancient_history
```

**Console**:
```
Question 1: Harappan Civilization; Urban Planning; Archaeological Sites
Suggested Keywords: civilization, planning, city
Question 2: Revenue Systems; Village Institutions; Temple Education; Brahmadeya
Suggested Keywords: village, tank, brahmins
```

**output_concepts.csv**:
```csv
Question Number,Question,Concepts,Suggested Keywords
1,Which of the following was a feature of the Harappan civilization?,Harappan Civilization; Urban Planning; Archaeological Sites,civilization, planning, city
2,Consider the following pairs: Eripatti,Revenue Systems; Village Institutions; Temple Education; Brahmadeya,village, tank, brahmins
```

## Config File
The `config.json` file is the control center:
```json
{
  "keywords": {
    "ancient_history": {
      "harappan": ["Harappan Civilization", "Urban Planning", "Archaeological Sites"],
      "ashoka": ["Mauryan Empire", "Ashokan Edicts"]
    }
  },
  "synonyms": {
    "ancient_history": {
      "harappan": ["indus valley", "harappa"],
      "ashoka": ["asoka", "maurya"]
    }
  },
  "fuzzy_threshold": 80,
  "llm_prompt": "Given the question: {question}, identify the {subject} concept(s) this question is based on. Return a list of concepts."
}
```




## Dependencies
Check `requirements.txt` for the full list (e.g., `fuzzywuzzy`, `nltk`).

## Makefile
```makefile
run:
	python main.py --subject=ancient_history

install:
	pip install -r requirements.txt
```
