import llm_eval


DEBUG = False

def mensagem_menu():
    return'''
Óla, esses são os nossos comandos:

/agentes
Lista os IPs das máquinas que possuem agentes de monitoramento instalados na rede local.

/procs <IP>
Mostra todos os processos em execução na máquina informada (quantidade, PID e nome).

/proc <IP> <PID>
Exibe detalhes de um processo específico: PID, nome, uso de memória (MB) e uso de CPU (%).

/topcpu <IP>
Lista os 5 processos que mais consomem CPU na máquina, com seus percentuais.

/topmem <IP>
Lista os 5 processos que mais consomem memória na máquina, com o valor usado.

/histcpu <IP>
Mostra os 10 processos que mais usaram CPU no último minuto (coleta a cada 5s).

/hardw <IP>
Exibe informações sobre o hardware da máquina (CPU, memória, disco etc.).

/eval <IP>
Solicita a uma LLM (ex.: Gemini) uma análise da situação da máquina, considerando dados de uso de CPU, memória e hardware. O resultado da avaliação é devolvido ao usuário.
'''

def formata_eval(resposta):
    return 'formata bonitinho o eval e retorna a função da analise de llm'


#resultado deve retornar algo parecido com isso:

'''
  **Relatório de Monitoramento**
    {função tal}
  
  **MEMÓRIA:**
- PID: 21545 | PER: 21145 | Nome: 4444
- PID: 21545 | PER: 21145 | Nome: 4444
- PID: 21545 | PER: 21145 | Nome: 4444

 **CPU:**
- PID: 21545 | PER: 21145 | Nome: 4444
- PID: 21545 | PER: 21145 | Nome: 4444
- PID: 21545 | PER: 21145 | Nome: 4444

 __Pronto para outro comando!__
'''

def formata_mensagem(resposta, comando_bot):
    try:
        resultado = '' #str com resposta de retorno
        comando = comando_bot[0]
        

        #formata função com json estilo telegram
        '''
        [{   'ok': True, 'result': 'resultado'}
        ]
        '''
        if comando == 'A': 
            dic = resposta[0]
            if dic['ok'] == True:
                result = dic['result']
                for maquina in result.keys():
                    resultado = resultado + f'{maquina} = {result[maquina]}\n'
            if dic['ok'] == False:
                resultado = dic['result']
            
            return resultado
        

        #formatar função especial P
        '''
        {
            “ok”: True/False 
            “pid”: NUM,
            “nome”: TEXTO,
            “path”: NOME,
            “mem”: NUM,
            “cpu”: NUM,
            “connections”:  [ 
                {“remote”: IP, “status”: TEXT},
                {“remote”: IP, “status”: TEXT},
                ...
                ]
            }
        '''
        # Lista de connections
        if comando == 'P':
            resultado += "\n"
            if resposta['ok']:
                resultado += f"OK = {resposta['ok']}\n"
                resultado += f"PID = {resposta['pid']}\n"
                resultado += f"NOME = {resposta['nome']}\n"
                resultado += f"PATH = {resposta['path']}\n"
                resultado += f"MEM = {resposta['mem']}MB\n"
                resultado += f"CPU = {resposta['cpu']}%\n"
                
                for iten in resposta['connections']:
                    for key in iten.keys():
                        resultado += f"{key} = {iten[key]} | "
                
            else:
                resultado += "OK = " + resposta['ok']
            resultado += '\n'
            return resultado


        #formata função i histcpu
        '''
        [
        {'pid': 0, 'name': 'System Idle Process', 'cpu_usage': 602.53}, 
        {'pid': 6980, 'name': 'Discord.exe', 'cpu_usage': 65.34}
        ]'''
        if comando == 'I':
            for processos in resposta:
                resultado += '\n' 
                for key in processos.keys():
                    resultado += f' {key} = {processos[key]}'
                    if key == 'cpu_usage':
                        resultado += "MB |"
                    else:
                        resultado += ' |' 
            resultado += '\n'
            return resultado
            #return 'função i toda bonitinha'
        



        #formata função com lista estilo roteiro de atividade
        '''
            [ 
            {“pid”: NUM, “nome”: TEXTO},
            {“pid”: NUM, “nome”: TEXTO},
            ]
        '''
        if comando == 'G' or comando == 'C' or comando == 'M' or comando == 'H':
            for processos in resposta:
                resultado += '\n' 
                for key in processos.keys():
                    resultado += f'{key} = {processos[key]} | '
            resultado += '\n'
            return resultado
        

        

        #formatar função eval
        '''
        [{'ok': True, 'result': {'mem': [{'pid': 2076, 'perc': 640.4}, {'pid': 6980, 'perc': 505.64}, {'pid': 15096, 'perc': 467.48}, {'pid': 16732, 'perc': 397.99}, 
        {'pid': 10504, 'perc': 353.37}], 'cpu': [{'pid': 0, 'perc': 617.3}, {'pid': 14960, 'perc': 108.7}, {'pid': 13672, 'perc': 58.1}, {'pid': 7580, 'perc': 15.6}, 
        {'pid': 6980, 'perc': 15.5}], 'har': [{'os': 'win32'}, {'diskT': 318.62}, {'diskU': 97.05}, {'diskF': 221.57}, {'diskP': 30.5,} {'ram': 7.9}, {'cpuC': 1.79}, 
        {'ip': '192.168.56.1'}]}}]
        
        '''

        if comando == 'E':
            #vai chamar uma função para formata especialmente a eval e chamar uma llm
            resultado += "MEMÓRIA:"+"\n"
            for mem in resposta[0]['result']['mem']:
                resultado += '\n'
                for key in mem.keys():
                    resultado += f"{key} = {mem[key]} | "
            resultado += "\n"
            resultado += "CPU:"+"\n"
            for mem in resposta[0]['result']['cpu']:
                resultado += '\n'
                for key in mem.keys():
                    resultado += f"{key} = {mem[key]} | "
            resultado += "\n"
            resultado += "HARDWARE:"+"\n"
            for mem in resposta[0]['result']['har']:
                resultado += '\n'
                for key in mem.keys():
                    resultado += f"{key} = {mem[key]} | "
            resultado += "\n"
            
            resultado = llm_eval.llm_responde(resultado)
            return resultado  


    except Exception as e:
        erro = type(e).__name__
        resultado = f'Erro na função mensagens.formatar_mensagem()\nErro: {erro}'
        print(resultado)
        return resultado



if DEBUG:
    print(formata_mensagem([{   'ok': True, 'result': 'resultado'}],"A"))
    print('*'*85)
    var1 = [
            {
            'ok': True, 'result': {
                                    'mem': [{'pid': 2076, 'perc': 640.4}, {'pid': 6980, 'perc': 505.64}, {'pid': 15096, 'perc': 467.48}, {'pid': 16732, 'perc': 397.99}, 
            {'pid': 10504, 'perc': 353.37}], 
            
            'cpu': [{'pid': 0, 'perc': 617.3}, {'pid': 14960, 'perc': 108.7}, {'pid': 13672, 'perc': 58.1}, {'pid': 7580, 'perc': 15.6}, 
            {'pid': 6980, 'perc': 15.5}], 
            
            'har': [{'os': 'win32'}, {'diskT': 318.62}, {'diskU': 97.05}, {'diskF': 221.57}, {'diskP': 30.5}, {'ram': 7.9}, {'cpuC': 1.79}, {'ip': '192.168.56.1'}]}
            }
            ]
    print(formata_mensagem(var1,'E'))
    print('*'*85)

    var2 = {
            'ok': True ,
            'pid': 12 ,
            'nome': 'opera',
            'path': 'opera.exe',
            'mem': 550,
            'cpu': 5,
            'connections':  [ 
                {'remote': '192.168.0.2', 'status': 'conected'},
                {'remote': '192.168.0.254', 'status': 'conected'},
            ]}
    print(formata_mensagem(var2,'P'))
    print('*'*85)
    print(formata_mensagem([{'pid': 0, 'name': 'System Idle Process', 'cpu_usage': 602.53}, {'pid': 6980, 'name': 'Discord.exe', 'cpu_usage': 65.34}  ],'I'))
    print('*'*85)
    print(formata_mensagem([{'pid': 545454, 'nome': 'fakfhak'},{'pid': 454564, 'nome': 'TEXTO'},{'pid': 123, 'nome': 'plain'}],'G'))
    print('*'*85)
