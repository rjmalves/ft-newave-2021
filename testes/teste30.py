# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 30
#
# Processar estudos com base no PMO/ PLD/ PEN/ PDE/
# Garantia Física nas versões 27 (versão oficial) e 27.4.3
# (em validação), com decks oficiais, porém considerando o
# hidrograma abaixo para o trecho de vazão reduzida (TVR).
#
# Avaliar o modelo MARS ajustado.

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
#    python testes/teste30.py
#
# 6- Observar os gráficos na pasta saidas/

from inewave.newave.pmo import LeituraPMO  # type: ignore
from inewave.newave.modelos.pmo import PMO  # type: ignore
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from typing import List
import os

CORES = ["orangered",
         "royalblue",
         "limegreen",
         "gold",
         "blueviolet"]

ESTILOS_LINHA = ['solid',
                 'dashed',
                 'dotted',
                 'solid']

nomes = ["NW 27 - Hidr. Oficial",
         "NW 27.4.3 - Hidr. Oficial",
         "NW 27 - Hidr. IBAMA",
         "NW 27.4.3 - Hidr. IBAMA"]

dir_base = ("/home/rogerio/ONS/validacao_newave2743")
caminhos = [os.path.join(dir_base, "pmo_2020_05_oficial_nw27"),
            os.path.join(dir_base, "pmo_2020_05_oficial"),
            os.path.join(dir_base, "pmo_2020_05_ibama_nw27"),
            os.path.join(dir_base, "pmo_2020_05_ibama")]
pmos: List[PMO] = []
for c in caminhos:
    leitor = LeituraPMO(c)
    print(f"lendo {c}")
    pmos.append(leitor.le_arquivo())

x = np.arange(0, 100, 10)
plt.figure(figsize=(10, 5))
for n, pmo in enumerate(pmos):
    y = [pmo.retas_perdas_engolimento.funcao_perdas(8, i) for i in x]
    plt.plot(x, y,
             label=nomes[n],
             c=CORES[n],
             linewidth=3.0,
             linestyle=ESTILOS_LINHA[n],
             alpha=0.8)
plt.title("Perdas por Engolimento Máximo (MARS) - REE B. Monte")
plt.xlabel("EFIOB (MWmes)")
plt.ylabel("Perdas (MWmes)")
plt.legend()
plt.tight_layout()
plt.savefig("saidas/teste30_zoom.png")
plt.close()

x = np.arange(0, 15000, 100)
plt.figure(figsize=(10, 5))
for n, pmo in enumerate(pmos):
    y = [pmo.retas_perdas_engolimento.funcao_perdas(8, i) for i in x]
    plt.plot(x, y,
             label=nomes[n],
             c=CORES[n],
             linewidth=3.0,
             linestyle=ESTILOS_LINHA[n],
             alpha=0.8)
plt.title("Perdas por Engolimento Máximo (MARS) - REE B. Monte")
plt.xlabel("EFIOB (MWmes)")
plt.ylabel("Perdas (MWmes)")
plt.legend()
plt.tight_layout()
plt.savefig("saidas/teste30.png")
plt.close()
