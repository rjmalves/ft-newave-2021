import numpy as np
from scipy.linalg import toeplitz
from typing import List


class YuleWalkerAR:
    """
    """
    def __init__(self,
                 sinal: np.ndarray):
        self.sinal = sinal

    def _autocorr(self) -> np.ndarray:
        acf = np.correlate(self.sinal, self.sinal, 'full')
        meio = acf.size//2
        c0 = acf[meio]
        return acf[meio:] / c0

    def ajusta_modelo(self, ordem: int) -> List[float]:
        acf = self._autocorr()
        # Monta a matriz de YW
        yw = toeplitz(acf[:ordem])
        autocors = acf[1:ordem+1].T
        coefs = np.matmul(np.linalg.inv(yw), autocors)
        return coefs


class YuleWalkerPAR:
    """
    """
    def __init__(self,
                 sinal: np.ndarray,
                 ordens: List[int]):
        n = len(sinal)
        self.ordens = ordens
        self.periodos = len(ordens)
        self.n_amostras = n//self.periodos
        self.sinal = sinal.reshape(n//self.periodos,
                                   self.periodos)
        # Normaliza o sinal por período
        for j in range(self.periodos):
            media = np.mean(self.sinal[:, j])
            desvio = np.std(self.sinal[:, j], ddof=1)
            self.sinal[:, j] = (self.sinal[:, j] - media) / desvio

    def _autocorr(self, p: int) -> np.ndarray:
        # Para cada lag até a ordem máxima dentre as ordens
        # fornecidas, calcula as correlaçoes
        max_ordem = max(self.ordens)
        acf_list: List[float] = []
        for o in range(max_ordem + 1):
            sinal_m = self.sinal[:, p]
            sinal_lag = self.sinal[:, p - o]
            # Se o mês de referência para o cálculo das
            # autocorrelações, com o lag "volta um ano",
            # então descontamos uma amostra de cada.
            if p < o:
                sinal_m = sinal_m[1:self.n_amostras]
                sinal_lag = sinal_lag[:self.n_amostras-1]
            u = np.mean(np.multiply(sinal_m,
                                    sinal_lag))
            acf_list.append(u / (np.std(sinal_m,
                                        ddof=1) *
                                 np.std(sinal_lag,
                                        ddof=1)))
        acf = np.array(acf_list)
        return acf

    def ajusta_modelo(self) -> List[List[float]]:
        acfs = [self._autocorr(p) for p in range(self.periodos)]
        # Para cada período, obtém os coeficientes
        coefs: List[List[float]] = []
        for p in range(self.periodos):
            o = self.ordens[p]
            # Monta a matriz YW
            yw = np.ones((o, o))
            for i in range(o):
                for j in range(o):
                    valor = 1.0
                    m = 0
                    lag = 0
                    if j < i:
                        m = (p - j - 1) % self.periodos
                        lag = i - j
                    elif j > i:
                        m = (p - i - 1) % self.periodos
                        lag = j - i
                    yw[i, j] = acfs[m][lag]
            # Obtém os coeficientes
            autocors = acfs[p][1:o+1].T
            coefs_norm = list(np.matmul(np.linalg.inv(yw), autocors))
            coefs.append(coefs_norm)
        return coefs
