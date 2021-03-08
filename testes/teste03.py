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

from inewave.newave.pmo import LeituraPMO  # type: ignore
from inewave.newave.parp import LeituraPARp  # type: ignore
from inewave.nwlistop.mediassin import LeituraMediasSIN  # type: ignore
from inewave.nwlistop.mediasmerc import LeituraMediasMerc  # type: ignore
import os
import numpy as np
import matplotlib.pyplot as plt  # type: ignore


# Variáveis auxiliares no processo
# Consideradas três execuções do NEWAVE, por exemplo:
# A - Máquina 1, Nº Processadores N
# B - Máquina 1, Nº Processadores M
# C - Máquina 2, Nº Processadores N ou M
diretorio_execA = ""
diretorio_execB = ""
diretorio_execC = ""

# Lê os arquivos de cada diretório
pmo_execA = LeituraPMO(diretorio_execA).le_arquivo()
pmo_execB = LeituraPMO(diretorio_execB).le_arquivo()
pmo_execC = LeituraPMO(diretorio_execC).le_arquivo()
parp_execA = LeituraPARp(diretorio_execA).le_arquivo()
parp_execB = LeituraPARp(diretorio_execB).le_arquivo()
parp_execC = LeituraPARp(diretorio_execC).le_arquivo()
mediassin_execA = LeituraMediasSIN(diretorio_execA).le_arquivo()
mediassin_execB = LeituraMediasSIN(diretorio_execB).le_arquivo()
mediassin_execC = LeituraMediasSIN(diretorio_execC).le_arquivo()
mediasmerc_execA = LeituraMediasMerc(diretorio_execA).le_arquivo()
mediasmerc_execB = LeituraMediasMerc(diretorio_execB).le_arquivo()
mediasmerc_execC = LeituraMediasMerc(diretorio_execC).le_arquivo()

# Compara os dados lidos
pmo_iguais = pmo_execA == pmo_execB == pmo_execC
parp_iguais = parp_execA == parp_execB == parp_execC
mediassin_iguais = mediassin_execA == mediassin_execB == mediassin_execC
mediasmerc_iguais = mediasmerc_execA == mediasmerc_execB == mediasmerc_execC

print(f"Arquivos pmo.dat iguais: {pmo_iguais}")
print(f"Arquivos parp.dat iguais: {parp_iguais}")
print(f"Arquivos MEDIAS-SIN.CSV iguais: {mediassin_iguais}")
print(f"Arquivos MEDIAS-MERC.CSV iguais: {mediasmerc_iguais}")


# Analisa os tempos de execução
tempos_A = pmo_execA.convergencia.tempos_execucao
tempos_B = pmo_execB.convergencia.tempos_execucao
tempos_C = pmo_execC.convergencia.tempos_execucao
max_tempo = max(tempos_A + tempos_B + tempos_C)

iters_A = list(range(1, len(tempos_A) + 1))
iters_B = list(range(1, len(tempos_B) + 1))
iters_C = list(range(1, len(tempos_C) + 1))
max_iter = max(iters_A + iters_B + iters_C)

# Gera o gráfico
largura = 0.5
plt.figure(figsize=(10, 5))
plt.bar(np.array(iters_A)[::3],
        tempos_A[::3], largura, label="Execução A")
plt.bar(np.array(iters_B)[::3] + 0.5,
        tempos_B[::3], largura, label="Execução B")
plt.bar(np.array(iters_C)[::3] + 1.0,
        tempos_C[::3], largura, label="Execução C")
plt.legend()
plt.title("Tempos de Execução das Iterações (Teste 03 - FT NEWAVE 2021)")
plt.xlabel("Iteração")
plt.ylabel("Tempo (s)")
plt.xlim(0, max_iter)
plt.ylim(0, max_tempo)
plt.tight_layout()

# Exporta a figura, criando a pasta se necessário
if not os.path.exists("saidas/"):
    os.makedirs("saidas/")
plt.savefig("saidas/teste03_tempos.png")
plt.close()
