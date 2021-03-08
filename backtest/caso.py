
from idecomp.config import SUBSISTEMAS  # type: ignore
from idecomp.decomp.modelos.relato import Relato  # type: ignore
from idecomp.decomp.relato import LeituraRelato  # type: ignore
from typing import Dict, List
import numpy as np
import os


class Caso:
    """
    """
    def __init__(self,
                 nome: str,
                 n_revs: int,
                 cmo_subsis: Dict[str, List[float]],
                 earm_subsis: Dict[str, List[float]],
                 earm_sin: List[float],
                 gt_subsis: Dict[str, List[float]],
                 gt_sin: List[float]
                 ):
        self.nome = nome
        self.n_revs = n_revs
        self.cmo_subsis = cmo_subsis
        self.earm_subsis = earm_subsis
        self.earm_sin = earm_sin
        self.gt_subsis = gt_subsis
        self.gt_sin = gt_sin

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
        cmo_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        gt_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        gt_sin: List[float] = []
        earm_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        earm_sin: List[float] = []
        primeiro = True
        for _, re in relatos.items():
            cmos = re.cmo_medio_subsistema
            gts = re.geracao_termica_subsistema
            earmax = re.armazenamento_maximo_subsistema
            earmax_sin = sum(list(earmax.values()))
            for s in SUBSISTEMAS:
                cmo_subsis[s].append(cmos[s][0])
                gt_subsis[s].append(np.sum(gts[s]))
                if primeiro:
                    earms = re.energia_armazenada_inicial_subsistema[s]
                else:
                    earms = re.energia_armazenada_subsistema[s][0]
                earm_subsis[s].append(earms)
            # Calcula GT do SIN
            gt_sin_r = sum([gt_subsis[s][-1] for s in SUBSISTEMAS])
            gt_sin.append(gt_sin_r)
            # Calcula EARM do SIN
            earm_sin_r = (sum([(earm_subsis[s][-1] / 100) * earmax[s]
                                for s in SUBSISTEMAS]) / earmax_sin)
            earm_sin.append(100 * earm_sin_r)
            if primeiro:
                primeiro = False
        
        n_revs = len(relatos_pasta)

        return Caso(nome,
                    n_revs,
                    cmo_subsis,
                    earm_subsis,
                    earm_sin,
                    gt_subsis,
                    gt_sin)
