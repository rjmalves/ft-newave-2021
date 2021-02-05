# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.02
# FEVEREIRO / 2021

# TESTE 04
#
# Avaliar críticas e eco de saída dos novos flags
# adicionados no arquivo de dados gerais:
# •	AFLUENCIA ANUAL PARP
# •	REDUCAO DA ORDEM

# INSTRUÇÕES PARA USO DO SCRIPT DE TESTE
#
# 1- Substituir nas variáveis auxiliares os diretórios onde
#    estão as saídas das execuções do NEWAVE.
#
# 2- Criar um ambiente virtual com o comando:
#    python -m venv ./venv
#
# 3- Ativar o ambiente virtual com um dos comandos:
#    LINUX: ./venv/bin/activate
#    WINDOWS: ./venv/Scripts/activate
#
# 4- Instalar os módulos necessários com o comando:
#    python -m pip install -r requirements.txt
#
# 5- Executar no terminal o script desejado. Por ex:
#    python testes/teste04.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.dger import LeituraDGer
from inewave.newave.pmo import LeituraPMO


# Variáveis auxiliares no processo
diretorio_exec = ""

# Lê os arquivos
dger = LeituraDGer(diretorio_exec).le_arquivo()
pmo = LeituraPMO(diretorio_exec).le_arquivo()


# Compara os dados lidos
eco_igual = dger.eq_eco_saida(pmo.dados_gerais)

print(f"Eco de saída igual: {eco_igual}")
print(f"Flags no dger = {dger.afluencia_anual_parp}")
print(f"Flags no  pmo = {pmo.dados_gerais.afluencia_anual_parp}")
