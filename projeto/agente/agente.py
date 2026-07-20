import socket , psutil , json , sys , threading , time

####################################################################################################
# FUNÇÕES PRINCIPAIS
def info_geral(): # PRONTO
    # Obtenção de informação geral de processos do agente. G
    lista_info_geral = []

    # (---------------) (---------------) (---------------)
    try:
        pids = psutil.pids()
        for i in pids:
            lista_info_geral.append({ 'pid': i,'nome': psutil.Process(i).name() })
    except:
        lista_info_geral = []
        print("Info geral ocasionou ERRO. Enviando lista vazia")
    # (---------------) (---------------) (---------------)

    lista_info_geral_byt = json.dumps(lista_info_geral) # lista em json
    tam_inf_geral = len(lista_info_geral_byt) # len de json
    tam_inf_geral_byt = tam_inf_geral.to_bytes(4,ENDIANNESS) # len em 4 bytes
    
    try:
        sock.send(tam_inf_geral_byt) # send len de json
        sock.send(lista_info_geral_byt.encode(CODIFICACAO)) # send json
        print("Info geral executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def proc_especifico(): # PRONTO
    # Obtenção de dados de um processo específico. P
    parametro_byt = sock.recv(4) # recebem parametro adicional
    parametro = int.from_bytes(parametro_byt,ENDIANNESS)
    print(parametro,type(parametro))
    dicio_proc_esp = {}
    dicio_proc_esp_default = {'ok': False} # Usado caso processo não exista ou ocorra erro no agente.
    # (---------------) (---------------) (---------------)
    if psutil.pid_exists(parametro): # Checa existência do processo.
        print("OK, Processo encontrado.")
        try:                                                # print(dir((psutil.Process(parametro))))
            dicio_proc_esp['ok'] = True
            dicio_proc_esp['pid'] = parametro
            dicio_proc_esp['nome'] = psutil.Process(parametro).name()
            dicio_proc_esp['path'] = psutil.Process(parametro).exe()
            dicio_proc_esp['mem'] = round(psutil.Process(parametro).memory_percent(),2)
            dicio_proc_esp['cpu'] = psutil.Process(parametro).cpu_percent()
            dicio_proc_esp['connections'] = gera_net_con(parametro) # Função para esse
        except: # Exception as e:
            #erro = type(e).__name__
            print("Processo especifico ocasionou ERRO. Enviando dicionário vazio.")
            dicio_proc_esp = dicio_proc_esp_default
    else:
        print("Processo não encontrado.")
        dicio_proc_esp = dicio_proc_esp_default
    # (---------------) (---------------) (---------------)
    dicio_proc_esp_byt = json.dumps(dicio_proc_esp)
    tam_dicio = len(dicio_proc_esp_byt)
    tam_dicio_byt = tam_dicio.to_bytes(4,ENDIANNESS)

    try:
        sock.send(tam_dicio_byt) # send len de json
        sock.send(dicio_proc_esp_byt.encode(CODIFICACAO)) # send json
        print("Processo especifico executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def por_cpu_thread():
    global THREADON
    while THREADON:
        global LISTA_POR_CPU
        lista_anterior = LISTA_POR_CPU
        lista_por_cpu = []
        # (---------------) (---------------) (---------------)
        # Partes do Google
        try:
            procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    pinfo = proc.info
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=0.1)
                    procs.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            # Ordena os processos pelo uso de CPU (cpu_percent) em ordem decrescente
            top_5 = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:5]
            for r in top_5:
                lista_por_cpu.append({"pid":r['pid'],"perc":round(r['cpu_percent'],2)})
        except:
            print("Threas 5+ Por CPU ocasionou ERRO. Mantendo lista anterior")
            lista_por_cpu = lista_anterior
        # (---------------) (---------------) (---------------)
        LISTA_POR_CPU = lista_por_cpu

def por_cpu(): # PRONTO
    # Obtém informação sobre os cinco processos que mais estão usando a CPU. C
    '''lista_por_cpu = []
    # (---------------) (---------------) (---------------)
    # Partes do Google
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            pinfo = proc.info
            pinfo['cpu_percent'] = proc.cpu_percent(interval=0.1)
            procs.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Ordena os processos pelo uso de CPU (cpu_percent) em ordem decrescente
    top_5 = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:5]
    for r in top_5:
        lista_por_cpu.append({"pid":r['pid'],"perc":round(r['cpu_percent'],2)})
    # (---------------) (---------------) (---------------)'''

    lista_por_cpu = LISTA_POR_CPU
    lista_por_cpu_byt = json.dumps(lista_por_cpu) # em json
    tam_lista_por_cpu = len(lista_por_cpu_byt) # len
    tam_lista_por_cpu_byt = tam_lista_por_cpu.to_bytes(4,ENDIANNESS) # len em 4 bytes
    
    try:
        sock.send(tam_lista_por_cpu_byt) # send len de json
        sock.send(lista_por_cpu_byt.encode(CODIFICACAO)) # send json
        print("5+ Por CPU executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def por_mem(): # PRONTO
    # Obtém informação sobre os cinco processos que mais estão usando memória. M
    lista_por_mem = []
    # (---------------) (---------------) (---------------) # memory_percent era None para todos !!!
    # Partes do Google
    try:
        processos = []
        #ram_size = psutil.virtual_memory().total / (1024 * 1024) # Tamanho da ram em MB

        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                # Obtém o uso de memória (RSS) em bytes e converte para MB (Quantidade de RAM física real que um processo está consumindo no momento)
                memoria_rss = proc.info['memory_info'].rss / (1024 * 1024)
                processos.append({'pid': proc.info['pid'],'name': proc.info['name'],'memory_mb': (memoria_rss)})
                #processos.append({'pid': proc.info['pid'],'name': proc.info['name'],'memory_mb': (memoria_rss*100)/ram_size}) # Também faz porcentagem 
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        processos_ordenados = sorted(processos, key=lambda p: p['memory_mb'], reverse=True)
        for p in processos_ordenados[:5]: # Pegando os 5
            lista_por_mem.append({"pid":p['pid'],"perc":round(p['memory_mb'],2)})
        # (---------------) (---------------) (---------------)
    except:
        print("5+ Por MEM ocasionou ERRO. Enviando lista vazia")
        lista_por_mem = []
    
    lista_por_mem_byt = json.dumps(lista_por_mem) # em json
    tam_lista_por_mem = len(lista_por_mem_byt) # len
    tam_lista_por_mem_byt = tam_lista_por_mem.to_bytes(4,ENDIANNESS) # len em 4 bytes
    
    try:
        sock.send(tam_lista_por_mem_byt) # send len de json
        sock.send(lista_por_mem_byt.encode(CODIFICACAO)) # send json
        print("5+ Por MEM executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def hardware(): # PRONTO
    # Obtém informação sobre o hardware da máquina. H
    # Ao menos cinco (5) elementos
    dici_hard = []
    # (---------------) (---------------) (---------------)
    try:
        dici_hard.append({'os':sys.platform})
        dici_hard.append({'diskT':round((psutil.disk_usage("/").total) / (1024**3),2)})
        dici_hard.append({'diskU':round((psutil.disk_usage("/").used) / (1024**3),2)})
        dici_hard.append({'diskF':round((psutil.disk_usage("/").free) / (1024**3),2)})
        dici_hard.append({'diskP':(psutil.disk_usage("/").percent)})
        dici_hard.append({'ram':round(psutil.virtual_memory().total / (1024**3),2)})
        dici_hard.append({'cpuC':round((psutil.cpu_freq().current) / (1000),2)})
        dici_hard.append({'ip':socket.gethostbyname(socket.gethostname())})

        """
        dici_hard['os'] = sys.platform # Para não usar platform
        dici_hard['diskT'] = round((psutil.disk_usage("/").total) / (1024**3),2) # total
        dici_hard['diskU'] = round((psutil.disk_usage("/").used) / (1024**3),2) # used
        dici_hard['diskF'] = round((psutil.disk_usage("/").free) / (1024**3),2) # free
        dici_hard['diskP'] = (psutil.disk_usage("/").percent) # percent %
        dici_hard['ram'] = round(psutil.virtual_memory().total / (1024**3),2) # Tamanho da ram em GB
        dici_hard['cpuC'] = round((psutil.cpu_freq().current) / (1000),2) # Frequência atual da CPU em GB
        dici_hard['ip'] = socket.gethostbyname(socket.gethostname()) # IP
        """


    except:
        dici_hard = []
        print("hardware ocasionou ERRO. Enviando dicionário vazio")
    # (---------------) (---------------) (---------------)
    dici_hard_byt = json.dumps(dici_hard)
    tam_dici_hard = len(dici_hard_byt)
    tam_dici_hard_byt = tam_dici_hard.to_bytes(4,ENDIANNESS)

    try:
        sock.send(tam_dici_hard_byt) # send len de json
        sock.send(dici_hard_byt.encode(CODIFICACAO)) # send json
        print("Especs do hardware executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def hist_cpu(): # PRONTO
    # 
    lista_hist_cpu = LISTA_HIST_CPU_1M


    lista_hist_cpu_byt = json.dumps(lista_hist_cpu) # lista em json
    tam_lista_hist_cpu = len(lista_hist_cpu_byt) # len de json
    tam_lista_hist_cpu_byt = tam_lista_hist_cpu.to_bytes(4,ENDIANNESS) # len em 4 bytes
    
    try:
        sock.send(tam_lista_hist_cpu_byt) # send len de json
        sock.send(lista_hist_cpu_byt.encode(CODIFICACAO)) # send json
        print("HistCPU executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")

def f_eval():
    # M, C e H
    try:
        # M
        lista_por_mem = []
        # (---------------) (---------------) (---------------) # memory_percent era None para todos !!!
        try:
            processos = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    memoria_rss = proc.info['memory_info'].rss / (1024 * 1024)
                    processos.append({'pid': proc.info['pid'],'name': proc.info['name'],'memory_mb': (memoria_rss)})
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            processos_ordenados = sorted(processos, key=lambda p: p['memory_mb'], reverse=True)
            for p in processos_ordenados[:5]:
                lista_por_mem.append({"pid":p['pid'],"perc":round(p['memory_mb'],2)})
            # (---------------) (---------------) (---------------)
        except:
            print("5+ Por MEM ocasionou ERRO. Enviando lista vazia")
            lista_por_mem = []
        # H
        dici_hard = []
        # (---------------) (---------------) (---------------)
        try:
            dici_hard.append({'os':sys.platform})
            dici_hard.append({'diskT':round((psutil.disk_usage("/").total) / (1024**3),2)})
            dici_hard.append({'diskU':round((psutil.disk_usage("/").used) / (1024**3),2)})
            dici_hard.append({'diskF':round((psutil.disk_usage("/").free) / (1024**3),2)})
            dici_hard.append({'diskP':(psutil.disk_usage("/").percent)})
            dici_hard.append({'ram':round(psutil.virtual_memory().total / (1024**3),2)})
            dici_hard.append({'cpuC':round((psutil.cpu_freq().current) / (1000),2)})
            dici_hard.append({'ip':socket.gethostbyname(socket.gethostname())})
        except:
            dici_hard = []
            print("hardware ocasionou ERRO. Enviando dicionário vazio")
        # (---------------) (---------------) (---------------)

        eval_dicio = [{'ok': True,
                    'result':{ 'mem': lista_por_mem,
                                'cpu': LISTA_POR_CPU,
                                'har': dici_hard
                            }
                    }
                    ]
    except:
        eval_dicio = [{'ok': False, 'result': 'Erro da função eval'}]

    eval_dicio_byt = json.dumps(eval_dicio) # lista em json
    eval_dicio_byt = eval_dicio_byt.encode(CODIFICACAO) #lista json em bytes

    tam_eval_dicio_cpu = len(eval_dicio_byt) # len de json
    tam_eval_dicio_byt = tam_eval_dicio_cpu.to_bytes(4,ENDIANNESS) # len em 4 bytes

    try:
        sock.send(tam_eval_dicio_byt) # send len de json
        sock.send(eval_dicio_byt) # send json
        print("Eval executado com sucesso.")
    except:
        global ONOFF
        ONOFF = False
        print("Socket ocasionou ERRO. Saindo...")
    
####################################################################################################
# FUNÇÕES ADICIONAIS

def pedido():
    pedido_byt = sock.recv(1) # Apenas um byte
    if pedido_byt != b"":
        pedido = pedido_byt.decode(CODIFICACAO)
        print("O gerente requisita: ",pedido) # TESTE
        operacoes(pedido)
    else:
        global ONOFF
        ONOFF = False

        print("Possível ERRO no gerente.")
    #threading.Thread(target=operacoes , args=(pedido,)).start() # Não posso usar threads, pois é uma única conexão. ???

def operacoes(op):
    match op:
        case "G": 
            info_geral()
        case "P": 
            proc_especifico()
        case "C": 
            por_cpu()
        case "M": 
            por_mem()
        case "H": 
            hardware()
        case "I":
            hist_cpu()
        case "E":
            f_eval()
        #case "T":
            #print("Teste de conexão.")
        #case "Q":
            #desconecta()
        case _:
            print("Opção inválida!") # Não deve ocorrer, tratamento dos possiveis ocorre no gerente.

def desconecta():
    global ONOFF
    ONOFF = False
    print("Gerente requisita desconexão!")

def gera_net_con(parametro):
    lista_connections = []
    #parametro = int(input("Digite um pid: ")) # TESTE

    try:
        for net_cons in (psutil.net_connections(kind='tcp')):
            if net_cons.pid == parametro:
                #lista_temp = []
                #for i in net_cons.raddr: 
                    #lista_temp.append(i)
                try:
                    #lista_connections.append({"remote":lista_temp[0],"status":net_cons.status})
                    lista_connections.append({"remote":net_cons.raddr[0],"status":net_cons.status})
                except: pass
                #print(lista_temp)
                #lista_temp = []
    except:
        lista_connections = []
        print("gera net conecctions ocasionou ERRO. retornando lista vazia.")
    #print(lista_connections)
    #for j in lista_connections: print(j)
    return lista_connections # Retorna lista de conexões
# Função copiada do google, MÁS ADAPTADA.

def get_top_cpu_processes(limit,TOP_CPU_TEMPO): # Função copiada do google, MÁS ADAPTADA.
    global THREADON
    while THREADON:
        global LISTA_HIST_CPU_1M
        """Retorna os top processos por uso de CPU no último minuto."""
        
        # Coleta inicial dos tempos de CPU de todos os processos
        processes_before = {}
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # cpu_times() retorna segundos de tempo de sistema/usuário
                processes_before[proc.info['pid']] = {
                    'proc': proc,
                    'times': proc.cpu_times()
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Aguarda 60 segundos para medir o intervalo
        #print("Monitorando uso de CPU por 60 segundos...")
        time.sleep(TOP_CPU_TEMPO) ########################################################################################## Teste

        processes_after = []
        
        # Compara tempos de CPU
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                if pid in processes_before:
                    # Calcula a diferença entre os tempos
                    before = processes_before[pid]['times']
                    after = proc.cpu_times()
                    
                    # Tempo total de CPU = Tempo de Usuário + Tempo de Sistema
                    total_time_before = before.user + before.system
                    total_time_after = after.user + after.system
                    
                    # Delta de tempo de CPU usado
                    cpu_delta = total_time_after - total_time_before
                    
                    # cpu_delta / 60 segundos dá a média no minuto
                    cpu_percent = (cpu_delta / 60) * 100
                    
                    processes_after.append({
                        'pid': pid,
                        'name': proc.info['name'],
                        'cpu_usage': round(cpu_percent,2) # DUAS CASAS DECIMAIS
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Ordena os processos pelo uso de CPU em ordem decrescente
        top_processes = sorted(processes_after, key=lambda x: x['cpu_usage'], reverse=True)

        LISTA_HIST_CPU_1M = top_processes[:limit] # UPDATE MINHA LISTA

####################################################################################################
# Variáveis

HOST_default = "127.0.0.1"
PORTA = 45678
ENDIANNESS = "big"
CODIFICACAO = "utf-8"
ONOFF = True
LISTA_HIST_CPU_1M = [] # Atualizada constantemente por uma thread
TOP_CPU_NUM = 10 # N processos no último minuto
TOP_CPU_TEMPO = 60 # Tempo de monitoramento, deve ser 60
THREADON = True # Faz loop da trhead parar
LISTA_POR_CPU = [] # Atualizada constantemente por uma thread

####################################################################################################
# Argv

#conectando ao servidor
conectado = False

parametros = sys.argv

while not conectado:
    try:
        if len(parametros) == 2:
            HOST = parametros[1]

        elif len(parametros) == 1:
            HOST = input("Digite o IP: ")
            if HOST == 'exit':
                sys.exit()

        else:
            sys.exit("Entrada invalida, insira após um espaço o IP no seguinte formato: 127.0.0.1 e apena isso.")

        print(f"Conectando-se ao Host: {HOST}, na Porta: {PORTA}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, int(PORTA)))
        conectado = True

        print(f'Conectado ao servidor com sucesso!')
        print(f'HOST: {HOST}, PORTA: {PORTA}')


    except SystemExit:
        sys.exit()

    except Exception as e:
        print('Não foi possível fazer a conexão com esse ip, tente novamente: ')
        parametros = parametros[:1]



####################################################################################################
"Inicio"
tr_cpu = threading.Thread(target=get_top_cpu_processes, args=(TOP_CPU_NUM,TOP_CPU_TEMPO,)).start()
top_cpu = threading.Thread(target=por_cpu_thread, args=()).start()

while ONOFF:
    pedido()

sock.close()
THREADON = False

print("Encerrando o agente!")
print("Encerrando threads...")