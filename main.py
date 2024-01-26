import pandas as pd
from datetime import datetime

def send_email(aniversariantes):
    pass

df = pd.read_pickle('aniversarios.pkl')
hoje = datetime.now().date()

df['EMAIL'] = [f'colaborador{i}@gmail.com' for i in range( len(df) )]

print(df)

df.iloc[5,1] = datetime.now().date()

aniversariantes = df[ df['DATA'] == hoje]
print(aniversariantes)

if not aniversariantes.empty:
    pass
