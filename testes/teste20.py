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
from inewave.nwlistop.modelos.mediasmerc import MediasMerc
import matplotlib.pyplot as plt
from typing import List


# Variáveis auxiliares com os diretorios dos casos
dir_base = "/home/rogerio/ONS/validacao_newave2745/"
dir_oficial_parp = dir_base + "pmo_2021_01_oficial_parp"
dir_oficial_parpa = dir_base + "pmo_2021_01_oficial_parpa"
dir_sul50_parp = dir_base + "pmo_2021_01_sul_50_mlt_parp"
dir_sul50_parpa = dir_base + "pmo_2021_01_sul_50_mlt_parpa"
dir_sul150_parp = dir_base + "pmo_2021_01_sul_150_mlt_parp"
dir_sul150_parpa = dir_base + "pmo_2021_01_sul_150_mlt_parpa"

# Lê os arquivos MEDIAS-MERC
medias_oficial_parp = LeituraMediasMerc(dir_oficial_parp).le_arquivo()
medias_oficial_parpa = LeituraMediasMerc(dir_oficial_parpa).le_arquivo()
medias_sul50_parp = LeituraMediasMerc(dir_sul50_parp).le_arquivo()
medias_sul50_parpa = LeituraMediasMerc(dir_sul50_parpa).le_arquivo()
medias_sul150_parp = LeituraMediasMerc(dir_sul150_parp).le_arquivo()
medias_sul150_parpa = LeituraMediasMerc(dir_sul150_parpa).le_arquivo()

# Variáveis auxiliares para os gráficos
CORES = ["orangered",
         "gold",
         "springgreen",
         "orangered",
         "gold",
         "springgreen"]

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
            min_y[sub] = min([min_y[sub]] + list(ena))
            max_y[sub] = max([max_y[sub]] + list(ena))
            h = axs[subx, suby].plot(x,
                                     ena,
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