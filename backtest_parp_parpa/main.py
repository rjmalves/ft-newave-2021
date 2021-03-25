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
    dir_cvar_50x25_parp = os.getenv("DIR_CVAR_5025_PARP")
    dir_cvar_50x35_parp = os.getenv("DIR_CVAR_5035_PARP")
    dir_cvar_50x50_parp = os.getenv("DIR_CVAR_5050_PARP")
    dir_cvar_25x50_parp = os.getenv("DIR_CVAR_2550_PARP")
    dir_cvar_50x25_parpa = os.getenv("DIR_CVAR_5025_PARPA")
    dir_cvar_50x35_parpa = os.getenv("DIR_CVAR_5035_PARPA")
    dir_cvar_50x50_parpa = os.getenv("DIR_CVAR_5050_PARPA")
    dir_cvar_25x50_parpa = os.getenv("DIR_CVAR_2550_PARPA")

    # Constroi os casos
    oficial = Caso.constroi_caso_de_pasta(dir_oficial,
                                          "Oficial")
    nome = "$\\alpha$ = 50%, $\\lambda$ = 25%"
    cvar_50x25_parp = Caso.constroi_caso_de_pasta(dir_cvar_50x25_parp,
                                                  nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 35%"
    cvar_50x35_parp = Caso.constroi_caso_de_pasta(dir_cvar_50x35_parp,
                                                  nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 50%"
    cvar_50x50_parp = Caso.constroi_caso_de_pasta(dir_cvar_50x50_parp,
                                                  nome)
    nome = "$\\alpha$ = 25%, $\\lambda$ = 50%"
    cvar_25x50_parp = Caso.constroi_caso_de_pasta(dir_cvar_25x50_parp,
                                                  nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 25%"
    cvar_50x25_parpa = Caso.constroi_caso_de_pasta(dir_cvar_50x25_parpa,
                                                   nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 35%"
    cvar_50x35_parpa = Caso.constroi_caso_de_pasta(dir_cvar_50x35_parpa,
                                                   nome)
    nome = "$\\alpha$ = 50%, $\\lambda$ = 50%"
    cvar_50x50_parpa = Caso.constroi_caso_de_pasta(dir_cvar_50x50_parpa,
                                                   nome)
    nome = "$\\alpha$ = 25%, $\\lambda$ = 50%"
    cvar_25x50_parpa = Caso.constroi_caso_de_pasta(dir_cvar_25x50_parpa,
                                                   nome)


    casos = [
             oficial,
             cvar_50x25_parpa,
             cvar_50x35_parpa,
             cvar_50x50_parpa,
             cvar_25x50_parpa,
             cvar_50x25_parp,
             cvar_50x35_parp,
             cvar_50x50_parp,
             cvar_25x50_parp
            ]
    saida = os.getenv("DIR_SAIDA")

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

    casos_cmp = [
                 oficial,
                 cvar_50x35_parp,
                 cvar_50x35_parpa
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
    for c in casos:
        exporta_dados(c, saida)


if __name__ == "__main__":
    main()
