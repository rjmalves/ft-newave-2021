from idecomp.decomp.modelos.relato import Relato
from idecomp.decomp.relato import LeituraRelato
from typing import Dict, List
import numpy as np
import os

SUBSISTEMAS = ["SE", "S", "NE", "N"]

class Caso:
    """
    """
    def __init__(self,
                 nome: str,
                 n_revs: int,
                 cmo_subsis: Dict[str, float],
                 earm_subsis: Dict[str, float],
                 gt_subsis: Dict[str, float]
                 ):
        self.nome = nome
        self.n_revs = n_revs
        self.cmo_subsis = cmo_subsis
        self.earm_subsis = earm_subsis
        self.gt_subsis = gt_subsis

    @classmethod
    def constroi_caso_de_pasta(cls,
                               dir: str,
                               nome: str):
        """
        Constroi um objeto Caso a partir de um diretório
        com saídas de rodadas encadeadas de DECOMP.
        """
        # Busca por todos os relatos na pasta
        arqs_pasta = os.listdir(dir)

        # Filtra os relatos
        relatos_pasta = [d for d in arqs_pasta if "relato" in d]
        relatos_pasta.sort()

        # Lê os relatos
        relatos: Dict[str, Relato] = {}
        for r in relatos_pasta:
            relatos[r] = LeituraRelato(dir).le_arquivo(r)

        # Prepara as listas de dados
        num_casos = len(relatos_pasta)
        cmo_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        gt_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        earm_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        primeiro = True
        for a, r in relatos.items():
            cmos = r.cmo_medio_subsistema
            gts = r.geracao_termica_subsistema
            for s in SUBSISTEMAS:
                cmo_subsis[s].append(cmos[s][0])
                gt_subsis[s].append(np.sum(gts[s]))
                if primeiro:
                    earms = r.energia_armazenada_inicial_subsistema[s]
                else:
                    earms = r.energia_armazenada_subsistema[s][0]
                earm_subsis[s].append(earms)
            if primeiro:
                primeiro = False
        
        n_revs = len(relatos_pasta)

        return Caso(nome,
                    n_revs,
                    cmo_subsis,
                    earm_subsis,
                    gt_subsis)
