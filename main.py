import pandas as pd
import re
import nltk
import os
import logging
import time
import json
import csv
import shutil
from tqdm import tqdm

CONFIG_FILE_PATH = 'config.json'

# initialize log file
def setup_logging():
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    timestamp = time.strftime("%d-%m-%Y-%H.%M.%S", time.localtime(time.time()))
    log_file_path = f"{log_folder}/cleaning_logs_{timestamp}.log"
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging setup complete.\n")

# load config
def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            config = json.load(file)
        logging.info("Configuration loaded successfully.\n")
        return config
    except FileNotFoundError:
        logging.error("Configuration file was not found.")
        raise
    except json.JSONDecodeError:
        logging.error("Error decoding the JSON configuration file.")
        raise

def initial_caps_cluster(text, min_capitals=4, max_lowercase_allowed=2):
    words = text.split()
    total_checked = 0
    capital_count = 0
    lowercase_count = 0

    for word in words:
        if word[0].isupper():
            capital_count += 1
        elif word[0].islower() and len(word) <= 6 and lowercase_count < max_lowercase_allowed:
            lowercase_count += 1
        else:
            break  # either too many lowercase words or a long one, end the cluster

        total_checked += 1

    return capital_count >= min_capitals

def initial_lowercase_cluster(text, max_lowercase=3, max_capital_allowed=4):
    """
    Returns True if the left context of the text
    contains more than `max_lowercase` lowercase-initial words,
    allowing up to `max_capital_allowed` capitalized-initial words.
    """
    words = text.split()
    lowercase_count = 0
    capital_count = 0

    for word in words[1:]:
        stripped = word.lstrip(",:;.!?\"'“”")

        if not stripped:
            continue

        first_char = stripped[0]
        if first_char.islower():
            lowercase_count += 1
        elif first_char.isupper():
            capital_count += 1
        else:
            break  # Stop if we hit something that’s not a word (e.g., punctuation-only token)

        if lowercase_count > max_lowercase and capital_count <= max_capital_allowed:
            return True
        elif capital_count > max_capital_allowed:
            break

    return False

def fix_bad_punctuation(text):
    """
    Detect unspaced, punctuated word-end, e.g.: "lorem!Ipsum, Lorem!Ipsum, lorem?ipsum"
    Punctuations: ".", "!", "?" (for both lowercase words: "!", "?")
    Returns the corrected string.
    """
    # uppercase words
    text = re.sub(r'(?<=[.!?])(?=[A-Z])', ' ', text)
    
    # lowercase words
    text = re.sub(r'(?<=[!?])(?=[a-z])', ' ', text)

    return text


def keep_initial_cap_cluster(text, max_lowercase_allowed=2, long_sentence_threshold=15):
    """
    Keep clusters of capitalized words on the left context of the text. 
    Tolerate two lowercase words
    Cluster threshold is 15 words
    """
    # 1) Normalize zero‑width spaces
    text = re.sub(r'[\u200B-\u200D\u2060]', '', text)
    
    # 2) Detect full vs truncated quotes
    full_double = text.count('"') >= 2
    full_curly  = text.count('“') >= 1 and text.count('”') >= 1
    full_quote_mode = full_double or full_curly

    words = text.split()
    sentence_length = len(words)

    cluster = []
    cap_positions = []
    lowercase_count = 0

    for word in words:
        w = word.replace("&amp;", "&")
        stripped = re.sub(r'(^[^\w&]+|[^\w&]+$)', '', w)

        # stop on opening quote if truncated
        if not full_quote_mode and w and w[0] in ('"', '“', '‘'):
            break

        # keep pure punctuation
        if not stripped:
            cluster.append(word)
            continue

        # capital‑initial
        if stripped[0].isupper():
            cluster.append(word)
            cap_positions.append(len(cluster)-1)
            lowercase_count = 0

        # short lowercase glue
        elif (stripped[0].islower() 
              and len(stripped) <= 12 
              and lowercase_count < max_lowercase_allowed):
            cluster.append(word)
            lowercase_count += 1

        # numbers/percent/adjectival years
        elif re.fullmatch(r'\d+([.,]\d+)?%?[,\.]?|\d{4}(?:-?an)?', stripped):
            cluster.append(word)

        # ampersand
        elif stripped == "&":
            cluster.append(word)

        # anything else → stop
        else:
            break

    # only apply penultimate rule on long sentences
    if sentence_length > long_sentence_threshold and len(cap_positions) >= 2:
        penult = cap_positions[-2]
        return ' '.join(cluster[:penult+1])
    else:
        return ' '.join(cluster)

def handle_short_token(token_props, start, end):
    if (
        token_props['starts_with_baca_juga'] and 
        token_props['with_consecutive_caps'] and 
        token_props['ends_with_exclamation']
    ):
        return (start, end)
    elif (
        token_props['ends_with_exclamation'] and
        (token_props['with_consecutive_caps'] or token_props['starts_with_baca_juga'])
    ):
        return (start, end)
    elif token_props['starts_with_baca_juga']:
        return (start, end)
    elif token_props['with_consecutive_caps']:
        return (start, end)
    elif token_props['ends_with_exclamation']:
        return (start, end)
    return None

def handle_medium_token(token, token_split, token_props, base_offset, match_text, clue_words):
    spans = []
    first_18_tokens = ' '.join(token_split[:18])
    start = match_text.find(token)
    if start == -1:
        return spans
    global_start = base_offset + start
    end = global_start + len(token)

    if (
        token_props['starts_with_baca_juga'] and
        token_props['with_consecutive_caps'] and
        token_props['ends_with_exclamation']
    ):
        spans.append((global_start, end))

    elif (
        token_props['ends_with_exclamation'] and
        (token_props['with_consecutive_caps'] or token_props['starts_with_baca_juga'])
    ):
        if token_props['with_consecutive_lower'] and token_props['starts_with_baca_juga']:
            spans.append((global_start, end))
        elif token_props['starts_with_baca_juga']:
            if len(token_split) > 24:
                cutoff = first_18_tokens
                cutoff_local = match_text.find(cutoff)
                if cutoff_local != -1:
                    span_start = base_offset + cutoff_local
                    spans.append((span_start, span_start + len(cutoff)))
            else:
                spans.append((global_start, end))
        elif token_props['with_consecutive_caps']:
            if len(token_split) > 24:
                cutoff = first_18_tokens
                cutoff_local = match_text.find(cutoff)
                if cutoff_local != -1:
                    span_start = base_offset + cutoff_local
                    spans.append((span_start, span_start + len(cutoff)))
            else:
                spans.append((global_start, end))

    elif token_props['starts_with_baca_juga']:
        if token_props['with_consecutive_lower']:
            cutoff = first_18_tokens
            cutoff_local = match_text.find(cutoff)
            if cutoff_local != -1:
                span_start = base_offset + cutoff_local
                spans.append((span_start, span_start + len(cutoff)))
        else:
            mod = keep_initial_cap_cluster(token)
            mod_local = match_text.find(mod)
            if mod_local != -1:
                span_start = base_offset + mod_local
                spans.append((span_start, span_start + len(mod)))

    elif token_props['with_consecutive_caps']:
        if any(re.search(rf'\b{word}\b', first_18_tokens, re.IGNORECASE) for word in clue_words):
            mod = keep_initial_cap_cluster(token)
            mod_local = match_text.find(mod)
            if mod_local != -1:
                span_start = base_offset + mod_local
                spans.append((span_start, span_start + len(mod)))
    return spans

def handle_long_token(token, token_split, token_props, base_offset, match_text, clue_words):
    return handle_medium_token(token, token_split, token_props, base_offset, match_text, clue_words)

def clean_text(text, row_index=None):
    if not isinstance(text, str):
        text = str(text) if not pd.isna(text) else ""

    baca_juga_re = re.compile(r"(?i)(baca juga[:\-\s]+(?:[\w\W]+?)(?=\s+baca juga|$))")
    clue_words = ['coba', 'cek', 'lihat', 'simak', 'awas', 'klaim']
    deletion_spans = []

    matches = list(baca_juga_re.finditer(text))

    if not matches:
        return
    logging.info(f"=== Baca juga constituent found on row {row_index} ===")

    for match in matches:
        match_text = match.group(1).strip()
        sentence = ' '.join(match_text.split())
        base_offset = match.start(1)
        
        sentence = fix_bad_punctuation(sentence)

        tokens = nltk.tokenize.sent_tokenize(sentence)[:3]
        
        n_token = 0
        for token in tokens:
            n_token =+ 1
            logging.info(f"Token count: {n_token}\n")
            token_split = token.split()
            word_count = len(token_split)

            token_props = {
                'starts_with_baca_juga': token.lower().startswith("baca juga"),
                'ends_with_exclamation': token.endswith("!"),
                'with_consecutive_caps': initial_caps_cluster(token),
                'with_consecutive_lower': initial_lowercase_cluster(token),
            }

            if word_count <= 10:
                span = handle_short_token(token_props, base_offset + match_text.find(token), base_offset + match_text.find(token) + len(token))
                if span:
                    deletion_spans.append(span)
            elif word_count <= 35:
                deletion_spans.extend(handle_medium_token(token, token_split, token_props, base_offset, match_text, clue_words))
            else:
                deletion_spans.extend(handle_long_token(token, token_split, token_props, base_offset, match_text, clue_words))

    # final cleanup
    cleaned_parts = []
    truncated_parts = []
    
    last_idx = 0
    for start, end in sorted(deletion_spans):
        cleaned_parts.append(text[last_idx:start])
        truncated_parts.append(text[start:end])
        last_idx = end
    cleaned_parts.append(text[last_idx:])

    cleaned_text = ''.join(cleaned_parts)
    truncated_text = ' '.join(truncated_parts)

    return cleaned_text, truncated_text

def detect_baca_juga(text):
    """
    Returns True if "baca juga" exists in text
    """
    pattern = r'\bbaca\s*juga\b[^a-zA-Z]*'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def apply_cleaning(row):
    text = row[config['text_col']]  # take text from configured column
    idx = row.name                  # .name gives row number
    cleaned_result = clean_text(text, row_index=idx)

    if cleaned_result:
        cleaned, truncated = cleaned_result
        baca_juga_found = detect_baca_juga(cleaned)
    else:
        cleaned = ""
        truncated = ""
        baca_juga_found = ""

    return pd.Series([cleaned, truncated, baca_juga_found])

def process_cleaning(input_folder, processed_folder, output_folder, text_col, cleaned_col, truncated_col, baca_juga_col):
    for filename in tqdm(os.listdir(input_folder), desc=f"Cleaning data", colour="green"):
        if filename.endswith('.csv'):
            filepath = os.path.join(input_folder, filename)
            df = pd.read_csv(filepath,quotechar='"', quoting=csv.QUOTE_ALL)
            df = df.replace(r'\n', ' ', regex=True)
            
            df[[cleaned_col, truncated_col, baca_juga_col]] = df.apply(apply_cleaning, axis=1)

            output_path = os.path.join(output_folder, f"output_{filename}")
            df.to_csv(output_path, index=False)
            shutil.move(filepath, os.path.join(processed_folder, filename))
            logging.info(f"Processed and moved file: {filename}")


if __name__ == "__main__":
    setup_logging()
    config = load_config()
    tqdm.pandas()
    process_cleaning(
        config['input_folder'], 
        config['processed_folder'], 
        config['output_folder'],
        config['text_col'],
        config['cleaned_col'],
        config['truncated_col'],
        config['baca_juga_col']
    )