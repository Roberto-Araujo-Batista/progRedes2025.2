## Sistema de monitoramento de máquinas da rede local usando Telegram. (100 pontos)

<hr/>

<p><strong>Contexto: </strong></p>

<p>O projeto proposto tem como objetivo desenvolver um sistema de monitoramento de máquinas em uma rede local, integrando agentes instalados nas estações com uma estação de gerência e um bot no Telegram para interação do usuário. A atividade insere-se no contexto da disciplina de Programação de Computadores, permitindo aplicar conceitos de comunicação em rede, uso de sockets TCP, coleta de métricas de processos e hardware com a biblioteca psutil, além da implementação de protocolos de troca de mensagens entre cliente e servidor. Dessa forma, os estudantes poderão vivenciar na prática o desenvolvimento de uma solução distribuída, que une programação, administração de sistemas e integração com ferramentas modernas de comunicação, reforçando competências essenciais para profissionais da área de Redes de Computadores.</p>

<hr/>

<p><strong>Objetivo: </strong></p>

<p>Fazer um sistema para monitoramento das estações em uma rede local. Nesse sistema haverá uma estação de gerência e uma ou mais máquinas que executam o agente.  A ideia é que o agente se conecte ao gerente e aceite pedidos de dados de monitoramento deste. O usuário deve obter os dados de monitoramento por meio de um bot Telegram. A arquitetura é como na Figura a seguir:</p>

<img width="1620" height="885" alt="540660670-7e9e55d9-0b15-426b-baec-0ab0684612ee" src="https://github.com/user-attachments/assets/e89e9241-bd5b-44da-b6c1-e94901270fd0" />

<p>A operação dos elementos na arquitetura deve ser assim:</p>

<ul>
  <li><strong>Bot TELEGRAM</strong>: Deve suportar os seguintes comandos:</li>
  <table>
    <tr>
      <th>Comando</th>
      <th>Finalidade</th>
    </tr>
    <tr><td><strong>/agentes</strong></td><td>deve apresentar os IPs das máquinas em que existem agentes de monitoramento instalados no segmento de rede local da estação de gerenciamento;</td></tr>
    <tr><td><strong>/procs</strong></td><td>recebe um IP (seguindo o comando, separado por espaço ) e lista o número de processos, o pid e o nome dos processos executando nessa máquina;</td></tr>
    <tr><td><strong>/proc</strong></td><td>recebe um IP e um PID (seguindo o comando, separados por espaço) e lista informações sobre o processo na máquina, como: o pid, o nome o uso de memória (em MB) e o uso da CPU (em percentual);</td></tr>
    <tr><td><strong>/topcpu</strong></td><td>recebe um IP e lista os cinco processos que mais estão usando a CPU na máquina, bem como os percentuais;</td></tr>
    <tr><td><strong>/topmem</strong></td><td>recebe um IP (seguindo o comando, separado por espaço) e lista os cinco processos que mais estão usando memória na máquina (bem como o valor usado);</td></tr>
    <tr><td><strong>/histcpu</strong></td><td>recebe um IP e lista os dez processos que mais usaram a CPU no último minuto, sendo uma coleta a cada 5 segundos;</td></tr>
    <tr><td><strong>/hardw</strong></td><td>recebe um IP e mostra informações sobre o hardware da máquina;</td></tr>
    <tr><td><strong>/eval</strong></td><td>recebe um IP e devolve o resultado de análise da situação da máquina por uma LLM (gemini, por exemplo). Nesse procedimento, envie as informações similares àquelas obtidas em <strong>/topmem</strong>, <strong>/topcpu</strong> e <strong>/hardw</strong> e solicite a avaliação à LLM – a resposta dela deve ser devolvida ao usuário. <strong>USAR REQUESTS PARA EFETUAR ESSA OPERAÇÃO JUNTO A UMA LLM.</strong></td></tr>
  </table>

  <p>&nbsp;</p>
  
  <li><strong>A estação de gerência</strong>:</li>
  <ul>   
    <li>Deve aceitar conexões dos agentes na porta 45678/TCP;</li>    
    <li>Deve buscar pedidos feitos ao telegram a cada 1s;</li>    
    <li>Deve manter uma <i>thread</i> aberta com cada agente, para obter os dados que requerem monitoramento contínuo;</li>    
    <li>Permitido o uso da biliobteca <strong>requests</strong> e demais bibliotecas básicas do Python, como: <strong>socket</strong>, <strong>os</strong>, <strong>sys</strong>, ...</li>    
    <li>NÃO será permitido o uso de biblioteca de terceiros tais como: <strong>python-telegram-bot</strong>, <strong>telebot</strong>, ...</li>    
  </ul>

  <p>&nbsp;</p>
  
  <li><strong>A estação com o agente</strong>:</li>
  <ul>    
    <li>Deve aceitar como parâmetro de linha de comando o IP da estação de gerenciamento;</li>    
    <li>Deve conectar na estação de gerenciamento na por 45678/TCP;</li>    
    <li>Deve aceitar pedidos da estação de gerenciamento;</li>    
    <li>Deve usar a biliobteca <strong>psutil</strong> para obter os dados de monitoramento e demais bibliotecas básicas do Python, como: <strong>socket</strong>, <strong>os</strong>, <strong>sys</strong>, ...</li>    
  </ul>

  <p>&nbsp;</p>

  <li><strong>O protocolo entre agente/gerente</strong>:</li>
  <ul>    
    <li>Estações de gerência e agente nunca devem cair por mensagens malformadas enviadas pelo outro lado da comunicação;</li>    
    <li>Nas comunicações, todos os números formados por mais de um byte devem usar a codificação <i>big endian</i>;</li>    
  </ul>

</ul>

<p>&nbsp;</p>
  
<p>Nos comandos abaixo os espaços e pulos de linha são para fins de apresentação, eles não existem nas mensagens.</p>

  <table>
    <tr>
      <th>Mensagem</th>
      <th>Explicação</th>
      <th>Pedido (parâmetros extras)</th>
      <th>Resposta</th>
    </tr>
    </tr>
    <tr>
      <td><strong>G</strong></td>
      <td>Obtenção de informação geral de processos do agente.</td>
      <td><strong><i>Nenhum</i></strong></td>
      <td>
        <strong><i>Tamanho</i></strong> → 4 bytes com o tamanho do JSON que imediatamente segue:<br/>
        <pre>[ 
  {“pid”: NUM, “nome”: TEXTO},
  {“pid”: NUM, “nome”: TEXTO},
  .... 
]</pre>      
      </td>
    </tr>
    <tr>
      <td><strong>P</strong></td>
      <td>Obtenção de dados de um processo específico.</td>
      <td><strong><i>pid (4 bytes)</i></strong> → o número de identificação do processo.</td>
      <td>
        <strong><i>Tamanho</i></strong> → 4 bytes com o tamanho do JSON que imediatamente segue:<br/>
        <pre>{
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
}</pre>
      “ok”  deve ser False se o processo não existe, situação em que os outros campos estarão ausentes.
      </td>
    </tr>
    <tr>
      <td><strong>C</strong></td>
      <td>Obtém informação  sobre os cinco processos que mais estão usando a CPU.</td>
      <td><strong><i>Nenhum</i></strong></td>
      <td>
        <strong><i>Tamanho</i></strong> → 4 bytes com o tamanho do JSON que imediatamente segue:<br/>
        <pre>[ 
  {“pid”: NUM, “perc”: NUM},
  {“pid”: NUM, “perc”: NUM},
  .... 
]</pre>      
      </td>
    </tr>
    <tr>
      <td><strong>M</strong></td>
      <td>Obtém informação sobre os cinco processos que mais estão usando memória.</td>
      <td><strong><i>Nenhum</i></strong></td>
      <td>
        <strong><i>Tamanho</i></strong> → 4 bytes com o tamanho do JSON que imediatamente segue:<br/>
        <pre>[ 
  {“pid”: NUM, “perc”: NUM},
  {“pid”: NUM, “perc”: NUM},
  .... 
]</pre>      
      </td>
    </tr>
    <tr>
      <td><strong>H</strong></td>
      <td>Obtém informação sobre o hardware da máquina.</td>
      <td><strong><i>Nenhum</i></strong></td>
      <td><strong><i>Tamanho</i></strong> → 4 bytes com o tamanho do JSON que imediatamente segue.<br/><br/>A sua escolha, com pelo menos cinco elementos.</td>
    </tr>
  </table>
  
<hr/>

<p><strong>Considerações Finais:</strong></p>

<ul>
  <li>A resposta a essa será conferida em sala de aula, por meio de execução de cliente e servidor, tanto do mesmo grupo, quanto de grupos distintos (servidor de um e clientes de outros);<br/><br/></li>
  <li>Deve ser criado um arquivo (<strong>funcoes_bot.py</strong>) onde deverão ser criadas funções para cada comando do bot.<br/></li>
</ul>

<hr/>



