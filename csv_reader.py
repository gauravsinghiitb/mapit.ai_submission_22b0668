import csv
import os
import logging

# Set up logging for any issues with CSV reading
logging.basicConfig(filename='concept_extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_subject_csv(subject):
    """Read questions from a CSV file for the given subject and return as a list of dictionaries."""
    csv_path = os.path.join("resources", f"{subject}.csv")
    if not os.path.exists(csv_path):
        logging.error(f"CSV file {csv_path} not found")
        return []

    questions = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append(row)
        logging.info(f"Successfully read {len(questions)} questions from {csv_path}")
        return questions
    except Exception as e:
        logging.error(f"Error reading CSV {csv_path}: {str(e)}")
        return []