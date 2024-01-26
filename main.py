import pandas as pd
from datetime import datetime
import win32com.client as win32

def send_birthday_email(lista_emails):
    outlook = win32.Dispatch('outlook.application')

    for email_address in lista_emails:
        email = outlook.CreateItem(0)
        email.Subject = 'Hoje tem Festa!'
        email.HTMLBody = """ """
        email.To = email_address
        #email.Send()


df = pd.read_pickle('aniversarios.pkl')
hoje = datetime.now().date()

df['EMAIL'] = [f'colaborador{i}@gmail.com' for i in range( len(df) )]

print(df)

df.iloc[5,1] = hoje

aniversariantes = df[ df['DATA'] == hoje]
print(aniversariantes)

if not aniversariantes.empty:
    lista_emails = df['EMAIL'].tolist()
    send_birthday_email(lista_emails)
