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

from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

def main():


    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    
    dir_semRHE = os.getenv("DIR_PROSPECTIVO_SEM_RHE")
    dir_comRHE = os.getenv("DIR_PROSPECTIVO_COM_RHE")
    

    # Constroi os casos
    semRHE = Caso.constroi_caso_de_pasta(dir_semRHE,
                                         "Sem RHE")
    comRHE = Caso.constroi_caso_de_pasta(dir_comRHE,
                                         "RHEmix CPAMP")

    casos = [
             semRHE,
             comRHE
            ]
    saida = "saidas/prospectivo"

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

    saida_cmp = os.getenv("DIR_SAIDA_PROSPECTIVO")

    print("Gerando diferenças")
    # Gera os gráficos de comparação
    grafico_cmo_subsistema_dif(casos, saida_cmp)
    grafico_earm_subsistema_dif(casos, saida_cmp)
    grafico_gt_subsistema_dif(casos, saida_cmp)
    grafico_earm_sin_dif(casos, saida_cmp)
    grafico_gt_sin_dif(casos, saida_cmp)

    # Exporta os dados
    for c in casos:
        exporta_dados(c, saida)


if __name__ == "__main__":
    main()
