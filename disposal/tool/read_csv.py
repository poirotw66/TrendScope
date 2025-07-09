import pandas as pd

df = pd.read_csv('data/sheet/consensus_2025.csv', encoding='ISO-8859-1')
print(df.head(5))
output_file = 'data/sheet/consensus_2025_utf8.csv'
df.to_csv(output_file, encoding='utf-8', index=False)
# {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
# import chardet

# with open('data/sheet/consensus_2025.csv', 'rb') as f:
#     raw = f.read()
#     result = chardet.detect(raw)
#     print(result)