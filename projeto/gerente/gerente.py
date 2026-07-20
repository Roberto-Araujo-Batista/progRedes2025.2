import socket , json , threading

####################################################################################################
# Funções gerente-agente
# FUNÇÕES PRINCIPAIS

DEBUG = True

def agentes():
    try:
        ip_json = [{'ok' : True, 'result': '' }]
        
        if AGENTES_CONECTADOS != []:
            #formatando o json
            result = {}
            result['total'] = len(AGENTES_CONECTADOS)
            #result = {'total': 5, 'maquina1': ip1, 'maquina2': ip2 ...} 

            maquina = 0
            while maquina < len(AGENTES_CONECTADOS):
                connect = AGENTES_CONECTADOS[maquina]
                ip = connect[1][0]
                result[f'maquina{maquina+1}'] = ip
                maquina += 1
            ip_json[0]['result'] = result 
        else:
            ip_json[0]['ok'] = False
            ip_json[0]['result'] = 'Não tem ninguém conectado'    
        
        print(ip_json)
        return ip_json
    
    except Exception as e:

        erro = type(e).__name__
        print('Erro na função agentes().\nErro: ', erro)

        ip_json[0]['ok'] = False
        ip_json[0]['result'] = f'Erro na função agentes().\nErro: {erro}'
        
        return ip_json

def procs(con): # PRONTO
    ### Obtenção de informação geral de processos do agente. G

    try: 
        # Recebe len e com o len recebe dados resultantes do pedido.
        len_byt = con.recv(4) # recebe len de json
        len = int.from_bytes(len_byt,ENDIANNESS)
        dados_byt = con.recv(len) # recebe json
        dados = json.loads(dados_byt) # json para lista

        print("Procs recebido.")
        return dados # Retorna uma lista
    except ConnectionResetError:
        dados = [{'result': 'conexão perdida'}]
        dados = json.loads(dados) 
        return dados
    
    except:
        print('erro na função procs')    


def proc(con,param): # 
    ### Obtenção de dados de um processo específico. P

    # Envia parametro adicional.
    parametro = int(param) # parametro tem que vir do telegram ______________________________________ 
    parametro_byt = int.to_bytes(parametro, 4)
    con.send(parametro_byt) # Envia parametro ao agente

    tam_dicio_byt = con.recv(4) # recebe len de json
    tam_dicio = int.from_bytes(tam_dicio_byt,ENDIANNESS)
    dados_byt = con.recv(tam_dicio) # recebe json
    dados = json.loads(dados_byt) # json para dicionário

    print("Processo especifico recebido.")
    return dados # Retorna um dicionário


def por_cpu(con): # PRONTO
    ### Obtém informação sobre os cinco processos que mais estão usando a CPU. C

    # Recebe len e com o len recebe dados resultantes do pedido.
    tam_lista_por_cpu_byt = con.recv(4) # recebe len de json
    tam_lista_por_cpu = int.from_bytes(tam_lista_por_cpu_byt,ENDIANNESS)
    lista_por_cpu_byt = con.recv(tam_lista_por_cpu) # recebe json
    lista_por_cpu = json.loads(lista_por_cpu_byt) # json para lista
    print("5+ Por CPU recebido.")
    return lista_por_cpu # Retorna uma lista

def por_mem(con): # PRONTO
    ### Obtém informação sobre os cinco processos que mais estão usando memória. M

    # Recebe len e com o len recebe dados resultantes do pedido.
    tam_lista_por_mem_byt = con.recv(4) # recebe len de json
    tam_lista_por_mem = int.from_bytes(tam_lista_por_mem_byt,ENDIANNESS) 
    lista_por_mem_byt = con.recv(tam_lista_por_mem)  # recebe json
    lista_por_mem = json.loads(lista_por_mem_byt) # json para lista

    print("5+ Por MEM recebido.")
    return lista_por_mem # Retorna uma lista

def hardware(con): # PRONTO
    ### Obtém informação sobre o hardware da máquina. H

    # Ao menos cinco (5) elementos
    tam_dici_hard_byt = con.recv(4) # recebe len de json
    tam_dici_hard = int.from_bytes(tam_dici_hard_byt)
    dici_hard_byt = con.recv(tam_dici_hard) # recebe json
    dici_hard = json.loads(dici_hard_byt) # json para lista

    print("Especs do hardware recebido.")
    return dici_hard # Retorna um dicionário

def hist_cpu(con): # 
    ### Lista os dez processos que mais usaram a CPU no último minuto. I

    # Recebe len e com o len recebe dados resultantes do pedido.
    lenH_byt = con.recv(4) # recebe len de json
    lenH = int.from_bytes(lenH_byt,ENDIANNESS)
    dadosH_byt = con.recv(lenH) # recebe json
    dadosH = json.loads(dadosH_byt) # json para lista

    print("HistCPU recebido.")
    return dadosH # Retorna uma lista

def eval(con):
    # Recebe len e com o len recebe dados resultantes do pedido.
    lenF_byt = con.recv(4) # recebe len de json
    lenF = int.from_bytes(lenF_byt,ENDIANNESS)
    dadosF_byt = con.recv(lenF) # recebe json
    dadosF = json.loads(dadosF_byt) # json para lista

    print("HistCPU recebido.")
    return dadosF # Retorna uma lista


# FUNÇÕES ADICIONAIS
def desconecta(con):
    global AGENTES_CONECTADOS
    print("Gerente requisitou a desconexão de: ",con)
    AGENTES_CONECTADOS.remove(con)
    con.close()

#Exibe no terminal os IPs e a porta que o agente está escutando
def ips_porta(Port):
    ips_ser = [addr[4][0] for addr in socket.getaddrinfo(socket.getfqdn(), 80, socket.AF_INET)]
    for ip in ips_ser:
        print (f"Escutando em: {ip} na porta: {Port}")

#função retorna a conexão certa procurando pelo ip
def encontra_connect(ip):
    try:
        #se a lista estiver vazia
        if AGENTES_CONECTADOS == []:
            return False

        for connect in AGENTES_CONECTADOS:
            cliente = connect[1]
            if ip == cliente[0]: #se ip de entrada == ao ip dentro da lista:
                return connect #vai sempre retornar a conexão completa, no retorno que vai escolher como mandar
        
        #se não encontrar o ip digitado
        return False
    
    except Exception as e:
        erro = type(e).__name__
        print('Erro na função encontra_connect().\nErro: ', erro)


#FUNÇÕES DE COMUNICAÇÃO

#só é chamada no código do bot.
def chama_gerente(comando_bot):
    try:
        con = True
        print('CHAMA GERENTE IS UP')
        #comando_bot = [comando, ip, pid]
        comando = comando_bot[0]
        if len(comando_bot) > 1:
            ip = comando_bot[1]
            connect = encontra_connect(ip) #função retorna a connect certa, retorna False caso não encontre o endereço

        if len(comando_bot) == 3:
            pid = comando_bot[2]

        if (con != False) and (comando != "A"):
            try:
                con = connect[0]
                con.send(comando.encode(CODIFICACAO)) #mandando a solicitação para o agente
                print('Solicitação enviada com sucesso!')
            except ConnectionResetError:
                print('O agente foi desconectado!')
                #remover conexão da lista
                AGENTES_CONECTADOS.remove(connect)
                return [{'ok': False, 'result': 'O agente solicitado foi desconectado'}]
            
            except Exception as e:
                erro = type(e).__name__
                print('erro ao tentar manda solicitação na função chama_gerente', erro)
        else:
            return agentes() #retorna os agentes disponíveis, porém está retornando com a formatação de mensagem de outro comando

        if comando == 'A':
            return agentes()
        if comando == 'G':
            return procs(con)
        if comando == 'P':
            return proc(con, pid)
        if comando == 'C':
            return por_cpu(con)
        if comando == 'M':
            return por_mem(con)
        if comando == 'I':
            return hist_cpu(con)
        if comando == 'H':
            return hardware(con)
        if comando == 'E':
            return eval(con)
        
        print('Essa função não existe')


            
    except Exception as e:
        erro = type(e).__name__
        print('Erro na função chama_gerente.\nErro', erro)


#isso tem que estar rolando em uma threading para outros computadores estarem conectados independente dos pedidos
def connecting():
    global AGENTES_CONECTADOS

    len_agentes = 0
    aux = len_agentes
    while True:
        try:
            con , cliente = sockG.accept()

            print("Conectado com: " , cliente)


            #formato da lista AGENTES_CONECTADOS = [('con', ('ip', porta)),   ('con2', ('ip2', porta2))]
            AGENTES_CONECTADOS.append((con, cliente))
            len_agentes = len(AGENTES_CONECTADOS)
            if len_agentes != aux:
                print('NOVA CONEXÃO', cliente, '\nCONECTADOS: ', len_agentes)
                aux = len_agentes

        except Exception as e:
            erro =  type(e).__name__
            print('Erro na função main().\nErro: ', erro)




def configurando_socket():
    #Deixando servidor up to connections
    global ENDIANNESS, CODIFICACAO, AGENTES_CONECTADOS, sockG
    # Variáveis
    HOST_default = ""
    PORTA = 45678
    ENDIANNESS = "big"
    CODIFICACAO = "utf-8"
    AGENTES_CONECTADOS = []

    #mostra os ips do servidor que estão abertos a conexão
    ips_porta(PORTA)

    try:
        #configurando socket
        sockG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockG.bind((HOST_default,PORTA))
        sockG.listen(1)

        print("Esperando conexão ... ...")

        threading.Thread(target=connecting).start()

    except Exception as e:
        erro = type(e).__name__
        print('Erro na função configurando_socket.\nErro: ', erro)

configurando_socket()