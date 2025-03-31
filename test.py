import pandas as pd
import os
import re

#read dataset
news_dataset = pd.read_csv(f"{os.getcwd()}/news_dataset.csv")
print(news_dataset["content"])

news_dataset['matches'] = news_dataset['content'].str.contains(r"(?i)\b(baca juga|advertisement|iklan)\b")
print(news_dataset['matches'].sum())
