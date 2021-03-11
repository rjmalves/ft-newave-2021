import numpy as np
from copy import deepcopy
from typing import Dict


class CorrelacoesEspaciais:
    """
    Conjunto de métodos para calcular as correlações
    espaciais por configuração, entre REEs, da mesma
    forma feita no parp.dat.
    """
    def __init__(self,
                 series_por_ree: Dict[int, np.ndarray]):
        self.sinal_m = deepcopy(series_por_ree)
        self.n_amostras, self.periodos = self.sinal_m[1].shape
        self.n_entradas = self.n_amostras * self.periodos
        # Calcula a média anual
        self.sinal_a = deepcopy(series_por_ree)
        for r in self.sinal_a.keys():
            medias_anuais = np.zeros((self.n_amostras,))
            for a in range(self.n_amostras):
                medias_anuais[a] = np.mean(self.sinal_a[r][a, :])
            self.sinal_a[r] = medias_anuais
        # O atributo ddof é usado para indicar se o desvio padrão
        # calculado é amostral ou populacional (é a quantia
        # subtraída do denoiminador - 'graus de liberdade')
        self.ddof = 0
        # Normaliza o sinal por período
        for r in self.sinal_m.keys():
            for j in range(self.periodos):
                med = np.mean(self.sinal_m[r][:, j])
                dsv = np.std(self.sinal_m[r][:, j], ddof=self.ddof)
                self.sinal_m[r][:, j] = (self.sinal_m[r][:, j] - med) / dsv
        # Normaliza o sinal em todo o período
        for r in self.sinal_a.keys():
            med = np.mean(self.sinal_a[r])
            dsv = np.std(self.sinal_a[r], ddof=self.ddof)
            self.sinal_a[r] = (self.sinal_a[r] - med) / dsv

    def _corr_espacial_mensal(self,
                              ree1: int,
                              ree2: int,
                              p: int) -> float:
        """
        """
        sinal_ree1 = deepcopy(self.sinal_m[ree1][:, p])
        sinal_ree2 = deepcopy(self.sinal_m[ree2][:, p])
        u = (1.0 / self.n_amostras) * np.sum(np.multiply(sinal_ree1,
                                                         sinal_ree2))
        return u

    def _corr_espacial_anual(self,
                             ree1: int,
                             ree2: int) -> float:
        """
        """
        sinal_ree1 = deepcopy(self.sinal_a[ree1])
        sinal_ree2 = deepcopy(self.sinal_a[ree2])
        u = (1.0 / self.n_amostras) * np.sum(np.multiply(sinal_ree1,
                                                         sinal_ree2))
        return u

    def corr_espaciais_mensais(self,
                               ree1: int,
                               ree2: int) -> np.ndarray:
        """
        """
        corrs = np.zeros((self.periodos, ))
        for p in range(self.periodos):
            corrs[p] = self._corr_espacial_mensal(ree1, ree2, p)
        return corrs

    def corr_espacial_anual(self,
                            ree1: int,
                            ree2: int) -> float:
        """
        """
        c = self._corr_espacial_anual(ree1, ree2)
        return c
