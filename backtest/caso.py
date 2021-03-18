
from idecomp.config import SUBSISTEMAS  # type: ignore
from idecomp.decomp.modelos.relato import Relato  # type: ignore
from idecomp.decomp.relato import LeituraRelato  # type: ignore
from typing import Dict, List
import os


class Caso:
    """
    """
    def __init__(self,
                 nome: str,
                 n_revs: int,
                 arquivos: List[str],
                 cmo_subsis: Dict[str, List[float]],
                 earm_subsis: Dict[str, List[float]],
                 earm_sin: List[float],
                 gt_subsis: Dict[str, List[float]],
                 gt_sin: List[float],
                 ghid_subsis: Dict[str, List[float]],
                 ghid_sin: List[float],
                 def_subsis: Dict[str, List[float]],
                 ):
        self.nome = nome
        self.n_revs = n_revs
        self.arquivos = arquivos
        self.cmo_subsis = cmo_subsis
        self.earm_subsis = earm_subsis
        self.earm_sin = earm_sin
        self.gt_subsis = gt_subsis
        self.gt_sin = gt_sin
        self.ghid_subsis = ghid_subsis
        self.ghid_sin = ghid_sin
        self.def_subsis = def_subsis

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
        relatos_pasta = [relatos_pasta[0]] + relatos_pasta

        # Lê os relatos
        relatos: Dict[str, Relato] = {}
        primeiro = True
        for r in relatos_pasta:
            if primeiro:
                relatos[r + "_INI"] = LeituraRelato(dir).le_arquivo(r)
                primeiro = False
            else:
                relatos[r] = LeituraRelato(dir).le_arquivo(r)

        relatos_pasta[0] = relatos_pasta[0] + "_INI"

        # Prepara as listas de dados
        cmo_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        gt_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        gt_sin: List[float] = []
        earm_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        earm_sin: List[float] = []
        ghid_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        ghid_sin: List[float] = []
        def_subsis: Dict[str, List[float]] = {s: [] for s in SUBSISTEMAS}
        for a in relatos_pasta:
            re = relatos[a]
            ghids = re.geracao_hidraulica_subsistema
            defs = re.deficit_subsistema
            cmos = re.cmo_medio_subsistema
            gts = re.geracao_termica_subsistema
            earmax = re.armazenamento_maximo_subsistema
            earmax_sin = sum(list(earmax.values()))
            # Se é o primeiro, só pega o EARM inicial
            if "INI" in a:
                for s in SUBSISTEMAS:
                    earms = re.energia_armazenada_inicial_subsistema[s]
                    earm_subsis[s].append(earms)
                    gt_subsis[s].append(0)
                    cmo_subsis[s].append(0)
                    ghid_subsis[s].append(0)
                    def_subsis[s].append(0)
                earm_sin_r = (sum([(earm_subsis[s][-1] / 100) * earmax[s]
                              for s in SUBSISTEMAS]) / earmax_sin)
                earm_sin.append(100 * earm_sin_r)
                gt_sin.append(0)
                ghid_sin.append(0)
                continue
            # Senão, pega todas as informações
            for s in SUBSISTEMAS:
                cmo_subsis[s].append(cmos[s][0])
                gt_subsis[s].append(gts[s][0])
                ghid_subsis[s].append(ghids[s][0])
                def_subsis[s].append(defs[s][0])
                earms = re.energia_armazenada_subsistema[s][0]
                earm_subsis[s].append(earms)
            # Calcula GT do SIN
            gt_sin_r = sum([gt_subsis[s][-1] for s in SUBSISTEMAS])
            gt_sin.append(gt_sin_r)
            # Calcula GHID do SIN
            gh_sin_r = sum([ghid_subsis[s][-1] for s in SUBSISTEMAS])
            ghid_sin.append(gh_sin_r)
            # Calcula EARM do SIN
            earm_sin_r = (sum([(earm_subsis[s][-1] / 100) * earmax[s]
                               for s in SUBSISTEMAS]) / earmax_sin)
            earm_sin.append(100 * earm_sin_r)
            if primeiro:
                primeiro = False

        n_revs = len(relatos_pasta) - 1

        return Caso(nome,
                    n_revs,
                    relatos_pasta,
                    cmo_subsis,
                    earm_subsis,
                    earm_sin,
                    gt_subsis,
                    gt_sin,
                    ghid_subsis,
                    ghid_sin,
                    def_subsis)
