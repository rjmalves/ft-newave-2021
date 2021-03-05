
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import List
from caso import Caso
from caso import SUBSISTEMAS

CORES = ["lightsalmon",
         "gold",
         "springgreen",
         "deepskyblue",
         "violet",
         "mediumvioletred"]

def grafico_cmo_subsistema(casos: List[Caso],
                           dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Evolução do CMO por Submercado",
                fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='Mês', ylabel='CMO (R$/MWh)')
    for ax in axs.flat:
        ax.label_outer()
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
    max_x = 0
    # Desenha as linhas
    for s, sub in enumerate(SUBSISTEMAS):
        # Decide qual subplot usar
        subx = int(s / 2)
        suby = s % 2
        # Faz o plot para cada caso
        for c, caso in enumerate(casos):
        # Recalcula os máximos e mínimos
            x = list(range(caso.n_revs))
            y = caso.cmo_subsis[sub]
            max_x = max([len(x) - 1, max_x])
            max_y = max([max_y] + list(y))
            min_y = min([min_y] + list(y))
            # Faz o plot
            axs[subx, suby].plot(x, y,
                                linewidth=3,
                                linestyle="solid",
                                color = CORES[c],
                                alpha=0.8,
                                label=caso.nome)
        axs[subx, suby].set_title(sub)
    # Adiciona a legenda e limita os eixos
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(min_y, max_y)
        axs[subx, suby].legend(loc=1, prop={'size': 8})
    # Salva o arquivo de saída
    plt.tight_layout()
    plt.savefig(os.path.join(dir_saida,
                             "teste_backtest_cmo.png"))
    plt.close()


def grafico_earm_subsistema(casos: List[Caso],
                            dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Evolução da EARM por Submercado",
                fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='Mês', ylabel='EARM (% EARMax)')
    # Variáveis para limitar os eixos no futuro
    max_y = {s: 0.0 for s in SUBSISTEMAS}
    min_y = {s: 1e4 for s in SUBSISTEMAS}
    max_x = 0

    handlers_legendas = []
    # Desenha as linhas
    for s, sub in enumerate(SUBSISTEMAS):
        # Decide qual subplot usar
        subx = int(s / 2)
        suby = s % 2
        # Faz o plot para cada caso
        for c, caso in enumerate(casos):
        # Recalcula os máximos e mínimos
            x = list(range(caso.n_revs))
            y = caso.earm_subsis[sub]
            max_x = max([len(x) - 1, max_x])
            max_y[sub] = max([max_y[sub]] + list(y))
            min_y[sub] = min([min_y[sub]] + list(y))
            # Faz o plot
            h = axs[subx, suby].plot(x, y,
                                     linewidth=3,
                                     linestyle="solid",
                                     color = CORES[c],
                                     alpha=0.8,
                                     label=caso.nome)
            handlers_legendas.append(h)
        axs[subx, suby].set_title(sub)
    # Adiciona a legenda e limita os eixos
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
        # axs[subx, suby].legend(bbox_to_anchor=(-1.05, -1.0),
        #                        loc='lower center',
        #                        mode="expand",
        #                        prop={'size': 8},
        #                        ncol=len(casos))
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(casos))

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(os.path.join(dir_saida,
                             "teste_backtest_earm.png"))
    plt.close()