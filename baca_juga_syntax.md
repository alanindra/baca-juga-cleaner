## The syntactic constructions of `"baca juga"` constituents

These rules are derived from empirical observation of typical constructions used in news media. More detailed analysis can be found [here](https://github.com/alanindra/baca-juga-cleaner/blob/main/analysis.ipynb).

### 1. Syntax classification
Each syntax construction follows the format [Class][Patterns], where:
- Class
  - **1**:
  - **2**:
  - **3**:
- Patterns:
  - **A**:

### 2. General rules and observations

- Constituents are extracted from the immediate right context of the `"baca juga"` string, limited to a maximum of three sentence tokens
- Constituents are predominantly short in length.
- Constituents are considered definitively irrelevant if they satisfy syntax 1A, i.e., all three of the following:
  - Begin with `"baca juga"`
  - Contain consecutive word-initial capitalization (e.g., "Cara Dapat Saldo")
  - End with an exclamation mark

### 3. Short-length constituents

Short constituents (≤ 10 words) are considered irrelevant when matching the following:

- **1A**: Start with `"baca juga"`, contain consecutive capitalized words, and end with *"!"*
- **1B**: End with *"!"*, and either start with *"baca juga"* or contain capitalized words
- **1C**: Start with `"baca juga"` only
- **1D**: Contain capitalized words only
- **1E**: End with *"!"* only

### 2. Medium-Length Constituents

Medium-length constituents (11–35 words) often include irrelevant segments and are processed as follows:

- **2A**: Start with `"baca juga"`, contain capitalized words, and end with *"!"*
- **2B**: End with *"!"* and either start with *"baca juga"* or contain capitalized words
- **2C**: Start with `"baca juga"`
- **2D**: Contain consecutive word-initial capitalized words

### 3. Long-Length Constituents

Some long constituents (> 35 words) are still filtered if they meet:

- **3C**: Start with `"baca juga"`
- **3D**: Contain capitalized clusters + common lexical triggers, e.g. `"cek"`, `"klaim`, etc.

### 4. Relevant Constituents or Rare Cases

- Segments in criteria such as **2E**, **4C** are considered *relevant* and preserved.
- Segments falling under **3A**, **3B**, **3E**, **4A**, **4B** are *rarely occurring* and are evaluated manually.
- A fallback method is implemented to detect unmatched *"baca juga"* strings for manual review.

This syntactic framework underpins the rule-based removal process for cleaning Indonesian news text data. The criteria, e.g. 1A are derived from empirical observation avaiable on [here](https://github.com/alanindra/baca-juga-cleaner/blob/main/analysis.ipynb).

### Original vs cleaned syntactic forms of `"baca juga"` constituents
