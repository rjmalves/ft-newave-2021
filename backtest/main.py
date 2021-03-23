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
# TODO - 
# Fazer gráficos cabeleira para o teste 20
# Trocar os diretórios de entrada do backtest para variáveis de ambiente (.env.example)
# Usar python dotenv

def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = ""
    dir_cvar_50x25 = ""
    dir_cvar_50x35 = ""
    dir_cvar_50x50 = ""

    # Constroi os casos
    oficial = Caso.constroi_caso_de_pasta(dir_oficial,
                                          "Oficial")
    cvar_50x25 = Caso.constroi_caso_de_pasta(dir_cvar_50x25,
                                             "$\\alpha$ = 50%, $\\lambda$ = 25%")
    cvar_50x35 = Caso.constroi_caso_de_pasta(dir_cvar_50x35,
                                             "$\\alpha$ = 50%, $\\lambda$ = 35%")
    cvar_50x50 = Caso.constroi_caso_de_pasta(dir_cvar_50x50,
                                             "$\\alpha$ = 50%, $\\lambda$ = 50%")

    casos = [oficial,
             cvar_50x25,
             cvar_50x35,
             cvar_50x50
            ]
    saida = ""

    # dir_smap = "/home/rogerio/ONS/backtest/decomp/smap"
    # smap = Caso.constroi_caso_de_pasta(dir_smap,
    #                                    "SMAP 1º Mês")
    # casos = [smap]
    # saida = "saidas/smap"

    # Gera os gráficos
    # saida = "saidas/smap"
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
                 cvar_50x35
                 ]

    saida_cmp = "saidas/compara"

    grafico_cmo_subsistema_dif(casos_cmp, saida_cmp)
    grafico_earm_subsistema_dif(casos_cmp, saida_cmp)
    grafico_gt_subsistema_dif(casos_cmp, saida_cmp)
    # Gera os gráficos de comparação

    # Exporta os dados
    for c in casos:
        exporta_dados(c, saida)


if __name__ == "__main__":
    main()
