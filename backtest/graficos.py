
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import List, Tuple
from caso import Caso
from caso import SUBSISTEMAS

CORES = ["black",
         "deepskyblue",
         "springgreen",
         "gold",
         "lightsalmon",
         "orangered"]

def xticks_graficos() -> Tuple[List[float], List[str]]:
    """
    """
    ticks = range(61)
    # labels = ["rv0\nJAN/20", "rv1", "rv2", "rv3", "rv4",
    #           "rv0\nFEV/20", "rv1", "rv2", "rv3",
    #           "rv0\nMAR/20", "rv1", "rv2", "rv3", 
    #           "rv0\nABR/20", "rv1", "rv2", "rv3", 
    #           "rv0\nMAI/20", "rv1", "rv2", "rv3", "rv4",
    #           "rv0\nJUN/20", "rv1", "rv2", "rv3", 
    #           "rv0\nJUL/20", "rv1", "rv2", "rv3", "rv4",
    #           "rv0\nAGO/20", "rv1", "rv2", "rv3", 
    #           "rv0\nSET/20", "rv1", "rv2", "rv3",
    #           "rv0\nOUT/20", "rv1", "rv2", "rv3", "rv4",
    #           "rv0\nNOV/20", "rv1", "rv2", "rv3",
    #           "rv0\nDEZ/20", "rv1", "rv2", "rv3",
    #           "rv0\nJAN/21", "rv1", "rv2", "rv3", "rv4",
    #           "rv0\nFEV/21", "rv1", "rv2", "rv3"]
    labels = ["rv0\nJAN/20", "", "", "", "",
              "rv0\nFEV/20", "", "", "",
              "rv0\nMAR/20", "", "", "", 
              "rv0\nABR/20", "", "", "", 
              "rv0\nMAI/20", "", "", "", "",
              "rv0\nJUN/20", "", "", "", 
              "rv0\nJUL/20", "", "", "", "",
              "rv0\nAGO/20", "", "", "", 
              "rv0\nSET/20", "", "", "",
              "rv0\nOUT/20", "", "", "", "",
              "rv0\nNOV/20", "", "", "",
              "rv0\nDEZ/20", "", "", "",
              "rv0\nJAN/21", "", "", "", "",
              "rv0\nFEV/21", "", "", ""]
    return ticks, labels


def grafico_cmo_subsistema(casos: List[Caso],
                           dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Evolução do CMO por Submercado",
                fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='CMO (R$/MWh)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
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
            y = caso.cmo_subsis[sub]
            max_x = max([len(x) - 1, max_x])
            max_y = max([max_y] + list(y))
            min_y = min([min_y] + list(y))
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
    x_ticks, x_labels = xticks_graficos()
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(min_y, max_y)
        axs[subx, suby].set_xticks(x_ticks)
        axs[subx, suby].set_xticklabels(x_labels,
                                        fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(casos))

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_cmo.png"))
    plt.close()


def grafico_earm_subsistema(casos: List[Caso],
                            dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Evolução do Armazenamento por Submercado",
                fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='EARM (% EARMax)')
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
    x_ticks, x_labels = xticks_graficos()
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
        axs[subx, suby].set_xticks(x_ticks)
        axs[subx, suby].set_xticklabels(x_labels,
                                        fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(casos))

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_earm_subsis.png"))
    plt.close()


def grafico_gt_subsistema(casos: List[Caso],
                          dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Evolução da Geração Térmica por Submercado",
                fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='GT (MWmed)')
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
            y = caso.gt_subsis[sub]
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
    x_ticks, x_labels = xticks_graficos()
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
        axs[subx, suby].set_xticks(x_ticks)
        axs[subx, suby].set_xticklabels(x_labels,
                                        fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(casos))

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_gt_subsis.png"))
    plt.close()


def grafico_earm_sin(casos: List[Caso],
                     dir_saida: str):
    # Cria o objeto de figura
    fig = plt.figure(figsize=(10, 5))
    plt.title("Evolução do Armazenamento para o SIN",
              fontsize=14)
    plt.ylabel('EARM (% EARMax)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
    max_x = 0

    handlers_legendas = []
    for c, caso in enumerate(casos):
    # Recalcula os máximos e mínimos
        x = list(range(caso.n_revs))
        y = caso.earm_sin
        max_x = max([len(x) - 1, max_x])
        max_y = max([max_y] + list(y))
        min_y = min([min_y] + list(y))
        # Faz o plot
        h = plt.plot(x, y,
                     linewidth=3,
                     linestyle="solid",
                     color = CORES[c],
                     alpha=0.8,
                     label=caso.nome)
        handlers_legendas.append(h)
    # Adiciona a legenda e limita os eixos
    x_ticks, x_labels = xticks_graficos()
    plt.xlim(0, max_x)
    plt.ylim(min_y, max_y)
    plt.xticks(x_ticks, x_labels, fontsize=9)
    plt.tight_layout()
    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.15)
    plt.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               bbox_to_anchor=(0.462, -0.18),
               loc="lower center",
               borderaxespad=0,
               ncol=len(casos),
               fontsize=9)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_earm_sin.png"))
    plt.close()


def grafico_gt_sin(casos: List[Caso],
                            dir_saida: str):
    # Cria o objeto de figura
    fig = plt.figure(figsize=(10, 5))
    plt.title("Evolução da Geração Térmica para o SIN",
              fontsize=14)
    plt.ylabel('GT (MWmed)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
    max_x = 0

    handlers_legendas = []
    for c, caso in enumerate(casos):
    # Recalcula os máximos e mínimos
        x = list(range(caso.n_revs))
        y = caso.gt_sin
        max_x = max([len(x) - 1, max_x])
        max_y = max([max_y] + list(y))
        min_y = min([min_y] + list(y))
        # Faz o plot
        h = plt.plot(x, y,
                     linewidth=3,
                     linestyle="solid",
                     color = CORES[c],
                     alpha=0.8,
                     label=caso.nome)
        handlers_legendas.append(h)
    # Adiciona a legenda e limita os eixos
    x_ticks, x_labels = xticks_graficos()
    plt.xlim(0, max_x)
    plt.ylim(min_y, max_y)
    plt.xticks(x_ticks, x_labels, fontsize=9)
    plt.tight_layout()
    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.15)
    plt.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               bbox_to_anchor=(0.462, -0.18),
               loc="lower center",
               borderaxespad=0,
               ncol=len(casos),
               fontsize=9)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_gt_sin.png"))
    plt.close()
