# 🤖 Telegram Bot - Gerenciador de Monitoramento Remoto

Este repositório contém o core de um bot do Telegram desenvolvido em Python para atuar como uma interface de linha de comando móvel para monitoramento e gerência de infraestrutura e agentes remotos. O bot permite extrair métricas de hardware, processos e sistemas diretamente pelo chat do Telegram, contando com um sistema de permissões para administradores.

## 🚀 Funcionalidades Atuais

* **Extração e Validação de Comandos:** Captura mensagens textuais enviadas ao bot, valida parâmetros (como endereços IP) e converte comandos amigáveis do Telegram em instruções internas simplificadas.
* **Controle de Acesso Restrito:** Sistema de whitelist baseado no ID de chat do Telegram. Se um usuário não autorizado tentar interagir, o bot bloqueia o comando e envia um alerta em tempo real para os administradores solicitando permissão.
* **Segmentação Automática de Mensagens:** Tratamento nativo para o limite de 4.096 caracteres por mensagem imposto pela API do Telegram, dividindo o retorno de dados longos (como tabelas de processos) em múltiplas mensagens sem quebrar o fluxo.
* **Integração com Módulos de Gerência:** Pronto para se conectar com agentes distribuídos (via módulo `gerente`) para coleta de dados de CPU, Memória, Processos específicos (PID) e Hardware.

---

## ⚙️ Comandos Suportados no Chat

O bot converte os comandos digitados no Telegram para códigos internos que o módulo `gerente` consegue processar. A tabela abaixo detalha o que cada comando faz e quais parâmetros você deve enviar no chat (ex: `/procs 192.168.1.10`).

| Comando Telegram | Cód. | O que ele faz? | Parâmetros esperados no chat |
| --- | --- | --- | --- |
| `/agentes` | `A` | Lista todos os agentes/máquinas que estão ativos e conectados na rede. | Nenhum argumento. Envie apenas `/agentes`. |
| `/procs` | `G` | Traz a lista completa de todos os processos que estão rodando na máquina destino. | Requer o IP do agente. Ex: `/procs [IP]` |
| `/proc` | `P` | Busca informações detalhadas de um processo específico que está rodando no agente. | Requer o IP e o PID do processo. Ex: `/proc [IP] [PID]` |
| `/topcpu` | `C` | Mostra quais são os processos que mais estão consumindo CPU no momento no agente. | Requer o IP do agente. Ex: `/topcpu [IP]` |
| `/topmem` | `M` | Mostra quais são os processos que mais estão consumindo Memória no momento no agente. | Requer o IP do agente. Ex: `/topmem [IP]` |
| `/histcpu` | `I` | Retorna o histórico de uso e consumo da CPU daquela máquina. | Requer o IP do agente. Ex: `/histcpu [IP]` |
| `/hardw` | `H` | Exibe um resumo dos detalhes de hardware da máquina (especificações do sistema). | Requer o IP do agente. Ex: `/hardw [IP]` |
| `/eval` | `E` | Executa rotinas de avaliação ou testes específicos diretamente no agente. | Requer o IP do agente. Ex: `/eval [IP]` |

---

## 🛠️ Estrutura de Arquivos Necessária

Para o funcionamento completo deste script, o repositório deve contar (ou receber futuramente) os seguintes módulos auxiliares:

* `mytokens.py`: Contendo a constante `TELEGRAM_TOKEN` com o token do seu bot gerado pelo BotFather.
* `gerente.py`: Contendo a função `chama_gerente(comando_bot)` que faz a ponte de comunicação e requisições com as máquinas/agentes monitorados.
* `mensagens.py`: Responsável por guardar os templates de texto, como o `mensagem_menu()` e a estilização/limpeza dos dados em `formata_mensagem()`.

---

## 📝 Próximos Passos (To-Do List)

> [!NOTE]
> Melhorias mapeadas no código para as próximas atualizações:
> * Implementar o retorno padronizado das funções do módulo `gerente`.
> * Padronizar todas as respostas enviadas pelos agentes remotos para o formato **JSON**.
> 
> 

---

## 💻 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git

```


2. Instale a biblioteca de dependência:
```bash
pip install requests

```


3. Certifique-se de configurar seus administradores diretamente na função `autoriza()` dentro do código e o token no arquivo `mytokens.py`.
4. Execute o script principal:
```bash
python main.py

```
