# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
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
#    LINUX: source venv/bin/activate
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
diretorio_oficial = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_oficial"
diretorio_parpa = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_parpa"
# Lê os arquivos
dger_oficial = LeituraDGer(diretorio_oficial).le_arquivo()
pmo_oficial = LeituraPMO(diretorio_oficial).le_arquivo()
dger_parpa = LeituraDGer(diretorio_parpa).le_arquivo()
pmo_parpa = LeituraPMO(diretorio_parpa).le_arquivo()

# Compara os dados lidos
eco_igual_oficial = dger_oficial.eq_eco_saida(pmo_oficial.dados_gerais)
flags_dger_oficial = dger_oficial.afluencia_anual_parp
flags_pmo_oficial = pmo_oficial.dados_gerais.afluencia_anual_parp
eco_igual_parpa = dger_parpa.eq_eco_saida(pmo_parpa.dados_gerais)
flags_dger_parpa = dger_parpa.afluencia_anual_parp
flags_pmo_parpa = pmo_parpa.dados_gerais.afluencia_anual_parp

print("PMO Oficial")
print(f"Eco de saída igual: {eco_igual_oficial}")
print(f"Flags no dger: AFL. ANUAL = {flags_dger_oficial[0]} RED ORDEM = {flags_dger_oficial[1]}")
print(f"Flags no  pmo: AFL. ANUAL = {flags_pmo_oficial[0]} RED ORDEM = {flags_pmo_oficial[1]}")

print("PMO PAR(p)-A")
print(f"Eco de saída igual: {eco_igual_parpa}")
print(f"Flags no dger: AFL. ANUAL = {flags_dger_parpa[0]} RED ORDEM = {flags_dger_parpa[1]}")
print(f"Flags no  pmo: AFL. ANUAL = {flags_pmo_parpa[0]} RED ORDEM = {flags_pmo_parpa[1]}")
