import argparse
import csv
import json
import logging
import os
from csv_reader import read_subject_csv
from concept_extractor import ConceptExtractor

# Set up logging to keep track of what's happening
logging.basicConfig(filename='concept_extraction.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Intern Test Task: Question to Concept Mapping")
    parser.add_argument('--subject', required=True, choices=['ancient_history', 'math', 'physics', 'economics'], help='Subject to process')
    args = parser.parse_args()
    data = read_subject_csv(args.subject)
    print(f"Loaded {len(data)} questions for subject: {args.subject}")

    # Load config for keywords and synonyms
    config_path = "config.json"
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        logging.info(f"Loaded config from {config_path}")
    except FileNotFoundError:
        logging.error(f"Config file {config_path} not found")
        print(f"Can't find {config_path}. Make sure it's in the project folder!")
        return
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in {config_path}")
        print(f"Something's wrong with {config_path}'s JSON format. Check it out!")
        return

    # Initialize our concept extractor
    extractor = ConceptExtractor(config)

    # Write results to output CSV
    output_path = "output_concepts.csv"
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Question Number", "Question", "Concepts", "Suggested Keywords"])

            # --- PLACEHOLDER FOR USER CODE ---
            # Loop through each question and extract concepts
            for row in data:
                q_num = row['Question Number']
                q_text = row['Question']
                # Grab options for extra context
                options = [row.get(f'Option {opt}', '') for opt in ['A', 'B', 'C', 'D']]
                # Extract concepts and suggested keywords
                concepts, suggested_keywords = extractor.extract_concepts(q_text, options, args.subject)
                # Print to console as per expected format
                print(f"Question {q_num}: {'; '.join(concepts)}")
                if suggested_keywords:
                    print(f"Suggested Keywords: {', '.join(suggested_keywords)}")
                # Write to CSV
                writer.writerow([q_num, q_text, "; ".join(concepts), ", ".join(suggested_keywords)])
            # ----------------------------------

        logging.info(f"Successfully wrote output to {output_path}")
    except Exception as e:
        logging.error(f"Error writing to {output_path}: {str(e)}")
        print(f"Oops, something went wrong writing the output. Check the log for details!")

if __name__ == "__main__":
    main()