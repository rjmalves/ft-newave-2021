import numpy as np
from copy import deepcopy
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
        self.ordens = ordens
        self.sinal = deepcopy(sinal)
        self.n_amostras, self.periodos = self.sinal.shape
        self.ddof = 0
        # Normaliza o sinal por período
        for j in range(self.periodos):
            media = np.mean(self.sinal[:, j])
            desvio = np.std(self.sinal[:, j], ddof=self.ddof)
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
                sinal_m = sinal_m[1:len(sinal_m)]
                sinal_lag = sinal_lag[:len(sinal_lag)-1]
            u = np.mean(np.multiply(sinal_m,
                                    sinal_lag))
            acf_list.append(u / (np.std(sinal_m,
                                        ddof=self.ddof) *
                                 np.std(sinal_lag,
                                        ddof=self.ddof)))
        acf = np.array(acf_list)
        print(f"p = {p} acf = {acf}")
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


class YuleWalkerPARA:
    """
    """
    def __init__(self,
                 sinal: np.ndarray,
                 ordens: List[int]):
        n = len(sinal)
        self.ordens = ordens
        self.sinal = deepcopy(sinal)
        self.n_amostras, self.periodos = self.sinal.shape
        self.medias = self._medias_per(sinal)
        self.ddof = 0
        print(self.sinal)
        # Normaliza o sinal por período
        for j in range(self.periodos):
            media = np.mean(self.sinal[:, j])
            desvio = np.std(self.sinal[:, j], ddof=self.ddof)
            self.sinal[:, j] = (self.sinal[:, j] - media) / desvio
        # Normaliza as médias por período
        for j in range(self.periodos):
            media = np.mean(self.medias[:, j])
            desvio = np.std(self.medias[:, j], ddof=self.ddof)
            self.medias[:, j] = (self.medias[:, j] - media) / desvio

    def _medias_per(self , sinal: np.ndarray):
        """
        Calcula a média dos últimos períodos e retorna a matriz
        de médias.
        """
        # Coloca todos os dados em sequência para facilitar
        sinal_seq = np.array(sinal.reshape(sinal.size,))
        medias = np.zeros((self.n_amostras, self.periodos))
        for i in range(1, self.n_amostras):
            for j in range(self.periodos):
                i_sinal = (i - 1) * self.periodos + j
                f_sinal = i_sinal + self.periodos
                medias[i, j] = np.mean(sinal_seq[i_sinal:f_sinal])
        return medias


    def _autocorr(self, p: int) -> np.ndarray:
        # Para cada lag até a ordem máxima dentre as ordens
        # fornecidas, calcula as correlaçoes
        max_ordem = max(self.ordens)
        acf_list: List[float] = []
        for o in range(max_ordem + 1):
            sinal_m = self.sinal[:, p]
            sinal_lag = self.sinal[:, p - o]
            # Se o mês de referência para o cálculo das
            # autocorrelações com o lag "volta um ano",
            # então descontamos uma amostra de cada.
            if p < o:
                sinal_m = sinal_m[1:self.n_amostras]
                sinal_lag = sinal_lag[:self.n_amostras-1]
            u = np.mean(np.multiply(sinal_m,
                                    sinal_lag))
            acf_list.append(u / (np.std(sinal_m,
                                        ddof=self.ddof) *
                                 np.std(sinal_lag,
                                        ddof=self.ddof)))
        acf = np.array(acf_list)
        return acf

    def _autocorr_media(self, p: int) -> np.ndarray:
        # Para cada lag até a ordem máxima dentre as ordens
        # fornecidas, calcula as correlaçoes
        max_ordem = max(self.ordens)
        acf_list: List[float] = []
        for o in range(max_ordem):
            sinal_med = self.medias[:, p]
            sinal_lag = self.sinal[:, p - o]
            # Se o mês de referência para o cálculo das
            # autocorrelações com o lag "volta um ano",
            # então descontamos uma amostra de cada.
            if p < o:
                sinal_med = sinal_med[1:self.n_amostras]
                sinal_lag = sinal_lag[:self.n_amostras-1]
            u = np.mean(np.multiply(sinal_med,
                                    sinal_lag))
            acf_list.append(u / (np.std(sinal_med,
                                        ddof=self.ddof) *
                                 np.std(sinal_lag,
                                        ddof=self.ddof)))
        acf = np.array(acf_list)
        return acf

    def ajusta_modelo(self) -> List[List[float]]:
        acfs = [self._autocorr(p) for p in range(self.periodos)]
        # Para cada período, obtém os coeficientes
        coefs: List[List[float]] = []
        for p in range(self.periodos):
            o = self.ordens[p]
            # Monta a matriz YW
            yw = np.ones((o + 1, o + 1))
            for i in range(o):
                for j in range(o):
                    m = 0
                    lag = 0
                    if j < i:
                        m = (p - j - 1) % self.periodos
                        lag = i - j
                    elif j > i:
                        m = (p - i - 1) % self.periodos
                        lag = j - i
                    yw[i, j] = acfs[m][lag]
            # Adiciona os termos da média do período
            medias = self._autocorr_media(p - 1)
            for i in range(o):
                yw[o, i] = medias[i]
                yw[i, o] = medias[i]
            # Obtém os coeficientes
            autocors = np.concatenate([acfs[p][1:o+1],
                                      np.array([medias[1]])]).T
            coefs_norm = list(np.matmul(np.linalg.inv(yw), autocors))
            coefs.append(coefs_norm)
        return coefs