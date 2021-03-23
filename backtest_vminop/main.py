from caso import Caso  # type: ignore
from graficos import grafico_cmo_subsistema, grafico_deficit_subsistema  # type: ignore
from graficos import grafico_earm_sin  # type: ignore
from graficos import grafico_earm_subsistema  # type: ignore
from graficos import grafico_gt_sin  # type: ignore
from graficos import grafico_gt_subsistema  # type: ignore
from graficos import exporta_dados  # type: ignore


def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = "/home/rogerio/ONS/vminop/saidas_oficial_semRHE/saidas_decomp"
    dir_soft_p2000 = "/home/rogerio/ONS/vminop/saidas_RHEsoft_penal2000/saidas_decomp"
    dir_hard_p2000 = "/home/rogerio/ONS/vminop/saidas_RHEhard_penal2000/saidas_decomp"
    dir_hard_pBigM = "/home/rogerio/ONS/vminop/saidas_RHEhard_penalBigM/saidas_decomp"
    dir_hard_pBigM_TD = "/home/rogerio/ONS/vminop/saidas_RHEhard_penalBigM_TD/saidas_decomp"
    dir_mix_hard_p2000_soft_p2000 = "/home/rogerio/ONS/vminop/saidas_RHEmix_hard2000_soft2000/saidas_decomp"
    dir_mix_hard_pBigM_soft_p2000 = "/home/rogerio/ONS/vminop/saidas_RHEmix_hardBigM_soft2000/saidas_decomp"
    dir_mix_hard_p2000_ultSemana_soft_p2000 = "/home/rogerio/ONS/vminop/saidas_RHEmix_hard2000_ultSemana_soft2000/saidas_decomp"

    # Constroi os casos
    oficial = Caso.constroi_caso_de_pasta(dir_oficial,
                                          "Oficial")
    soft_p2000 = Caso.constroi_caso_de_pasta(dir_soft_p2000,
                                             "RHE Soft")
    hard_p2000 = Caso.constroi_caso_de_pasta(dir_hard_p2000,
                                             "RHE Hard penal. 2000")
    hard_pBigM = Caso.constroi_caso_de_pasta(dir_hard_pBigM,
                                             "RHE Hard penal. BigM")
    hard_pBigM_TD = Caso.constroi_caso_de_pasta(dir_hard_pBigM_TD,
                                                "RHE Hard penal. BigM + TD")
    mix_hard_p2000_soft_p2000 = Caso.constroi_caso_de_pasta(dir_mix_hard_p2000_soft_p2000,
                                                            "RHE Mix hard 2000, soft 2000")
    mix_hard_pBigM_soft_p2000 = Caso.constroi_caso_de_pasta(dir_mix_hard_pBigM_soft_p2000,
                                                            "RHE Mix hard BigM, soft 2000")
    mix_hard_p2000_ultSemana_soft_p2000 = Caso.constroi_caso_de_pasta(dir_mix_hard_p2000_ultSemana_soft_p2000,
                                                                      "RHE Mix hard 2000 Ult. Semana, soft 2000")

    casos = [
             oficial,
             soft_p2000,
             hard_p2000,
             hard_pBigM,
             hard_pBigM_TD,
             mix_hard_p2000_soft_p2000,
             mix_hard_pBigM_soft_p2000,
             mix_hard_p2000_ultSemana_soft_p2000
            ]
    saida = "saidas/vminop"

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

    # Exporta os dados
    for c in casos:
        exporta_dados(c, saida)


if __name__ == "__main__":
    main()
