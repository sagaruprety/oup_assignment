from pydantic import BaseModel
from collections import defaultdict
import json
from typing import List, Optional

# Define data classes using Pydantic

class Token(BaseModel):
    id: str
    text: str
    lemma: str
    pos: str
    pos_finegrained: str
    feats: Optional[str] = None
    start_char: str
    end_char: str

class Sentence(BaseModel):
    sentence_text: str
    tokens: List[Token]

def process_input(input_data: dict) -> Dict[str, Dict[str, Any]]:
    """
    Process the input data and generate lemma frequency information.

    Args:
        input_data (dict): Parsed input data.

    Returns:
        dict: Output containing lemma frequency information for each lemma.
    """
    lemma_info = {}  # To store lemma info

    for sentence in input_data['sentences']:

        for token in sentence['tokens']:
            lemma = token['lemma']
            pos = token['pos']
            feats = token['feats']
            wordform = token['text']
            # Update the lemma info

            # initialising dictionary at first encounter with  key
            if not lemma in lemma_info:
                lemma_info[lemma] = {}
            lemma_info[lemma]['pos'] = pos
            lemma_info[lemma]['inflection_info'] = feats

            # initialising dictionary at first encounter with  key
            if not 'total_frequency' in lemma_info[lemma]:
                lemma_info[lemma]['total_frequency'] = 0
            lemma_info[lemma]['total_frequency'] += 1

            # initialising dictionary at first encounter with  key
            if not 'wordform_frequency' in lemma_info[lemma]:
                lemma_info[lemma]['wordform_frequency'] = {}
                
            # initialising dictionary at first encounter with  key
            if not wordform in lemma_info[lemma]['wordform_frequency']:
                lemma_info[lemma]['wordform_frequency'][wordform] = 0
            lemma_info[lemma]['wordform_frequency'][wordform] += 1


    return lemma_info


if __name__ == "__main__":
    # Load the input data
    with open('./data/sample_parsed_sentences.json') as f:
        input_data = json.load(f)

    # Process the input data and display the output
    output = process_input(input_data)

    # Save the output data as a JSON file
    with open('./data/output.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)