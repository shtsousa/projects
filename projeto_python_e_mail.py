# -*- coding: utf-8 -*-
"""Projeto Python E-mail.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wcLTBwXy_ciFauaD-bbC4ZXTo4QIXW9E

Desafio:
Você faz parte da equipe de Analytics de uma grande marca de vestuário com mais de 25 lojas espalhadas em Shoppings de todo o Brasil.

Toda semana você precisa enviar para a diretoria um ranking atualizado com as 25 lojas contendo 3 informações:

Faturamento de cada Loja
Quantidade de Produtos Vendidos de cada Loja
Ticket Médio dos Produto de cada Loja
Além disso, cada loja tem 1 gerente que precisa receber o resumo das informações da loja dele. Por isso, cada gerente deve receber no e-mail:

Faturamento da sua loja
Quantidade de Produtos Vendidos da sua loja
Ticket Médio dos Produto da sua Loja
Esse relatório é sempre enviado como um resumo de todos os dados disponíveis no ano.

Passo a passo da construção do código:
- Passo 1: Importar a base de dados
- Passo 2: Calcular o faturamento de cada Loja
- Passo 3: Calcular a quantidade de produtos vendidos de cada Loja
- Passo 4: Calcular o Ticket Médio de cada Loja
- Passo 5: Enviar e-mail para diretoria 
- Passo 6: Enviar e-mail para cada loja

Passo 1: Importar base de Dados
"""

import pandas as pd

tabela_vendas = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/Vendas.xlsx")
display(tabela_vendas)

"""Passo 2: Calcular o faturamento da Loja"""

tabela_faturamento = tabela_vendas[["ID Loja","Valor Final"]].groupby("ID Loja").sum()
tabela_faturamento = tabela_faturamento.sort_values(by="Valor Final",ascending=False)
display(tabela_faturamento)

"""Passo 3: Calcular a quantidade de produto vendido em cada loja"""

tabela_quantidade = tabela_vendas[["ID Loja","Quantidade"]].groupby("ID Loja").sum()
tabela_quantidade = tabela_quantidade.sort_values(by="Quantidade",ascending=False)
display(tabela_quantidade)

"""Passo 4: Calcular o Ticket Médio"""

ticket_medio = (tabela_faturamento["Valor Final"] / tabela_quantidade["Quantidade"]).to_frame()
ticket_medio = ticket_medio.rename(columns={0:"Ticket Medio"})
display(ticket_medio)

"""Função Enviar E-mail"""

def enviar_email(nome_da_loja, tabela):
  import smtplib
  import email.message

  server = smtplib.SMTP('smtp.gmail.com:587')  
  corpo_email = f"""
  <p>Prezados,</p>
  <p>Segue relatório de vendas</p>
  {tabela.to_html()}
  <p>Qualquer dúvida, estou a disposição</p>  
  """ #vamos editar
    
  msg = email.message.Message()
  msg['Subject'] = f"Relatório de Vendas - {nome_da_loja}" #vamos editar    
  msg['From'] = 'samuelhtsousa@gmail.com' #vamos editar
  msg['To'] = 'samuamgs@gmail.com' #vamos editar
  password = "93537054sh" #vamos editar
  msg.add_header('Content-Type', 'text/html')
  msg.set_payload(corpo_email )
    
  s = smtplib.SMTP('smtp.gmail.com: 587')
  s.starttls()
  # Login Credentials for sending the mail
  s.login(msg['From'], password)
  s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
  print('Email enviado')

"""Passo 5: Enviar-email

"""

tabela_completa = tabela_faturamento.join(tabela_quantidade).join(ticket_medio)
enviar_email("Diretoria",tabela_completa)
display(tabela_completa)

"""Passo 6: Enviar e-mail para cada loja"""

lista_lojas=tabela_vendas["ID Loja"].unique()

for loja in lista_lojas:
  tabela_loja = tabela_vendas.loc[tabela_vendas["ID Loja"] == loja, ["ID Loja", "Quantidade", "Valor Final"]]
  tabela_loja = tabela_loja.groupby("ID Loja").sum()
  tabela_loja["Ticket Medio"] = tabela_loja["Valor Final"] / tabela_loja["Quantidade"]
  enviar_email(loja, tabela_loja)
