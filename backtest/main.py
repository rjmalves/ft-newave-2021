from idecomp.decomp.modelos.relato import Relato
from idecomp.decomp.relato import LeituraRelato
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np
import os
from caso import Caso
from caso import SUBSISTEMAS
from graficos import grafico_cmo_subsistema
from graficos import grafico_earm_sin
from graficos import grafico_earm_subsistema
from graficos import grafico_gt_sin
from graficos import grafico_gt_subsistema


def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = "/home/rogerio/ONS/backtest/decomp/oficial/saidas_decomp"
    dir_cvar_30x35 = "/home/rogerio/ONS/backtest/decomp/cvar_30x35/saidas_decomp"
    dir_cvar_40x35 = "/home/rogerio/ONS/backtest/decomp/cvar_40x35/saidas_decomp"
    dir_cvar_50x25 = "/home/rogerio/ONS/backtest/decomp/cvar_50x25/saidas_decomp"
    dir_cvar_50x35 = "/home/rogerio/ONS/backtest/decomp/cvar_50x35/saidas_decomp"
    dir_cvar_50x50 = "/home/rogerio/ONS/backtest/decomp/cvar_50x50/saidas_decomp"

    # Constroi os casos
    oficial = Caso.constroi_caso_de_pasta(dir_oficial,
                                          "Oficial")
    cvar_30x35 = Caso.constroi_caso_de_pasta(dir_cvar_30x35,
                                             "$\\alpha$ = 30%, $\\lambda$ = 35%")
    cvar_40x35 = Caso.constroi_caso_de_pasta(dir_cvar_40x35,
                                             "$\\alpha$ = 40%, $\\lambda$ = 35%")
    cvar_50x25 = Caso.constroi_caso_de_pasta(dir_cvar_50x25,
                                             "$\\alpha$ = 50%, $\\lambda$ = 25%")
    cvar_50x35 = Caso.constroi_caso_de_pasta(dir_cvar_50x35,
                                             "$\\alpha$ = 50%, $\\lambda$ = 35%")
    cvar_50x50 = Caso.constroi_caso_de_pasta(dir_cvar_50x50,
                                             "$\\alpha$ = 50%, $\\lambda$ = 50%")

    casos = [oficial,
             cvar_50x25,
             cvar_50x35,
             cvar_40x35,
             cvar_30x35,
             cvar_50x50]

    # dir_smap = "/home/rogerio/ONS/backtest/decomp/smap"
    # smap = Caso.constroi_caso_de_pasta(dir_smap,
    #                                    "SMAP 1º Mês")
    # casos = [smap]
    # Gera os gráficos
    saida = "saidas/"
    # # CMO por subsistema
    grafico_cmo_subsistema(casos, saida)
    # # EARM por subsistema
    grafico_earm_subsistema(casos, saida)
    # # GT por subsistema
    grafico_gt_subsistema(casos, saida)
    # EARM para SIN
    grafico_earm_sin(casos, saida)
    # GT para SIN
    grafico_gt_sin(casos, saida)

if __name__ == "__main__":
    main()
