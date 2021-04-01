
import matplotlib.pyplot as plt  # type: ignore
import csv
import os
from typing import List, Tuple
from caso import Caso  # type: ignore
from caso import SUBSISTEMAS  # type: ignore

CORES = [
         "black",
         "deepskyblue",
         "springgreen",
         "gold",
         "lightsalmon",
         "deepskyblue",
         "springgreen",
         "gold",
         "lightsalmon"
         ]

TIPOS = [
         "solid",
         "solid",
         "solid",
         "solid",
         "solid",
         "dashed",
         "dashed",
         "dashed",
         "dashed"
        ]

LARGURAS = [
            3,
            3,
            3,
            3,
            3,
            2,
            2,
            2,
            2
           ]

def xticks_graficos() -> Tuple[List[int], List[str]]:
    """
    """
    ticks = list(range(61))
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
            y = caso.cmo_subsis[sub][1:]
            max_x = max([len(x) - 1, max_x])
            max_y = max([max_y] + list(y))
            min_y = min([min_y] + list(y))
            # Faz o plot
            h, = axs[subx, suby].plot(x, y,
                                      linewidth=LARGURAS[c],
                                      linestyle=TIPOS[c],
                                      color=CORES[c],
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
        axs[subx, suby].set_yticks(range(0, int(max_y), 125),
                                   minor=True)
        axs[subx, suby].grid(which='major', axis='y', alpha=0.5)
        axs[subx, suby].grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               [c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=5)

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.115)
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
    vminp = {"SE": 20, "S": 30, "NE": 23.5, "N": 20.8}
    handlers_legendas = []
    # Desenha as linhas
    for s, sub in enumerate(SUBSISTEMAS):
        # Decide qual subplot usar
        subx = int(s / 2)
        suby = s % 2
        # Faz o plot para cada caso
        for c, caso in enumerate(casos):
            # Recalcula os máximos e mínimos
            x = list(range(caso.n_revs + 1))
            y = caso.earm_subsis[sub]
            max_x = max([len(x) - 1, max_x])
            max_y[sub] = max([max_y[sub]] + list(y))
            min_y[sub] = min([min_y[sub]] + list(y))
            # Faz o plot
            h = axs[subx, suby].plot(x, y,
                                     linewidth=LARGURAS[c],
                                     linestyle=TIPOS[c],
                                     color=CORES[c],
                                     alpha=0.8,
                                     label=caso.nome)
            handlers_legendas.append(h)
        # Faz o plot do vminp para o subsistema
        x = range(max_x + 2)
        y = [vminp[sub]] * len(x)
        h = axs[subx, suby].plot(x, y,
                             linewidth=2,
                             linestyle="dashed",
                             color="red",
                             alpha=0.65,
                             label="VminOP")
        axs[subx, suby].set_title(sub)
    # Adiciona a legenda e limita os eixos
    x_ticks, x_labels = xticks_graficos()
    for s, sub in enumerate(SUBSISTEMAS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, max_x)
        axs[subx, suby].set_ylim(0, 100)
        axs[subx, suby].set_xticks(x_ticks + [max_x])
        axs[subx, suby].set_xticklabels([""] + x_labels,
                                        fontsize=9)
        axs[subx, suby].set_yticks(range(0, 100, 5),
                                   minor=True)
        axs[subx, suby].grid(which='major', axis='y', alpha=0.5)
        axs[subx, suby].grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=5)

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.115)
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
    max_y = 0.0
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
            y = caso.gt_subsis[sub][1:]
            max_x = max([len(x) - 1, max_x])
            max_y = max([max_y] + list(y))
            min_y[sub] = min([min_y[sub]] + list(y))
            # Faz o plot
            h = axs[subx, suby].plot(x, y,
                                     linewidth=LARGURAS[c],
                                     linestyle=TIPOS[c],
                                     color=CORES[c],
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
        axs[subx, suby].set_ylim(0, max_y)
        axs[subx, suby].set_xticks(x_ticks)
        axs[subx, suby].set_xticklabels(x_labels,
                                        fontsize=9)
        axs[subx, suby].set_yticks(range(0, int(max_y), 500),
                                   minor=True)
        axs[subx, suby].grid(which='major', axis='y', alpha=0.5)
        axs[subx, suby].grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=[c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=5)

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.115)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_gt_subsis.png"))
    plt.close()


def grafico_earm_sin(casos: List[Caso],
                     dir_saida: str):
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("Evolução do Armazenamento para o SIN",
                 fontsize=14)
    ax.set_ylabel('EARM (% EARMax)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
    max_x = 0

    handlers_legendas = []
    for c, caso in enumerate(casos):
        # Recalcula os máximos e mínimos
        x = list(range(caso.n_revs + 1))
        y = caso.earm_sin
        max_x = max([len(x) - 1, max_x])
        max_y = max([max_y] + list(y))
        min_y = min([min_y] + list(y))
        # Faz o plot
        h, = ax.plot(x, y,
                     linewidth=LARGURAS[c],
                     linestyle=TIPOS[c],
                     color=CORES[c],
                     alpha=0.8,
                     label=caso.nome)
        handlers_legendas.append(h)
    # Adiciona a legenda e limita os eixos
    x_ticks, x_labels = xticks_graficos()
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, 100)
    ax.set_xticks(x_ticks + [max_x])
    ax.set_xticklabels([""] + x_labels,
                       fontsize=9)
    ax.set_yticks(list(range(0, 100, 5)), minor=True)
    ax.grid(which='major', axis='y', alpha=0.5)
    ax.grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.20)
    plt.legend(handlers_legendas,
               [c.nome for c in casos],
               bbox_to_anchor=(0.462, -0.25),
               loc="lower center",
               borderaxespad=0,
               ncol=5,
               fontsize=8)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_earm_sin.png"))
    plt.close()


def grafico_gt_sin(casos: List[Caso],
                   dir_saida: str):
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("Evolução da Geração Térmica para o SIN",
              fontsize=14)
    ax.set_ylabel('GT (MWmed)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
    min_y = 1e4
    max_x = 0

    handlers_legendas = []
    for c, caso in enumerate(casos):
        # Recalcula os máximos e mínimos
        x = list(range(caso.n_revs))
        y = caso.gt_sin[1:]
        max_x = max([len(x) - 1, max_x])
        max_y = max([max_y] + list(y))
        min_y = min([min_y] + list(y))
        # Faz o plot
        h, = ax.plot(x, y,
                     linewidth=LARGURAS[c],
                     linestyle=TIPOS[c],
                     color=CORES[c],
                     alpha=0.8,
                     label=caso.nome)
        handlers_legendas.append(h)
    # Faz o plot da meta GT para o subsistema
    x = range(max_x + 1)
    y = [15000] * len(x)
    h, = ax.plot(x, y,
                 linewidth=2,
                 linestyle="dashed",
                 color="red",
                 alpha=0.65,
                 label="Meta CMSE")
    # Adiciona a legenda e limita os eixos
    x_ticks, x_labels = xticks_graficos()
    ax.set_xlim(0, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, fontsize=9)
    ax.set_yticks(list(range(0, int(max_y), 500)), minor=True)
    ax.grid(which='major', axis='y', alpha=0.5)
    ax.grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.20)
    plt.legend(handlers_legendas,
               [c.nome for c in casos],
               bbox_to_anchor=(0.462, -0.25),
               loc="lower center",
               borderaxespad=0,
               ncol=5,
               fontsize=8)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_gt_sin.png"))
    plt.close()


def grafico_deficit_subsistema(casos: List[Caso],
                               dir_saida: str):
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle("Déficit por Submercado",
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='Deficit (MWmed)')
    # Variáveis para limitar os eixos no futuro
    max_y = 0.0
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
            x = list(range(caso.n_revs + 1))
            y = caso.def_subsis[sub]
            max_x = max([len(x) - 1, max_x])
            max_y[sub] = max([max_y] + list(y))
            min_y[sub] = min([min_y[sub]] + list(y))
            # Faz o plot
            h = axs[subx, suby].plot(x, y,
                                     linewidth=LARGURAS[c],
                                     linestyle=TIPOS[c],
                                     color=CORES[c],
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
        axs[subx, suby].set_ylim(0, max_y)
        axs[subx, suby].set_xticks(x_ticks + [max_x])
        axs[subx, suby].set_xticklabels([""] + x_labels,
                                        fontsize=9)
        axs[subx, suby].set_yticks(range(0, int(max_y), 500),
                                   minor=True)
        axs[subx, suby].grid(which='major', axis='y', alpha=0.5)
        axs[subx, suby].grid(which='minor', axis='y', alpha=0.2)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               [c.nome for c in casos],
               loc="lower center",
               borderaxespad=0.2,
               ncol=5)

    # Salva o arquivo de saída
    plt.subplots_adjust(bottom=0.115)
    plt.savefig(os.path.join(dir_saida,
                             "backtest_def_subsis.png"))
    plt.close()


def exporta_dados(caso: Caso,
                  caminho: str):
    """
    Exporta um conjunto de dados para um formato CSV.
    """
    cabecalhos = ["NOME_ARQ", "EARM_SE", "EARM_S",
                  "EARM_NE", "EARM_N", "EARM_SIN",
                  "GT_SE", "GT_S", "GT_NE", "GT_N",
                  "GT_SIN", "GH_SE", "GH_S", "GH_NE",
                  "GH_N", "GH_SIN", "CMO_SE", "CMO_S",
                  "CMO_NE", "CMO_N", "DEF_SE", "DEF_S",
                  "DEF_NE", "DEF_N"]
    n_dados = caso.n_revs + 1
    arq = os.path.join(caminho, f"{caso.nome}.csv")
    with open(arq, "w", newline="") as arqcsv:
        escritor = csv.writer(arqcsv,
                              delimiter=",",
                              quotechar="|",
                              quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(cabecalhos)
        for i in range(n_dados):
            if i == 0:
                nome = "INI"
            else:
                nome = caso.arquivos[i]
            earm_se = caso.earm_subsis["SE"][i]
            earm_s = caso.earm_subsis["S"][i]
            earm_ne = caso.earm_subsis["NE"][i]
            earm_n = caso.earm_subsis["N"][i]
            earm_sin = caso.earm_sin[i]
            gt_se = caso.gt_subsis["SE"][i]
            gt_s = caso.gt_subsis["S"][i]
            gt_ne = caso.gt_subsis["NE"][i]
            gt_n = caso.gt_subsis["N"][i]
            gt_sin = caso.gt_sin[i]
            ghid_se = caso.ghid_subsis["SE"][i]
            ghid_s = caso.ghid_subsis["S"][i]
            ghid_ne = caso.ghid_subsis["NE"][i]
            ghid_n = caso.ghid_subsis["N"][i]
            ghid_sin = caso.ghid_sin[i]
            cmo_se = caso.cmo_subsis["SE"][i]
            cmo_s = caso.cmo_subsis["S"][i]
            cmo_ne = caso.cmo_subsis["NE"][i]
            cmo_n = caso.cmo_subsis["N"][i]
            def_se = caso.def_subsis["SE"][i]
            def_s = caso.def_subsis["S"][i]
            def_ne = caso.def_subsis["NE"][i]
            def_n = caso.def_subsis["N"][i]
            escritor.writerow([nome,
                               earm_se,
                               earm_s,
                               earm_ne,
                               earm_n,
                               earm_sin,
                               gt_se,
                               gt_s,
                               gt_ne,
                               gt_n,
                               gt_sin,
                               ghid_se,
                               ghid_s,
                               ghid_ne,
                               ghid_n,
                               ghid_sin,
                               cmo_se,
                               cmo_s,
                               cmo_ne,
                               cmo_n,
                               def_se,
                               def_s,
                               def_ne,
                               def_n])
