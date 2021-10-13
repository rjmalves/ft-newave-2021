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
from inewave.newave.modelos.parp import PARp
from inewave.nwlistop.mediasmerc import LeituraMediasMerc
from inewave.nwlistop.mediassin import LeituraMediasSIN
from inewave.nwlistop.eafbm00 import LeituraEafbm00
from inewave.newave.parp import LeituraPARp
from inewave.nwlistop.modelos.eafbm00 import Eafbm00
from inewave.nwlistop.modelos.mediasmerc import MediasMerc
from inewave.nwlistop.modelos.mediassin import MediasSIN
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
         "springgreen",
         "deepskyblue",
         "orangered",
         "springgreen",
         "deepskyblue"]

CORES_BOXES = ["orangered",
               "silver"]

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
           "", "", "", "ABR\n2025", "", "", "", "", "", "", "NOV\n2025", ""]

xlabels_boxes = ["JAN\n2021", "FEV\n2021", "MAR\n2021", "ABR\n2021",
                 "MAI\n2021", "JUN\n2021", "JUL\n2021", "AGO\n2021",
                 "SET\n2021", "OUT\n2021", "NOV\n2021", "DEZ\n2021"]

xlabels_media = ["JAN", "FEV", "MAR", "ABR",
                 "MAI", "JUN", "JUL", "AGO",
                 "SET", "OUT", "NOV", "DEZ"]

mlt = {"SUL": np.ones((12,)),
       "SUDESTE": np.ones((12,)),
       "NORDESTE": np.ones((12,)),
       "NORTE": np.ones((12,))}

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
                                     alpha=0.8,
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


# Gera os gráficos de CMO
def grafico_cmo(medias: List[MediasMerc],
                nomes: List[str],
                titulo: str,
                dir_saida: str):
    n_meses = len(medias[0].custo_marginal_operacao["SUL"])
    x = range(n_meses)
    min_y = {s: 1e5 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(titulo,
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='CMO (R$/MWh)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        for s, sub in enumerate(SUBMERCADOS):
            # Decide qual subplot usar
            subx = int(s / 2)
            suby = s % 2
            cmo = media.custo_marginal_operacao[sub]
            min_y[sub] = min([min_y[sub]] + list(cmo))
            max_y[sub] = max([max_y[sub]] + list(cmo))
            h = axs[subx, suby].plot(x,
                                     cmo,
                                     linewidth=3,
                                     linestyle=ESTILOS[i],
                                     color=CORES[i],
                                     alpha=0.8,
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


grafico_cmo([medias_sul50_parp,
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
            "CMO por Submercado",
            "saidas/teste20_cmo.png")


# Gera os gráficos de EARM
def grafico_earm(medias: List[MediasMerc],
                 nomes: List[str],
                 titulo: str,
                 dir_saida: str):
    n_meses = len(medias[0].energias_armazenadas_percentuais["SUL"])
    x = range(n_meses)
    min_y = {s: 1e5 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(titulo,
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='EARM (% EARMax)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        for s, sub in enumerate(SUBMERCADOS):
            # Decide qual subplot usar
            subx = int(s / 2)
            suby = s % 2
            earm = media.energias_armazenadas_percentuais[sub]
            min_y[sub] = min([min_y[sub]] + list(earm))
            max_y[sub] = max([max_y[sub]] + list(earm))
            h = axs[subx, suby].plot(x,
                                     earm,
                                     linewidth=3,
                                     linestyle=ESTILOS[i],
                                     color=CORES[i],
                                     alpha=0.8,
                                     label=nome)
            handlers_legendas.append(h)
            axs[subx, suby].set_title(sub)
    for s, sub in enumerate(SUBMERCADOS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, n_meses-1)
        axs[subx, suby].set_ylim(0, 100)
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


grafico_earm([medias_sul50_parp,
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
             "EARM por Submercado",
             "saidas/teste20_earm.png")


# Gera os gráficos de GHID
def grafico_ghid(medias: List[MediasMerc],
                 nomes: List[str],
                 titulo: str,
                 dir_saida: str):
    n_meses = len(medias[0].geracao_hidraulica_total["SUL"])
    x = range(n_meses)
    min_y = {s: 1e5 for s in SUBMERCADOS}
    max_y = {s: 0 for s in SUBMERCADOS}
    handlers_legendas = []
    # Cria o objeto de figura
    fig, axs = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(titulo,
                 fontsize=14)
    for ax in axs.flat:
        ax.set(xlabel='', ylabel='Ger. Hid (MWmed)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        for s, sub in enumerate(SUBMERCADOS):
            # Decide qual subplot usar
            subx = int(s / 2)
            suby = s % 2
            ghid = media.geracao_hidraulica_total[sub]
            min_y[sub] = min([min_y[sub]] + list(ghid))
            max_y[sub] = max([max_y[sub]] + list(ghid))
            h = axs[subx, suby].plot(x,
                                     ghid,
                                     linewidth=3,
                                     linestyle=ESTILOS[i],
                                     color=CORES[i],
                                     alpha=0.8,
                                     label=nome)
            handlers_legendas.append(h)
            axs[subx, suby].set_title(sub)
    for s, sub in enumerate(SUBMERCADOS):
        subx = int(s / 2)
        suby = s % 2
        axs[subx, suby].set_xlim(0, n_meses-1)
        # axs[subx, suby].set_ylim(0, 100)
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


grafico_ghid([medias_sul50_parp,
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
             "Geração Hidraulica por Submercado",
             "saidas/teste20_ghid.png")


# # Lê os arquivos MEDIAS-SIN
sin_oficial_parp = LeituraMediasSIN(dir_sul100_parp).le_arquivo()
sin_oficial_parpa = LeituraMediasSIN(dir_sul100_parpa).le_arquivo()
sin_sul50_parp = LeituraMediasSIN(dir_sul50_parp).le_arquivo()
sin_sul50_parpa = LeituraMediasSIN(dir_sul50_parpa).le_arquivo()
sin_sul150_parp = LeituraMediasSIN(dir_sul150_parp).le_arquivo()
sin_sul150_parpa = LeituraMediasSIN(dir_sul150_parpa).le_arquivo()


# Gera os gráficos de EARM
def grafico_earm_sin(medias: List[MediasSIN],
                     nomes: List[str],
                     titulo: str,
                     dir_saida: str):
    n_meses = len(medias[0].energias_armazenadas_percentuais)
    x = range(n_meses)
    handlers_legendas = []
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title(titulo)
    plt.ylabel('EARM (% EARMax)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        earm = media.energias_armazenadas_percentuais
        h = ax.plot(x,
                    earm,
                    linewidth=3,
                    linestyle=ESTILOS[i],
                    color=CORES[i],
                    alpha=0.8,
                    label=nome)
        handlers_legendas.append(h)
    ax.set_xlim(0, len(x)-1)
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=3)
    plt.subplots_adjust(bottom=0.185)
    plt.savefig(dir_saida)
    plt.close()


grafico_earm_sin([sin_sul50_parp,
                  sin_oficial_parp,
                  sin_sul150_parp,
                  sin_sul50_parpa,
                  sin_oficial_parpa,
                  sin_sul150_parpa],
                 ["Sul 50% MLT PAR(p)",
                  "Sul 100% MLT PAR(p)",
                  "Sul 150% MLT PAR(p)",
                  "Sul 50% MLT PAR(p)-A",
                  "Sul 100% MLT PAR(p)-A",
                  "Sul 150% MLT PAR(p)-A"],
                 "EARM SIN",
                 "saidas/teste20_earm_sin.png")


# Gera os gráficos de ENA
def grafico_ena_sin(medias: List[MediasSIN],
                    nomes: List[str],
                    titulo: str,
                    dir_saida: str):
    n_meses = len(medias[0].energia_natural_afluente)
    x = range(n_meses)
    handlers_legendas = []
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title(titulo)
    plt.ylabel('ENA (MWmed)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        earm = media.energia_natural_afluente
        h = ax.plot(x,
                    earm,
                    linewidth=3,
                    linestyle=ESTILOS[i],
                    color=CORES[i],
                    alpha=0.8,
                    label=nome)
        handlers_legendas.append(h)
    ax.set_xlim(0, len(x)-1)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=3)
    plt.subplots_adjust(bottom=0.185)
    plt.savefig(dir_saida)
    plt.close()


grafico_ena_sin([sin_sul50_parp,
                 sin_oficial_parp,
                 sin_sul150_parp,
                 sin_sul50_parpa,
                 sin_oficial_parpa,
                 sin_sul150_parpa],
                ["Sul 50% MLT PAR(p)",
                 "Sul 100% MLT PAR(p)",
                 "Sul 150% MLT PAR(p)",
                 "Sul 50% MLT PAR(p)-A",
                 "Sul 100% MLT PAR(p)-A",
                 "Sul 150% MLT PAR(p)-A"],
                "ENA SIN",
                "saidas/teste20_ena_sin.png")


# Gera os gráficos de ENA
def grafico_ghid_sin(medias: List[MediasSIN],
                     nomes: List[str],
                     titulo: str,
                     dir_saida: str):
    n_meses = len(medias[0].geracao_hidraulica_total)
    x = range(n_meses)
    handlers_legendas = []
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title(titulo)
    plt.ylabel('Ger. Hid. (MWmed)')
    for i, (media, nome) in enumerate(zip(medias, nomes)):
        earm = media.geracao_hidraulica_total
        h = ax.plot(x,
                    earm,
                    linewidth=3,
                    linestyle=ESTILOS[i],
                    color=CORES[i],
                    alpha=0.8,
                    label=nome)
        handlers_legendas.append(h)
    ax.set_xlim(0, len(x)-1)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels,
                       fontsize=9)
    plt.tight_layout()
    fig.legend(handlers_legendas,
               labels=nomes,
               loc="lower center",
               borderaxespad=0.2,
               ncol=3)
    plt.subplots_adjust(bottom=0.185)
    plt.savefig(dir_saida)
    plt.close()


grafico_ghid_sin([sin_sul50_parp,
                  sin_oficial_parp,
                  sin_sul150_parp,
                  sin_sul50_parpa,
                  sin_oficial_parpa,
                  sin_sul150_parpa],
                 ["Sul 50% MLT PAR(p)",
                  "Sul 100% MLT PAR(p)",
                  "Sul 150% MLT PAR(p)",
                  "Sul 50% MLT PAR(p)-A",
                  "Sul 100% MLT PAR(p)-A",
                  "Sul 150% MLT PAR(p)-A"],
                 "Geração Hidráulica SIN",
                 "saidas/teste20_ghid_sin.png")

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


# Gera os gráficos "Cabeleira" para o SUL
def grafico_cenarios_ena_sul(eafbms: List[Dict[str, Eafbm00]],
                             nomes: List[str],
                             titulo: str,
                             dir_saida: str):
    sub = "SUL"
    n_meses = 12 * len(anos)
    x = np.array(range(0, 3 * n_meses, 3))
    x_boxes = [x + i * 0.5 for i in range(len(eafbms))]

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
        plt.boxplot(eafb_mes_estudo,
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
                        medianprops={"color": 'black'})
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
                         ["Sul 50% MLT",
                          "Sul 100% MLT",
                          "Sul 150% MLT"],
                         "Distribuição da ENA SUL - PAR(p)",
                         "saidas/teste20_ena_box_parp.png")

grafico_cenarios_ena_sul([eafbm_sul50_parpa,
                          eafbm_oficial_parpa,
                          eafbm_sul150_parpa],
                         ["Sul 50% MLT",
                          "Sul 100% MLT",
                          "Sul 150% MLT"],
                         "Distribuição da ENA SUL - PAR(p)-A",
                         "saidas/teste20_ena_box_parpa.png")

grafico_cenarios_ena_sul_compara([eafbm_sul50_parpa,
                                  eafbm_sul50_parp],
                                 ["PAR(p)-A",
                                  "PAR(p)"],
                                 "Distribuição da ENA SUL - 50% MLT",
                                 "saidas/teste20_ena_box_parp_parpa_50.png")

grafico_cenarios_ena_sul_compara([eafbm_oficial_parpa,
                                  eafbm_oficial_parp],
                                 ["PAR(p)-A",
                                  "PAR(p)"],
                                 "Distribuição da ENA SUL - 100% MLT",
                                 "saidas/teste20_ena_box_parp_parpa_100.png")

grafico_cenarios_ena_sul_compara([eafbm_sul150_parpa,
                                  eafbm_sul150_parp],
                                 ["PAR(p)-A",
                                  "PAR(p)"],
                                 "Distribuição da ENA SUL - 150% MLT",
                                 "saidas/teste20_ena_box_parp_parpa_150.png")


# Lê o parp.dat e plota as médias móveis de 12 meses
parp_sul50_parpa = LeituraPARp(dir_sul50_parpa).le_arquivo()
parp_sul100_parpa = LeituraPARp(dir_sul100_parpa).le_arquivo()
parp_sul150_parpa = LeituraPARp(dir_sul150_parpa).le_arquivo()


# Gera os gráficos de média móvel da ENA
def grafico_media_movel(parps: List[PARp],
                        nomes: List[str],
                        titulo: str,
                        dir_saida: str):
    x = np.array(range(0, 1 * 12, 1))
    x_boxes = [x + i * 0.5 for i in range(len(parps))]
    handlers_legendas = []
    # Cria o objeto de figura
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title(titulo)
    plt.ylabel('ENA (MWmed)')
    for i, (parp, nome) in enumerate(zip(parps, nomes)):
        media_sul = parp.series_medias_ree(2)[2021]
        media_iguacu = parp.series_medias_ree(11)[2021]
        serie_media = []
        for mes in range(12):
            dados_mes = media_sul[1:, mes] + media_iguacu[1:, mes]
            serie_media.append(dados_mes)

        # Desenha o boxplot para cada mês de estudo
        h = plt.boxplot(serie_media,
                        positions=x_boxes[i],
                        whis=(0, 100),
                        patch_artist=True,
                        boxprops={"facecolor": "silver",
                                  "color": "silver"},
                        capprops={"color": "silver"},
                        whiskerprops={"color": "silver"},
                        flierprops={"color": "silver",
                                    "markeredgecolor": "silver"},
                        medianprops={"color": "black"})
        handlers_legendas.append(h)
    plt.xticks(ticks=x,
               labels=xlabels_media[:len(x)])
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.085)
    plt.savefig(dir_saida)
    plt.close()


grafico_media_movel([parp_sul50_parpa],
                    ["ENA Sul"],
                    "Distribuição das Médias Móveis - ENA SUL",
                    "saidas/teste20_media_movel_parpa.png")
