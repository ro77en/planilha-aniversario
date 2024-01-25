import pandas as pd
from datetime import datetime

df = pd.read_pickle('aniversarios.pkl')
hoje = datetime.now().date()

aniversariantes = df[ df['DATA'] == hoje]
print(aniversariantes)