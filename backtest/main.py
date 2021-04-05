from caso import Caso  # type: ignore
from graficos import grafico_cmo_subsistema  # type: ignore
from graficos import grafico_deficit_subsistema
from graficos import grafico_earm_sin  # type: ignore
from graficos import grafico_earm_subsistema  # type: ignore
from graficos import grafico_gt_sin  # type: ignore
from graficos import grafico_gt_subsistema  # type: ignore
from graficos import exporta_dados  # type: ignore
from graficos_compara import grafico_cmo_subsistema_dif  # type: ignore
from graficos_compara import grafico_earm_subsistema_dif  # type: ignore
from graficos_compara import grafico_gt_subsistema_dif  # type: ignore
from graficos_compara import grafico_gt_sin_dif  # type: ignore
from graficos_compara import grafico_earm_sin_dif  # type: ignore

import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = os.getenv("DIR_OFICIAL")
    dir_cvar_50x25 = os.getenv("DIR_CVAR_5025")
    dir_cvar_50x35 = os.getenv("DIR_CVAR_5035")
    dir_cvar_50x50 = os.getenv("DIR_CVAR_5050")
    dir_cvar_25x50 = os.getenv("DIR_CVAR_2550")

    # Constroi os casos
    oficial = Caso.constroi_caso_de_pasta(dir_oficial,
                                          "Oficial")
    nome = "$\\alpha$ = 50%, $\\lambda$ = 25%"
    cvar_50x25 = Caso.constroi_caso_de_pasta(dir_cvar_50x25,
                                             nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 35%"
    cvar_50x35 = Caso.constroi_caso_de_pasta(dir_cvar_50x35,
                                             nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 50%"
    cvar_50x50 = Caso.constroi_caso_de_pasta(dir_cvar_50x50,
                                             nome)
    nome = "$\\alpha$ = 25%, $\\lambda$ = 50%"
    cvar_25x50 = Caso.constroi_caso_de_pasta(dir_cvar_25x50,
                                             nome)

    casos = [oficial,
             cvar_50x25,
             cvar_50x35,
             cvar_50x50,
             cvar_25x50
             ]

    saida = os.getenv("DIR_SAIDA")

    # dir_smap = os.getenv("DIR_SMAP")
    # smap = Caso.constroi_caso_de_pasta(dir_smap,
    #                                    "SMAP 1º Mês")
    # casos = [smap]
    # saida = os.getenv("DIR_SAIDA_SMAP")

    # Gera os gráficos
    # CMO por subsistema
    grafico_cmo_subsistema(casos, saida)
    # EARM por subsistema
    grafico_earm_subsistema(casos, saida)
    # GT por subsistema
    grafico_gt_subsistema(casos, saida)
    # Déficit por subsistema
    grafico_deficit_subsistema(casos, saida)
    # EARM para SIN
    grafico_earm_sin(casos, saida)
    # GT para SIN
    grafico_gt_sin(casos, saida)

    # Exporta os dados
    for c in casos:
        exporta_dados(c, saida)

    # Altera o nome do 50x35 para simplificar
    cvar_50x35.nome = "VminOP + PAR(p)-A"

    casos_cmp = [
                 oficial,
                 cvar_50x35
                 ]

    saida_cmp = os.getenv("DIR_SAIDA_CMP")

    print("Gerando diferenças")
    # Gera os gráficos de comparação
    grafico_cmo_subsistema_dif(casos_cmp, saida_cmp)
    grafico_earm_subsistema_dif(casos_cmp, saida_cmp)
    grafico_gt_subsistema_dif(casos_cmp, saida_cmp)
    grafico_earm_sin_dif(casos_cmp, saida_cmp)
    grafico_gt_sin_dif(casos_cmp, saida_cmp)

    # Exporta os dados
    for c in casos_cmp:
        exporta_dados(c, saida_cmp)


if __name__ == "__main__":
    main()
