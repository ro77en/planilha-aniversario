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
    texto_cartao = []
    for i, linha in df_aniversariantes.iterrows():
        nome_completo = linha['NOME'].split()
        nome_formatado = ' '.join([nome_completo[0], nome_completo[-1]])
        setor = linha['SETOR']
        aniversariante = ' - '.join([nome_formatado, setor])
        texto_cartao.append(aniversariante)
    return texto_cartao

    
def obter_dimensoes_texto(text_string, font):
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def criar_cartao(cartao_niver, post_it, fonte, texto_cartao):
    # cartão
    cartao_niver = cartao_niver.copy()
    post_it = post_it.copy()

    nova_largura = int(post_it.width * 1.5)
    nova_altura = int(post_it.height * 1.5)
    post_it = post_it.resize((nova_largura, nova_altura))

    
    # escrevendo texto
    draw_post_it = ImageDraw.Draw(post_it)
    posicao_y = 200
    for palavra in texto_cartao:
        x_text, y_text = obter_dimensoes_texto(palavra, fonte)
        x_post_it = ((nova_largura - x_text) // 2) + 8
        y_post_it = posicao_y
        print(f'Posição do texto: ({x_post_it}, {y_post_it}), Tamanho do texto: ({x_text}, {y_text})')
        draw_post_it.text((x_post_it, y_post_it), palavra, font=fonte, fill=(47,61,100))
        posicao_y += 10
        print(f'Nova posição Y: {posicao_y}')

    print('Visualização do post it antes da sobreposicao: ')
    post_it.show()
    img_camadas = sobrepor_camadas(cartao_niver, post_it)
    cartao_final = Image.alpha_composite(cartao_niver, img_camadas)
    post_it.save('post_it_editado.png')
    return (cartao_final)

def sobrepor_camadas(cartao_niver, post_it):
    layer = Image.new('RGBA', cartao_niver.size, (0,0,0,0))
    layer.paste(post_it, (1000,100))
    layer2 = layer.copy()
    layer2.putalpha(256)
    layer.paste(layer2, layer)
    return layer


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

cartao_niver = Image.open('cartao_niver.png')
fonte = ImageFont.truetype('FREESCPT.TTF', 55)
post_it = Image.open('post_it.png')


cartao_final = criar_cartao(cartao_niver, post_it, fonte, texto_cartao)
cartao_final.show()