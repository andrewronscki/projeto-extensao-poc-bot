import requests
import time
import json
import os

class TelegramBot:
  def __init__(self):
    token = 'SEU TOKEN TELEGRAM'
    self.baseUrl = f'https://api.telegram.org/bot{token}/'
    
  def Start(self):
    update_id = None
    while True:
      update = self.get_messages(update_id)
      messages = update['result']
      if messages:
        for message in messages:
          update_id = message['update_id']
          chat_id = message['message']['from']['id']
          isFirstMessage = message['message']['message_id'] == 1
          responseToMessage = self.create_response(message, isFirstMessage)
          self.response(responseToMessage, chat_id)

    
  def get_messages(self, update_id):
    link_request = f'{self.baseUrl}getUpdates?timeout=100'
    if update_id:
      link_request = f'{link_request}&offset={update_id + 1}'
    result = requests.post(link_request)
    return json.loads(result.content)

  def create_response(self, message, isFirstMessage):
    message = message['message']['text']

    if isFirstMessage == True or message.lower() == 'menu':
      return f'''Olá bem vindo a nossa lanchonete. Digite o número do hamburguer que gostaria de pedir{os.linesep}1 - Queijo MAX{os.linesep}2 - Duplo Burguer Bacon{os.linesep}3 - Triple X'''
    if message == '1':
      return f'''Queijo Max - R$ 20,00{os.linesep}Confirmar pedido(s/n)?'''
    if message == '2':
      return f'''Duplo Burguer Bacon - R$ 25,00{os.linesep}Confirmar pedido(s/n)?'''
    if message == '3':
      return f'''Triple X - R$ 30,00{os.linesep}Confirmar pedido(s/n)?'''
    if message.lower() in ('s', 'sim'):
      return 'Pedido confirmado!'
    else:
      return 'Gostaria de acessar o menu? Digite "menu"'

  def response(self, responseToMessage, chat_id):
    content = {
      'chat_id': chat_id,
      'text': responseToMessage
    }
    link_to_send = f'{self.baseUrl}sendMessage'
    requests.post(link_to_send, content)

bot = TelegramBot()
bot.Start()
  