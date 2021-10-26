# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 03
#
# Processar PMOs/PLDs na versão 27.4.3 variando o número
# de processadores e em máquinas diferentes.
# Os resultados devem ser idênticos.

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
#    python testes/teste03.py
#
# 6- Observar a saída exibida no terminal e a figura
#    gerada na pasta saidas/.

from inewave.newave.pmo import PMO  # type: ignore
from inewave.newave.parp import PARp  # type: ignore
from inewave.nwlistop.mediassin import MediasSIN  # type: ignore
from inewave.nwlistop.mediasmerc import MediasMerc  # type: ignore
import os
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from itertools import combinations

# Variáveis auxiliares no processo
# Consideradas três execuções do NEWAVE, por exemplo:
# A - Máquina 1, Nº Processadores N
# B - Máquina 1, Nº Processadores M
# C - Máquina 2, Nº Processadores N ou M
diretorio_execA = ""
diretorio_execB = ""
diretorio_execC = ""

# Lê os arquivos de cada diretório
pmo_execA = PMO.le_arquivo(diretorio_execA)
pmo_execB = PMO.le_arquivo(diretorio_execB)
pmo_execC = PMO.le_arquivo(diretorio_execC)
parp_execA = PARp.le_arquivo(diretorio_execA)
parp_execB = PARp.le_arquivo(diretorio_execB)
parp_execC = PARp.le_arquivo(diretorio_execC)
mediassin_execA = MediasSIN.le_arquivo(diretorio_execA)
mediassin_execB = MediasSIN.le_arquivo(diretorio_execB)
mediassin_execC = MediasSIN.le_arquivo(diretorio_execC)
mediasmerc_execA = MediasMerc.le_arquivo(diretorio_execA)
mediasmerc_execB = MediasMerc.le_arquivo(diretorio_execB)
mediasmerc_execC = MediasMerc.le_arquivo(diretorio_execC)

# Compara os dados lidos
pmo_iguais = all([d1 == d2 for d1, d2 in
                  combinations([pmo_execA.custo_operacao_series_simuladas,
                                pmo_execB.custo_operacao_series_simuladas,
                                pmo_execC.custo_operacao_series_simuladas], 2)])
parp_iguais = all([d1 == d2 for d1, d2 in
                   combinations([parp_execA.coeficientes_ree(1),
                                 parp_execB.coeficientes_ree(1),
                                 parp_execC.coeficientes_ree(1)], 2)])
mediassin_iguais = all([d1 == d2 for d1, d2 in
                       combinations([mediassin_execA.medias,
                                     mediassin_execB.medias,
                                     mediassin_execC.medias], 2)])
mediasmerc_iguais = all([d1 == d2 for d1, d2 in
                         combinations([mediasmerc_execA.medias,
                                       mediasmerc_execB.medias,
                                       mediasmerc_execC.medias], 2)])

print(f"Arquivos pmo.dat iguais: {pmo_iguais}")
print(f"Arquivos parp.dat iguais: {parp_iguais}")
print(f"Arquivos MEDIAS-SIN.CSV iguais: {mediassin_iguais}")
print(f"Arquivos MEDIAS-MERC.CSV iguais: {mediasmerc_iguais}")
