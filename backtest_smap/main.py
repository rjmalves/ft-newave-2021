from caso import Caso  # type: ignore
from graficos import grafico_cmo_subsistema  # type: ignore
from graficos import grafico_deficit_subsistema
from graficos import grafico_earm_sin  # type: ignore
from graficos import grafico_earm_subsistema  # type: ignore
from graficos import grafico_gt_sin  # type: ignore
from graficos import grafico_ghid_sin  # type: ignore
from graficos import grafico_gt_subsistema  # type: ignore
from graficos import grafico_ghid_subsistema  # type: ignore
from graficos import exporta_dados  # type: ignore

import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_vigente_novo = os.getenv("DIR_VIGENTE_NOVO")
    dir_1omes_2semanas = os.getenv("DIR_1MES_2SEMANAS")
    dir_perfeito_1omes = os.getenv("DIR_PERFEITO_1MES")
    dir_perfeito = os.getenv("DIR_PERFEITO")
    dir_proposto = os.getenv("DIR_PROPOSTO")

    # Constroi os casos
    vigente = Caso.constroi_caso_de_pasta(dir_vigente_novo,
                                          "Vigente")
    nome = "SMAP 1º Mês (2 Semanas)"
    mes2semanas = Caso.constroi_caso_de_pasta(dir_1omes_2semanas,
                                              nome)
    nome = "SMAP Perfeito 1º Mês"
    perfeito1mes = Caso.constroi_caso_de_pasta(dir_perfeito_1omes,
                                               nome)
    # nome = "SMAP Perfeito"
    # perfeito = Caso.constroi_caso_de_pasta(dir_perfeito,
    #                                        nome)
    nome = "SMAP Proposto"
    proposto = Caso.constroi_caso_de_pasta(dir_proposto,
                                           nome)

    casos = [
             vigente,
             mes2semanas,
             perfeito1mes,
            #  perfeito,
             proposto
             ]

    saida = os.getenv("DIR_SAIDA_SMAP")

    # Gera os gráficos
    # CMO por subsistema
    grafico_cmo_subsistema(casos, saida)
    # EARM por subsistema
    grafico_earm_subsistema(casos, saida)
    # GT por subsistema
    grafico_gt_subsistema(casos, saida)
    # Ghid por subsistema
    grafico_ghid_subsistema(casos, saida)
    # Déficit por subsistema
    grafico_deficit_subsistema(casos, saida)
    # EARM para SIN
    grafico_earm_sin(casos, saida)
    # GT para SIN
    grafico_gt_sin(casos, saida)
    # GHid para SIN
    grafico_ghid_sin(casos, saida)

    # Exporta os dados
    for c in casos:
        exporta_dados(c, saida)


if __name__ == "__main__":
    main()
