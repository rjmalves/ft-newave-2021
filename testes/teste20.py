# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 20
#
# Processar um caso condicionado com X% da MLT como tendência
# hidrológica, utilizando as metodologias PAR(p) e PAR(p)-A.
# • X=50%
# • X=100%
# • X=150%

# (a) Comparar os resultados dos cenários gerados e da média móvel
# de 12 meses.
# (b) Comparar os resultados a partir da análise das impressões
# no PMO.DAT, PARP.DAT e NWLISTOP.


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
#    python testes/teste20.py
#
# 6- Observar a saída exibida no terminal.
from inewave.config import SUBMERCADOS
from inewave.nwlistop.mediasmerc import LeituraMediasMerc
from inewave.nwlistop.eafbm00 import LeituraEafbm00
from inewave.nwlistop.modelos.eafbm00 import Eafbm00
from inewave.nwlistop.modelos.mediasmerc import MediasMerc
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from typing import List, Dict


# Variáveis auxiliares com os diretorios dos casos
dir_base = "/home/rogerio/ONS/validacao_newave2745/"
dir_sul100_parp = dir_base + "pmo_2021_01_sul_100_mlt_parp"
dir_sul100_parpa = dir_base + "pmo_2021_01_sul_100_mlt_parpa"
dir_sul50_parp = dir_base + "pmo_2021_01_sul_50_mlt_parp"
dir_sul50_parpa = dir_base + "pmo_2021_01_sul_50_mlt_parpa"
dir_sul150_parp = dir_base + "pmo_2021_01_sul_150_mlt_parp"
dir_sul150_parpa = dir_base + "pmo_2021_01_sul_150_mlt_parpa"

# Variáveis auxiliares para os gráficos
CORES = ["orangered",
         "gold",
         "springgreen",
         "orangered",
         "gold",
         "springgreen"]

CORES_BOXES = ["springgreen",
               "black"]

ESTILOS = ["solid",
           "solid",
           "solid",
           "dotted",
           "dotted",
           "dotted"]

xlabels = ["", "", "", "ABR\n2021", "", "", "", "", "", "", "NOV\n2021", "",
           "", "", "", "ABR\n2022", "", "", "", "", "", "", "NOV\n2022", "",
           "", "", "", "ABR\n2023", "", "", "", "", "", "", "NOV\n2023", "",
           "", "", "", "ABR\n2024", "", "", "", "", "", "", "NOV\n2024", "",
           "", "", "", "ABR\n2025", "", "", "", "", "", "", "NOV\n2025", "" ]

xlabels_boxes = ["JAN\n2021", "FEV\n2021", "MAR\n2021", "ABR\n2021",
                 "MAI\n2021", "JUN\n2021", "JUL\n2021", "AGO\n2021",
                 "SET\n2021", "OUT\n2021", "NOV\n2021", "DEZ\n2021"]

mlt = {"SUL": np.array([7578.947109,
                        8353.733091,
                        7091.32785,
                        6593.198947,
                        8575.623952,
                        10436.38004,
                        10982.2097,
                        10079.67903,
                        11797.27154,
                        13441.68193,
                        9425.657175,
                        7453.415242]),
       "SUDESTE": np.array([65939.26526,
                            70761.90476,
                            68949.31877,
                            54749.85816,
                            39972.38701,
                            32633.28732,
                            25736.06484,
                            20627.69028,
                            19795.06843,
                            23766.68375,
                            31442.20876,
                            48011.39621]),
       "NORDESTE": np.array([13660.03734,
                             14373.16351,
                             14224.43226,
                             11604.44857,
                             7020.822773,
                             4640,
                             3827.408297,
                             3338.147758,
                             2984.776095,
                             3257.817914,
                             5297.435161,
                             9873.402405]),
       "NORTE": [15694.83658,
                 22780.20976,
                 26715.41545,
                 26994.00506,
                 20419.26383,
                 10713.49383,
                 5286.886206,
                 3223.591086,
                 2296.188787,
                 2409.390474,
                 4028.668135,
                 8295.214222]}

anos = [2021, 2022, 2023, 2024, 2025]
meses = list(range(12))

# # Lê os arquivos MEDIAS-MERC
medias_oficial_parp = LeituraMediasMerc(dir_sul100_parp).le_arquivo()
medias_oficial_parpa = LeituraMediasMerc(dir_sul100_parpa).le_arquivo()
medias_sul50_parp = LeituraMediasMerc(dir_sul50_parp).le_arquivo()
medias_sul50_parpa = LeituraMediasMerc(dir_sul50_parpa).le_arquivo()
medias_sul150_parp = LeituraMediasMerc(dir_sul150_parp).le_arquivo()
medias_sul150_parpa = LeituraMediasMerc(dir_sul150_parpa).le_arquivo()


# Gera os gráficos de ENA
def grafico_ena(medias: List[MediasMerc],
                nomes: List[str],
                titulo: str,
                dir_saida: str):
    n_meses = len(medias[0].energia_natural_afluente["SUL"])
    x = range(n_meses)
    min_y = {s: 1e5 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(titulo,
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='ENA (MWmed)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        for s, sub in enumerate(SUBMERCADOS):
            # Decide qual subplot usar
            subx = int(s / 2)
            suby = s % 2
            ena = media.energia_natural_afluente[sub]
            ena_mes_estudo: List[float] = []
            for mes in range(60):
                ena_mlt = ena[mes] / mlt[sub][mes % 12]
                ena_mes_estudo.append(ena_mlt)
            if sub == "SUL":
                print(f"caso: {nome} ena = {ena_mes_estudo[:12]}")
            min_y[sub] = min([min_y[sub]] + list(ena_mes_estudo))
            max_y[sub] = max([max_y[sub]] + list(ena_mes_estudo))
            h = axs[subx, suby].plot(x,
                                     ena_mes_estudo,
                                     linewidth=3,
                                     linestyle=ESTILOS[i],
                                     color=CORES[i],
                                     alpha=0.7,
                                     label=nome)
            handlers_legendas.append(h)
            axs[subx, suby].set_title(sub)
    for s, sub in enumerate(SUBMERCADOS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, n_meses-1)
        axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
        axs[subx, suby].set_xticks(x)
        axs[subx, suby].set_xticklabels(xlabels,
                                        fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(nomes))
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(dir_saida)
    plt.close()

grafico_ena([medias_sul50_parp,
             medias_oficial_parp,
             medias_sul150_parp,
             medias_sul50_parpa,
             medias_oficial_parpa,
             medias_sul150_parpa],
            ["Sul 50% MLT PAR(p)",
             "Sul 100% MLT PAR(p)",
             "Sul 150% MLT PAR(p)",
             "Sul 50% MLT PAR(p)-A",
             "Sul 100% MLT PAR(p)-A",
             "Sul 150% MLT PAR(p)-A"],
            "ENA Média por Submercado",
            "saidas/teste20_ena.png")

# # Gera os gráficos de CMO
# def grafico_cmo(medias: List[MediasMerc],
#                 nomes: List[str],
#                 titulo: str,
#                 dir_saida: str):
#     n_meses = len(medias[0].custo_marginal_operacao["SUL"])
#     x = range(n_meses)
#     min_y = {s: 1e5 for s in SUBMERCADOS}
#     max_y = {s: 0 for s in SUBMERCADOS}
#     handlers_legendas = []
#     # Cria o objeto de figura
#     fig, axs = plt.subplots(2, 2, figsize=(16, 9))
#     fig.suptitle(titulo,
#                  fontsize=14)
#     for ax in axs.flat:
#         ax.set(xlabel='', ylabel='CMO (R$/MWh)')
#     for i, (media, nome) in enumerate(zip(medias, nomes)):
#         for s, sub in enumerate(SUBMERCADOS):
#             # Decide qual subplot usar
#             subx = int(s / 2)
#             suby = s % 2
#             cmo = media.custo_marginal_operacao[sub]
#             min_y[sub] = min([min_y[sub]] + list(cmo))
#             max_y[sub] = max([max_y[sub]] + list(cmo))
#             h = axs[subx, suby].plot(x,
#                                      cmo,
#                                      linewidth=3,
#                                      linestyle=ESTILOS[i],
#                                      color=CORES[i],
#                                      alpha=0.7,
#                                      label=nome)
#             handlers_legendas.append(h)
#             axs[subx, suby].set_title(sub)
#     for s, sub in enumerate(SUBMERCADOS):
#         subx = int(s / 2)
#         suby = s % 2
#         axs[subx, suby].set_xlim(0, n_meses-1)
#         axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
#         axs[subx, suby].set_xticks(x)
#         axs[subx, suby].set_xticklabels(xlabels,
#                                         fontsize=9)
#     plt.tight_layout()
#     fig.legend(handlers_legendas,
#                labels=nomes,
#                loc="lower center",
#                borderaxespad=0.2,
#                ncol=len(nomes))
#     plt.subplots_adjust(bottom=0.085)
#     plt.savefig(dir_saida)
#     plt.close()

# grafico_cmo([medias_sul50_parp,
#              medias_oficial_parp,
#              medias_sul150_parp,
#              medias_sul50_parpa,
#              medias_oficial_parpa,
#              medias_sul150_parpa],
#             ["Sul 50% MLT PAR(p)",
#              "Sul 100% MLT PAR(p)",
#              "Sul 150% MLT PAR(p)",
#              "Sul 50% MLT PAR(p)-A",
#              "Sul 100% MLT PAR(p)-A",
#              "Sul 150% MLT PAR(p)-A"],
#             "CMO por Submercado",
#             "saidas/teste20_cmo.png")

# # Gera os gráficos de EARM
# def grafico_earm(medias: List[MediasMerc],
#                  nomes: List[str],
#                  titulo: str,
#                  dir_saida: str):
#     n_meses = len(medias[0].energias_armazenadas_percentuais["SUL"])
#     x = range(n_meses)
#     min_y = {s: 1e5 for s in SUBMERCADOS}
#     max_y = {s: 0 for s in SUBMERCADOS}
#     handlers_legendas = []
#     # Cria o objeto de figura
#     fig, axs = plt.subplots(2, 2, figsize=(16, 9))
#     fig.suptitle(titulo,
#                  fontsize=14)
#     for ax in axs.flat:
#         ax.set(xlabel='', ylabel='EARM (% EARMax)')
#     for i, (media, nome) in enumerate(zip(medias, nomes)):
#         for s, sub in enumerate(SUBMERCADOS):
#             # Decide qual subplot usar
#             subx = int(s / 2)
#             suby = s % 2
#             earm = media.energias_armazenadas_percentuais[sub]
#             min_y[sub] = min([min_y[sub]] + list(earm))
#             max_y[sub] = max([max_y[sub]] + list(earm))
#             h = axs[subx, suby].plot(x,
#                                      earm,
#                                      linewidth=3,
#                                      linestyle=ESTILOS[i],
#                                      color=CORES[i],
#                                      alpha=0.7,
#                                      label=nome)
#             handlers_legendas.append(h)
#             axs[subx, suby].set_title(sub)
#     for s, sub in enumerate(SUBMERCADOS):
#         subx = int(s / 2)
#         suby = s % 2
#         axs[subx, suby].set_xlim(0, n_meses-1)
#         axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
#         axs[subx, suby].set_xticks(x)
#         axs[subx, suby].set_xticklabels(xlabels,
#                                         fontsize=9)
#     plt.tight_layout()
#     fig.legend(handlers_legendas,
#                labels=nomes,
#                loc="lower center",
#                borderaxespad=0.2,
#                ncol=len(nomes))
#     plt.subplots_adjust(bottom=0.085)
#     plt.savefig(dir_saida)
#     plt.close()

# grafico_earm([medias_sul50_parp,
#               medias_oficial_parp,
#               medias_sul150_parp,
#               medias_sul50_parpa,
#               medias_oficial_parpa,
#               medias_sul150_parpa],
#              ["Sul 50% MLT PAR(p)",
#               "Sul 100% MLT PAR(p)",
#               "Sul 150% MLT PAR(p)",
#               "Sul 50% MLT PAR(p)-A",
#               "Sul 100% MLT PAR(p)-A",
#               "Sul 150% MLT PAR(p)-A"],
#              "EARM por Submercado",
#              "saidas/teste20_earm.png")

# Lê os arquivos eafbm00x
eafbm_oficial_parp = LeituraEafbm00(dir_sul100_parp).le_arquivos()
eafbm_oficial_parpa = LeituraEafbm00(dir_sul100_parpa).le_arquivos()
eafbm_sul50_parp = LeituraEafbm00(dir_sul50_parp).le_arquivos()
eafbm_sul50_parpa = LeituraEafbm00(dir_sul50_parpa).le_arquivos()
eafbm_sul150_parp = LeituraEafbm00(dir_sul150_parp).le_arquivos()
eafbm_sul150_parpa = LeituraEafbm00(dir_sul150_parpa).le_arquivos()

anos = list(eafbm_sul50_parp["SUL"].energias_por_ano.keys())[:1]
anos.sort()
meses = list(range(12))

# Gera os gráficos "Cabeleira"
def grafico_cenarios_ena(eafbms: List[Dict[str, Eafbm00]],
                         nomes: List[str],
                         titulo: str,
                         dir_saida: str):
    n_meses = 12 * len(anos)
    x = np.array(range(0, 3 * n_meses, 3))
    x_boxes = [x + i * 0.5 for i in range(len(eafbms))]
    min_y = {s: 1e6 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(titulo,
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='ENA (MWmed)')
    for i, (eafbs_subs, nome) in enumerate(zip(eafbms, nomes)):
        for s, sub in enumerate(SUBMERCADOS):
            # Decide qual subplot usar
            subx = int(s / 2)
            suby = s % 2
            # Agrupa as energias por mes de estudo
            eafb = eafbs_subs[sub].energias_por_ano
            eafb_mes_estudo: List[np.ndarray] = []
            for ano in anos:
                for mes in meses:
                    eafb_mes_estudo.append(eafb[ano][mes, :])
            
            # Desenha o boxplot para cada mês de estudo
            axs[subx, suby].boxplot(eafb_mes_estudo,
                                    positions=x_boxes[i],
                                    whis=(0, 100))
            
            axs[subx, suby].set_title(sub)
    for s, sub in enumerate(SUBMERCADOS):
        subx = int(s / 2)
        suby = s % 2
        # axs[subx, suby].set_xlim(0, n_meses-1)
        # axs[subx, suby].set_ylim(min_y[sub], max_y[sub])
        axs[subx, suby].set_xticks(x)
        axs[subx, suby].set_xticklabels(xlabels[:len(x)],
                                        fontsize=9)
    plt.tight_layout()
    # fig.legend(handlers_legendas,
    #            labels=nomes,
    #            loc="lower center",
    #            borderaxespad=0.2,
    #            ncol=len(nomes))
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(dir_saida)
    plt.close()


# Gera os gráficos "Cabeleira" para o SUL
def grafico_cenarios_ena_sul(eafbms: List[Dict[str, Eafbm00]],
                             nomes: List[str],
                             titulo: str,
                             dir_saida: str):
    sub = "SUL"
    n_meses = 12 * len(anos)
    x = np.array(range(0, 3 * n_meses, 3))
    x_boxes = [x + i * 0.5 for i in range(len(eafbms))]
    min_y = {s: 1e6 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(figsize=(10, 5))
    plt.title(titulo,
              fontsize=14)
    plt.xlabel("")
    plt.ylabel('ENA (MWmed)')
    for i, (eafbs_subs, nome) in enumerate(zip(eafbms, nomes)):
        # Agrupa as energias por mes de estudo
        eafb = eafbs_subs[sub].energias_por_ano
        eafb_mes_estudo: List[np.ndarray] = []
        for ano in anos:
            for mes in meses:
                eafb_mlt = eafb[ano][mes, :] / mlt[sub][mes]
                eafb_mes_estudo.append(eafb_mlt)
        
        # Desenha o boxplot para cada mês de estudo
        h = plt.boxplot(eafb_mes_estudo,
                        positions=x_boxes[i],
                        whis=(0, 100),
                        patch_artist=True,
                        boxprops={"facecolor": CORES[i],
                                  "color": CORES[i]},
                        capprops={"color": CORES[i]},
                        whiskerprops={"color": CORES[i]},
                        flierprops={"color": CORES[i],
                                    "markeredgecolor": CORES[i]},
                        medianprops={"color": "black"})
    
    plt.xticks(ticks=x,
               labels=xlabels_boxes[:len(x)])
    plt.tight_layout()
    # Cria legenda customizada
    custom_leg = [Line2D([], [],
                         color=CORES[i],
                         marker="s",
                         linestyle="None",
                         markersize=12)
                  for i in range(len(nomes))]
    fig.legend(handles=custom_leg,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(nomes))
    plt.subplots_adjust(bottom=0.140)
    plt.savefig(dir_saida)
    plt.close()

# Gera os gráficos "Cabeleira" para o SUL
def grafico_cenarios_ena_sul_compara(eafbms: List[Dict[str, Eafbm00]],
                                     nomes: List[str],
                                     titulo: str,
                                     dir_saida: str):
    sub = "SUL"
    n_meses = 12 * len(anos)
    x = np.array(range(0, 2 * n_meses, 2))
    x_boxes = [x + i * 0.5 for i in range(len(eafbms))]
    min_y = {s: 1e6 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(figsize=(10, 5))
    plt.title(titulo,
              fontsize=14)
    plt.xlabel("")
    plt.ylabel('ENA (MWmed)')
    for i, (eafbs_subs, nome) in enumerate(zip(eafbms, nomes)):
        # Agrupa as energias por mes de estudo
        eafb = eafbs_subs[sub].energias_por_ano
        eafb_mes_estudo: List[np.ndarray] = []
        for ano in anos:
            for mes in meses:
                eafb_mlt = eafb[ano][mes, :] / mlt[sub][mes]
                eafb_mes_estudo.append(eafb_mlt)
        
        # Desenha o boxplot para cada mês de estudo
        h = plt.boxplot(eafb_mes_estudo,
                        positions=x_boxes[i],
                        whis=(0, 100),
                        # notch=True,
                        patch_artist=True,
                        boxprops={"facecolor": CORES_BOXES[i],
                                  "color": CORES_BOXES[i]},
                        capprops={"color": CORES_BOXES[i]},
                        whiskerprops={"color": CORES_BOXES[i]},
                        flierprops={"color": CORES_BOXES[i],
                                    "markeredgecolor": CORES_BOXES[i]},
                        medianprops={"color": CORES_BOXES[i]})
        handlers_legendas.append(h)
        
    
    plt.xticks(ticks=x,
               labels=xlabels_boxes[:len(x)])
    plt.tight_layout()
    # Cria legenda customizada
    custom_leg = [Line2D([], [],
                         color=CORES_BOXES[i],
                         marker="s",
                         linestyle="None",
                         markersize=12)
                  for i in range(len(nomes))]
    fig.legend(handles=custom_leg,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=len(nomes))
    plt.subplots_adjust(bottom=0.140)
    plt.savefig(dir_saida)
    plt.close()

grafico_cenarios_ena_sul([eafbm_sul50_parp,
                          eafbm_oficial_parp,
                          eafbm_sul150_parp],
                         ["Sul 50% MLT PAR(p)",
                          "Sul 100% MLT PAR(p)",
                          "Sul 150% MLT PAR(p)",],
                         "Distribuição da ENA SUL - PAR(p)",
                         "saidas/teste20_ena_cenarios_parp.png")

grafico_cenarios_ena_sul([eafbm_sul50_parpa,
                          eafbm_oficial_parpa,
                          eafbm_sul150_parpa],
                         ["Sul 50% MLT PAR(p)-A",
                          "Sul 100% MLT PAR(p)-A",
                          "Sul 150% MLT PAR(p)-A",],
                         "Distribuição da ENA SUL - PAR(p)-A",
                         "saidas/teste20_ena_cenarios_parpa.png")

grafico_cenarios_ena_sul_compara([eafbm_sul50_parpa,
                                  eafbm_sul50_parp],
                                 ["Sul 50% MLT PAR(p)-A",
                                  "Sul 50% MLT PAR(p)",],
                                 "Distribuição da ENA SUL - PAR(p) e PAR(p)-A - 50% MLT",
                                 "saidas/teste20_ena_cenarios_parp_parpa_50.png")

grafico_cenarios_ena_sul_compara([eafbm_oficial_parpa,
                                  eafbm_oficial_parp],
                                 ["Sul 100% MLT PAR(p)-A",
                                  "Sul 100% MLT PAR(p)",],
                                 "Distribuição da ENA SUL - PAR(p) e PAR(p)-A - 100% MLT",
                                 "saidas/teste20_ena_cenarios_parp_parpa_100.png")

grafico_cenarios_ena_sul_compara([eafbm_sul150_parpa,
                                  eafbm_sul150_parp],
                                 ["Sul 150% MLT PAR(p)-A",
                                  "Sul 150% MLT PAR(p)",],
                                 "Distribuição da ENA SUL - PAR(p) e PAR(p)-A - 150% MLT",
                                 "saidas/teste20_ena_cenarios_parp_parpa_150.png")
