import chardet
import pandas as pd
with open('./data/sheet/Consensus_HK_2025_sessions_20250520.csv', 'rb') as f:
    result = chardet.detect(f.read(100000))
    print(result)

df = pd.read_csv('./data/sheet/Consensus_HK_2025_sessions_20250520.csv', encoding=result['encoding'])
print(df.columns)
