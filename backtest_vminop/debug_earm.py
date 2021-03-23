import os
from typing import Dict
from idecomp.decomp.modelos.relato import Relato  # type: ignore
from idecomp.decomp.relato import LeituraRelato  # type: ignore


def main():
    # Diretórios com as saídas do backtest no formato
    # relato_AAAA_MM.rvX
    dir_oficial = "/home/rogerio/ONS/backtest/decomp/oficial/saidas_decomp"
    dir_cvar_30x35 = "/home/rogerio/ONS/backtest/decomp/cvar_30x35/saidas_decomp"
    dir_cvar_40x35 = "/home/rogerio/ONS/backtest/decomp/cvar_40x35/saidas_decomp"
    dir_cvar_50x25 = "/home/rogerio/ONS/backtest/decomp/cvar_50x25/saidas_decomp"
    dir_cvar_50x35 = "/home/rogerio/ONS/backtest/decomp/cvar_50x35/saidas_decomp"
    dir_cvar_50x50 = "/home/rogerio/ONS/backtest/decomp/cvar_50x50/saidas_decomp"

    dirs = [dir_oficial,
            dir_cvar_30x35,
            dir_cvar_40x35,
            dir_cvar_50x25,
            dir_cvar_50x35,
            dir_cvar_50x50]

    for dir in dirs:
        print(dir)
        # Busca por todos os relatos na pasta
        arqs_pasta = os.listdir(dir)

        # Filtra os relatos
        relatos_pasta = [d for d in arqs_pasta if "relato" in d]
        relatos_pasta.sort()

        # Lê os relatos
        relatos: Dict[str, Relato] = {}
        print("Lendo relatos...")
        for r in relatos_pasta:
            relatos[r] = LeituraRelato(dir).le_arquivo(r)
        
        # Para cada relato, printa o EARM S inicial e final da 1ª semana
        print("ARQ;EARM_S_INI;EARM_S_1a_SEM")
        for arq, r in relatos.items():
            earm_ini = r.energia_armazenada_inicial_subsistema["S"]
            earm_1 = r.energia_armazenada_subsistema["S"][0]
            str_saida = f"{arq};{earm_ini};{earm_1}"
            print(str_saida)
        print("")
        print("FIM")
        print("")

if __name__ == "__main__":
    main()
