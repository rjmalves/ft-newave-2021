# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 01
#
# Processar estudos com base no PMO/PLD e PEN nas versões
# 27 (versão oficial) e 27.4.3 (em validação), sem a nova
# funcionalidade habilitada.
# Comparar os resultados a partir da análise das impressões
# no PMO.DAT, PARP.DAT e NWLISTOP.

# INSTRUÇÕES PARA USO DO SCRIPT DE TESTE
#
# 1- Substituir nas variáveis auxiliares os diretórios onde
#    foram executadas as respectivas versões do NEWAVE.
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
#    python testes/teste01.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.pmo import LeituraPMO  # type: ignore
from inewave.newave.parp import LeituraPARp  # type: ignore
from inewave.nwlistop.mediassin import LeituraMediasSIN  # type: ignore
from inewave.nwlistop.mediasmerc import LeituraMediasMerc  # type: ignore


# Variáveis auxiliares no processo
diretorio_v270000 = ""
diretorio_v270403 = ""

# Lê os arquivos de cada diretório
pmo_v270000 = LeituraPMO(diretorio_v270000).le_arquivo()
pmo_v270403 = LeituraPMO(diretorio_v270403).le_arquivo()
parp_v270000 = LeituraPARp(diretorio_v270000).le_arquivo()
parp_v270403 = LeituraPARp(diretorio_v270403).le_arquivo()
mediassin_v270000 = LeituraMediasSIN(diretorio_v270000).le_arquivo()
mediassin_v270403 = LeituraMediasSIN(diretorio_v270403).le_arquivo()
mediasmerc_v270000 = LeituraMediasMerc(diretorio_v270000).le_arquivo()
mediasmerc_v270403 = LeituraMediasMerc(diretorio_v270403).le_arquivo()

# Compara os dados lidos
pmo_iguais = pmo_v270000 == pmo_v270403
parp_iguais = parp_v270000 == parp_v270403
mediassin_iguais = mediassin_v270000 == mediassin_v270403
mediasmerc_iguais = mediasmerc_v270000 == mediasmerc_v270403

print(f"Arquivos pmo.dat iguais: {pmo_iguais}")
print(f"Arquivos parp.dat iguais: {parp_iguais}")
print(f"Arquivos MEDIAS-SIN.CSV iguais: {mediassin_iguais}")
print(f"Arquivos MEDIAS-MERC.CSV iguais: {mediasmerc_iguais}")
