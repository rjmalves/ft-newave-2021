from caso import Caso  # type: ignore
from graficos import grafico_cmo_subsistema, grafico_deficit_subsistema  # type: ignore
from graficos import grafico_earm_sin  # type: ignore
from graficos import grafico_earm_subsistema  # type: ignore
from graficos import grafico_gt_sin  # type: ignore
from graficos import grafico_gt_subsistema  # type: ignore
from graficos import exporta_dados  # type: ignore

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = os.getenv("DIR_OFICIAL")
    dir_soft_p2000 = os.getenv("DIR_SOFT_P2000")
    dir_hard_p2000 = os.getenv("DIR_HARD_P2000")
    dir_hard_pBigM = os.getenv("DIR_HARD_PBIGM")
    dir_hard_pBigM_TD = os.getenv("DIR_HARD_PBIGM_TD")
    env = "DIR_MIX_HARD_P2000_SOFT_P2000"
    dir_mix_hard_p2000_soft_p2000 = os.getenv(env)
    env = "DIR_MIX_HARD_PBIGM_SOFT_P2000"
    dir_mix_hard_pBigM_soft_p2000 = os.getenv(env)
    env = "DIR_MIX_HARD_P2000_ULTSEMANA_SOFT_P2000"
    dir_mix_hard_p2000_ultSemana_soft_p2000 = os.getenv(env)

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

    saida = os.getenv("DIR_SAIDA")

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
