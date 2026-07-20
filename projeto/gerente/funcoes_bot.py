import requests

#funções próprias
import mensagens
import gerente
import mytokens

"""
- fazer o retorno das funções do gerente
- fazer todos os retornos dos agentes voltarem com um padrão de json

"""

#função vai extrair as informações importantes da requisição feita com as mensagens do bot
def extraindo_info(result):
    try:
        #informações necessárias para usar no código
        global update_id, text, chat_id, message_id, first_name, person_id, message_id

        #vai servir para não puxar todas as mensagens anteriores
        update_id = result['update_id']
        message_info = result['message']
        message_id = message_info['message_id'] #saber se é a primeira mensagem do chat, se sim, perguntar se autoriza ou não
        person_id = message_info['from']['id'] #limitar para quem vai enviar
        text = message_info['text'] #mensagem enviada
        chat_info  = message_info['chat']
        chat_id    = chat_info['id'] #serve para mandar a mensagem de resposta
        first_name = chat_info['first_name']  #personalizar mensagem e saber para quem dar autorização

        print(update_id, person_id, text, chat_id )

        #só manda mensagens para autorizados
        admin_id = admins.values()
        if chat_id in admin_id:
            print('autorizado')
            return True
        elif (chat_id not in admin_id) and (message_id < 10):
            print('pedindo autorização')
            autoriza(1)
            return False

        return True

    except Exception as e:
        erro = type(e).__name__
        print('Erro na função extraindo_info\nErro: ', erro)

def valida_ip(ip):
    if ip.count('.') != 3:
        return False
    
    for octeto in ip.split('.'):
        if int(octeto) < 0 or int(octeto) > 255:
            return False
    return ip

def converte_comando(comando_bot):
    #se der errado a conversão ou o código, será enviado o comandos de menu novamente.
    try:
        #comando_bot = ['comando', 'ip', 'pid']
        comandos_padrao = {
                        '/agentes' : 'A',
                        '/procs'   : 'G',
                        '/proc'    : 'P',
                        '/topcpu'  : 'C',
                        '/topmem'  : 'M',
                        '/histcpu' : 'I',
                        '/hardw'   : 'H',
                        '/eval'    : 'E'}
        #convertendo comando
        comando = comandos_padrao[comando_bot[0]]
        comando_bot[0] = comando
        #validando os comandos:
        #único comando que não precisa de parâmetro:
        if comando_bot[0] == 'A' and len(comando_bot) == 1:
            return comando_bot
        
        #único comando que precisa de 3 parâmetros: [comando, ip, pid]
        if comando_bot[0] == 'P':
            if len(comando_bot) == 3: 
                if valida_ip(comando_bot[1]) and comando_bot[2].isnumeric():
                    return comando_bot
                
            raise ValueError
            
        #os outros comando precisam de dois parâmetros: [comando, ip]
        if len(comando_bot) == 2:
            if valida_ip(comando_bot[1]):
                return comando_bot
            else:
                raise ValueError
        else:
            raise ValueError
        
    except: 
        return mensagens.mensagem_menu()

def autoriza(op = 0):
    global admins
    
    if op == 0:
        admins = {
            'Roberto Araujo'  : 5433464039,
            'Giuseppe Cadura' : 8283300756,

        }
        return admins
    
    if op == 1: #buscar autorização: 
        envia_mensagem(chat_id, 'Aguarde Autorização, mandando mensagem para o Admin...')

        pergunta = f'{first_name} está tentando acessar o seu bot. chat_id:{chat_id}'
        for admin_id in admins.values(): 
            envia_mensagem(admin_id, pergunta)
        return False


def envia_mensagem(chat_id, resposta):
    global conta
    partes = []
    #bot do telegram tem limite de caracter de 4.096, caso a mensagem seja maior que isso, elas serão enviadas em partes
    #seguindo tanto o limite de caracter quanto o limite da nossa mensagem gerado por um |
    
    limite = 4095

    if len(resposta) < limite: 
        #mandando mensagens de volta:
        dados = {"chat_id": chat_id, 'text': resposta}
        url = f'https://api.telegram.org/bot{mytokens.TELEGRAM_TOKEN}/sendMessage'
        r = requests.post(url, json=dados).json()
        if r['ok']:
            print('mensagem enviada com sucesso para: ', chat_id)
    
    else:
        while len(resposta) // limite:
            partes += [resposta[:limite]]
            resposta = resposta[limite:]
        if resposta:
            partes += [resposta]

        for parte in partes:
            #as mensagens vão ser mandadas apenas com separação de limite, são 4h e 21min
            dados = {"chat_id": chat_id, 'text': parte}
            url = f'https://api.telegram.org/bot{mytokens.TELEGRAM_TOKEN}/sendMessage'
            r = requests.post(url, json=dados).json()
            if r['ok']:
                print('mensagem enviada com sucesso para: ', chat_id)

    return True


def recebendo_mensagens():
    global update_id, admins
    update_id = 0

    #retorna um dicionário com as pessoas que tem autorização para enviar o código
    #verifica se o id da mensagem é a que tem salva no dicionário
    admins = autoriza()

    while True:
        updates = {'offset' : update_id+1}
        url = f'https://api.telegram.org/bot{mytokens.TELEGRAM_TOKEN}/getUpdates'
        r = requests.post(url, json=updates).json()
        ok = r['ok'] #resultado da solicitação: True or False
        if ok:
            try:
                if r['result'] == []:
                    print('-'*50)
                    print('Conectado ao Telegram!\nEsperando mensagens...')
                    print('-'*50)
                else:
                    for result in r['result']: #r['result'] é uma lista com as mensagens do telegram

                        if extraindo_info(result): #a extração fica com variáveis globais usadas durante o resto do código
                            comando_bot = converte_comando(text.split())
                            if comando_bot.__class__ == list:
                                
                                resposta = gerente.chama_gerente(comando_bot)
                                print('funcoes bot reposta: ', resposta) #mostrar mensagem no terminal para debug
                                resposta = mensagens.formata_mensagem(resposta, comando_bot) #função tratar resposta antes de mandar

                                envia_mensagem(chat_id, resposta)
                            elif comando_bot.__class__ == str:
                                envia_mensagem(chat_id, comando_bot)

            except Exception as e:
                erro = type(e).__name__
                print('Erro na função recebendo_mensagens\nErro', erro)

        else:
            print('A solicitação está sendo retornada como False: ')
            print(r)

recebendo_mensagens()
