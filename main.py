import pandas as pd
from datetime import datetime
import win32com.client as win32
from PIL import Image, ImageDraw, ImageFont

def send_birthday_email(lista_emails):
    outlook = win32.Dispatch('outlook.application')

    for email_address in lista_emails:
        email = outlook.CreateItem(0)
        email.Subject = 'Hoje tem Festa!'
        email.HTMLBody = """ """
        email.To = email_address
        #email.Send()

def formatar_texto_cartao(df_aniversariantes):
    for i, linha in df_aniversariantes.iterrows():
        nome_completo = linha['NOME'].split()
        nome_formatado = ' '.join([nome_completo[0], nome_completo[-1]])
        setor = linha['SETOR']
        texto_cartao = ' - '.join([nome_formatado, setor])
        return texto_cartao
    
def obter_dimensoes_texto(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

def criar_cartao(texto, cartao_niver, post_it):
    pass

df = pd.read_pickle('aniversarios.pkl')
hoje = datetime.now().date()

print(df)

df.iloc[5,1] = hoje

aniversariantes = df[ df['DATA'] == hoje]
print(aniversariantes)

if not aniversariantes.empty:
    lista_emails = df['EMAIL'].tolist()
    send_birthday_email(lista_emails)

texto_cartao = formatar_texto_cartao(aniversariantes)
print(texto_cartao)
