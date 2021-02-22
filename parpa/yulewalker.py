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
        # O atributo ddof é usado para indicar se o desvio padrão
        # calculado é amostral ou populacional (é a quantia
        # subtraída do denoiminador - 'graus de liberdade')
        self.ddof = 0
        # Normaliza o sinal por período
        for j in range(self.periodos):
            media = np.mean(self.sinal[:, j])
            desvio = np.std(self.sinal[:, j], ddof=self.ddof)
            self.sinal[:, j] = (self.sinal[:, j] - media) / desvio

    def _autocorr(self, p: int, lag: int) -> float:
        sinal_m = self.sinal[:, p]
        sinal_lag = self.sinal[:, p - lag]
        # Se o mês de referência para o cálculo das
        # autocorrelações, com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if p < lag:
            sinal_m = sinal_m[1:len(sinal_m)]
            sinal_lag = sinal_lag[:len(sinal_lag)-1]
        u = np.mean(np.multiply(sinal_m,
                                sinal_lag))
        ac = (u / (np.std(sinal_m,
                          ddof=self.ddof) *
                   np.std(sinal_lag,
                          ddof=self.ddof)))
        return ac

    def estima_modelo(self) -> List[List[float]]:
        """
        Realiza a estimação dos coeficientes do modelo PAR(p)
        a partir da resolução do sistema de Yule-Walker.
        """
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
                    yw[i, j] = self._autocorr(m, lag)
            # Obtém os coeficientes
            autocors = np.array([self._autocorr(p, lag)
                                 for lag in range(1, o + 1)]).T
            coefs_norm = list(np.matmul(np.linalg.inv(yw), autocors))
            coefs.append(coefs_norm)
        return coefs

    def facp(self,
             p: int,
             maxlag: int) -> np.ndarray:
        """
        Calcula a função de autocorrelação parcial periódica
        para um período `p`, considerando um máximo de atrasos `maxlag`.
        """
        # Monta a matriz YW
        yw = np.ones((maxlag, maxlag))
        for i in range(maxlag):
            for j in range(maxlag):
                m = 0
                lag = 0
                if j < i:
                    m = (p - j - 1) % self.periodos
                    lag = i - j
                elif j > i:
                    m = (p - i - 1) % self.periodos
                    lag = j - i
                yw[i, j] = self._autocorr(m, lag)
        # Obtém os coeficientes
        autocors = np.array([self._autocorr(p, lag)
                             for lag in range(1, maxlag + 1)]).T
        acps: List[float] = []
        # A FACP(k) é definida como o último coeficiente do modelo
        # AR de ordem k ajustado via Yule-Walker.
        # Logo, é da forma:
        #
        # Ajuste_YW_ordem1[0], Ajuste_YW_ordem2[1], ...
        for o in range(1, maxlag):
            acp = list(np.matmul(np.linalg.inv(yw[:o, :o]),
                                 autocors[:o]))[o - 1]
            acps.append(acp)
        return np.array(acps)


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
        # O atributo ddof é usado para indicar se o desvio padrão
        # calculado é amostral ou populacional (é a quantia
        # subtraída do denoiminador - 'graus de liberdade')
        self.ddof = 0
        # Normaliza o sinal por período
        for j in range(self.periodos):
            media = np.mean(self.sinal[:, j])
            desvio = np.std(self.sinal[:, j], ddof=self.ddof)
            self.sinal[:, j] = (self.sinal[:, j] - media) / desvio
        # Normaliza as médias por período
        for j in range(self.periodos):
            media = np.mean(self.medias[1:, j])
            desvio = np.std(self.medias[1:, j], ddof=self.ddof)
            self.medias[:, j] = (self.medias[:, j] - media) / desvio

    def _medias_per(self , sinal: np.ndarray):
        """
        Calcula a média dos últimos períodos e retorna a matriz
        de médias.
        """
        # Coloca todos os dados em sequência para facilitar
        sinal_seq = np.array(sinal.reshape(sinal.size,))
        medias = np.zeros((self.n_amostras, self.periodos))
        for i in range(1, 88):
            for j in range(12):
                i_sinal = (i - 1) * 12 + j
                f_sinal = i_sinal + 12
                medias[i, j] = np.mean(sinal_seq[i_sinal:f_sinal])
        return medias

    def _autocorr(self, p: int, lag: int) -> float:
        sinal_m = self.sinal[:, p]
        sinal_lag = self.sinal[:, p - lag]
        # Se o mês de referência para o cálculo das
        # autocorrelações, com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if p < lag:
            sinal_m = sinal_m[1:len(sinal_m)]
            sinal_lag = sinal_lag[:len(sinal_lag)-1]
        u = np.mean(np.multiply(sinal_m,
                                sinal_lag))
        ac = (u / (np.std(sinal_m,
                          ddof=self.ddof) *
                   np.std(sinal_lag,
                          ddof=self.ddof)))
        return ac

    def _autocorr_media(self, p: int, lag: int) -> np.ndarray:
        lag_mod = lag % self.periodos
        sinal_med = self.medias[:, p]
        sinal_lag = self.sinal[:, lag_mod]
        print(f"AUTOCOR MEDIA: p = {p}, lag = {lag}, col = {lag_mod}")
        # Se o mês de referência para o cálculo das
        # autocorrelações com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if p < lag_mod:
            sinal_med = sinal_med[1:self.n_amostras]
            sinal_lag = sinal_lag[:self.n_amostras-1]

        u = np.mean(np.multiply(sinal_med,
                                sinal_lag))
        ac = (u / (np.std(sinal_med,
                          ddof=self.ddof) *
                   np.std(sinal_lag,
                          ddof=self.ddof)))
        return ac

    def estima_modelo(self) -> List[List[float]]:
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
                    yw[i, j] = self._autocorr(m, lag)
            # Obtém os coeficientes
            # Adiciona os termos da média do período
            for i in range(o):
                yw[o, i] = self._autocorr_media(p - 1, i)
                yw[i, o] = yw[o, i]
            # Obtém os coeficientes
            media_futura = self._autocorr_media(p - 1, -1)
            autocors = np.concatenate([[self._autocorr(p, lag)
                                        for lag in range(1, o + 1)],
                                      np.array([media_futura])]).T
            coefs_norm = list(np.matmul(np.linalg.inv(yw), autocors))
            coefs.append(coefs_norm)
        return coefs

    def facp(self, p: int, maxlag: int) -> List[float]:
        # Para cada período, obtém os coeficientes
        coefs: List[List[float]] = []
        # Monta a matriz YW
        yw = np.ones((maxlag + 1, maxlag + 1))
        for i in range(maxlag):
            for j in range(maxlag):
                m = 0
                lag = 0
                if j < i:
                    m = (p - j - 1) % self.periodos
                    lag = i - j
                elif j > i:
                    m = (p - i - 1) % self.periodos
                    lag = j - i
                yw[i, j] = self._autocorr(m, lag)
        # Obtém os coeficientes
        # Adiciona os termos da média do período
        for i in range(maxlag):
            yw[maxlag, i] = self._autocorr_media(maxlag - 1, i)
            yw[i, maxlag] = yw[maxlag, i]
        # Obtém os coeficientes
        media_futura = self._autocorr_media(maxlag - 1, -1)
        autocors = np.concatenate([[self._autocorr(p, lag)
                                    for lag in range(1, maxlag + 1)],
                                    np.array([media_futura])]).T
        coefs_norm = list(np.matmul(np.linalg.inv(yw), autocors))
        coefs.append(coefs_norm)
        acps: List[float] = []
        # A FACP(k) é definida como o último coeficiente do modelo
        # AR de ordem k ajustado via Yule-Walker.
        # Logo, é da forma:
        #
        # Ajuste_YW_ordem1[0], Ajuste_YW_ordem2[1], ...
        for o in range(1, maxlag):
            acp = list(np.matmul(np.linalg.inv(yw[:o, :o]),
                                autocors[:o]))[o - 1]
            acps.append(acp)
        return np.array(acps)
