from inewave.config import MESES
import numpy as np  # type: ignore
import time
from copy import deepcopy
from scipy.linalg import toeplitz  # type: ignore
from typing import List, Dict


class YuleWalkerAR:
    """
    Conjunto de métodos para cálculos associados com a
    montagem da matriz de autocorrelações de YW para um
    modelo AR.
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
    Conjunto de métodos para cálculos associados com a
    montagem da matriz de autocovariâncias de YW para um
    modelo PAR(p).
    """
    def __init__(self,
                 series_por_config: Dict[int, np.ndarray]):

        # O atributo ddof é usado para indicar se o desvio padrão
        # calculado é amostral ou populacional (é a quantia
        # subtraída do denoiminador - 'graus de liberdade')
        self.ddof = 0
        self.sinal = deepcopy(series_por_config)
        self.n_amostras, self.periodos = self.sinal[1].shape
        self._atualiza_tabela_configs(np.ones((2 * self.periodos,),
                                              dtype=np.int64))

    def _atualiza_tabela_configs(self, configs: np.ndarray):
        """
        Gera novamente a tabela de sinais após receber uma
        atualização na tabela de configurações.
        """
        self.tabela_configs = np.reshape(configs,
                                         (configs.size,))
        self.sinal_bkp = np.zeros((self.n_amostras,
                                   2 * self.periodos))
        self.sinal_n = np.zeros((self.n_amostras,
                                 2 * self.periodos))
        self.desvios_sinal = np.zeros((2 * self.periodos,))
        # Lê os sinais brutos e monta o horizonte de 24 meses
        # das configurações respectivas
        p = self.periodos
        for i, c in enumerate(self.tabela_configs):
            self.sinal_bkp[:, i] = deepcopy(self.sinal[c][:, i % p])
        # Normaliza o sinal
        for j in range(2 * p):
            med = np.mean(self.sinal_bkp[:, j])
            dsv = np.std(self.sinal_bkp[:, j], ddof=self.ddof)
            self.sinal_n[:, j] = (self.sinal_bkp[:, j] - med) / dsv
            self.desvios_sinal[j] = dsv

    def _autocorr(self, p: int, lag: int) -> float:
        """
        Calcula a autocorrelação para o sinal normalizado, em
        um período `p` e com lag `lag`. A autocorrelação é
        definida em [1] por:

        Gamma(k) = E[(z(t) - E[z(t)]) * (z(t - k) - E[z(t - k)])]

        Rho(k) = Gamma(k) / Gamma(0)

        Para o modelo periódico, convém representar o período de
        cada amostra. Se o total de períodos é P::

        Gamma(p, k) = E[(z(t, p) - E[z(t, p)]) * z(t - k, K) - E[z(t - k, K)])]

        onde K = (p - k) % P.

        Então a autocorrelação é:

        Rho(p, k) = Gamma(p, k) / Gamma(p, 0)

        **Referências**

        [1] K.W. Hipel A.I McLeod. Time Series Modelling of Water Resources
        and Environmental Systems, Volume 45, Cap. 14. 1994.
        """
        sinal_m = deepcopy(self.sinal_n[:, p])
        sinal_lag = deepcopy(self.sinal_n[:, lag])
        # Se o mês de referência para o cálculo das
        # autocorrelações, com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if lag < self.periodos and p >= self.periodos:
            sinal_m = sinal_m[1:]
            sinal_lag = sinal_lag[:-1]
        u = (1.0 / self.n_amostras) * np.sum(np.multiply(sinal_m,
                                                         sinal_lag))
        return u

    def _matriz_extendida(self, p: int, lag: int) -> np.ndarray:
        """
        Retorna a matriz extendida que será usada para montar
        o sistema de equações de Yule-Walker para um período
        `p` e um lag máximo de `lag`.
        """
        ORDEM_MATRIZ = lag + 1
        # Monta a matriz YW
        # print(f"MATRIZ EXTENDIDA p = {p} lag = {lag}")
        mat = np.ones((ORDEM_MATRIZ, ORDEM_MATRIZ))
        for i in range(ORDEM_MATRIZ):
            for j in range(i + 1, ORDEM_MATRIZ):
                m = p - i
                lag = j - i
                col_p = self.periodos + m
                mat[i, j] = self._autocorr(col_p,
                                           col_p - lag)
                mat[j, i] = mat[i, j]
        return mat

    def _resolve_yw(self,
                    mat: np.ndarray,
                    lag: int) -> List[float]:
        """
        Monta e resolve o sistema de equações de Yule-Walker
        a partir de uma matriz extendida, para um certo período
        `p` e um lag `lag`.
        """
        ORDEM_MATRIZ = lag + 1
        ind_submat = list(range(1, ORDEM_MATRIZ))
        rho_grid = np.ix_(ind_submat, [0])
        yw_grid = np.ix_(ind_submat, ind_submat)

        yw = mat[yw_grid]
        rho = mat[rho_grid]
        coefs_norm = list(np.matmul(np.linalg.inv(yw), rho))
        return [c[0] for c in coefs_norm]

    def estima_modelo(self,
                      ordens: List[int],
                      configs: np.ndarray) -> List[List[float]]:
        """
        Realiza a estimação dos coeficientes do modelo PAR(p)
        a partir da resolução do sistema de Yule-Walker.
        """
        self._atualiza_tabela_configs(configs)
        coefs: List[List[float]] = []
        for p in range(self.periodos):
            o = ordens[p]
            mat = self._matriz_extendida(p, o)
            coefs.append(self._resolve_yw(mat, o))

        return coefs

    def facp(self,
             p: int,
             maxlag: int,
             configs: np.ndarray) -> np.ndarray:
        """
        Calcula a função de autocorrelação parcial periódica
        para um período `p`, considerando um máximo de atrasos `maxlag`.
        """
        self._atualiza_tabela_configs(configs)
        acps: List[float] = []
        # A FACP(k) é definida como o último coeficiente do modelo
        # AR de ordem k ajustado via Yule-Walker.
        # Logo, é da forma:
        #
        # Ajuste_YW_ordem1[0], Ajuste_YW_ordem2[1], ...
        for o in range(1, maxlag):
            mat = self._matriz_extendida(p, o)
            acps.append(self._resolve_yw(mat, o)[o - 1])
        return np.array(acps)

    def escolhe_ordem_modelo(self,
                             p: int,
                             max_ordem: int,
                             configs: np.ndarray) -> int:
        """
        """
        interv_conf = 1.96/np.sqrt(self.n_amostras)
        serie_facp = self.facp(p, 11, configs)
        ordem = 1
        for i in range(max_ordem):
            if abs(serie_facp[i]) >= interv_conf:
                ordem = i + 1
        return ordem

    def contribuicoes(self,
                      coefs: List[List[float]]):
        """
        """
        fis: List[List[float]] = []
        n_meses = len(coefs)
        max_lag = 11
        # Para cada mês, calcula os fis
        for p in range(len(coefs)):
            coefs_mes = coefs[p]
            ordem_mes = len(coefs_mes)
            fis_mes: List[float] = []
            desv_mes = self.desvios_sinal[p + 12]
            # Calcula a contribuição da média
            # Para cada coeficiente, calcula a contribuição própria
            for i in range(ordem_mes):
                desv_lag = self.desvios_sinal[p + 12 - (i + 1)]
                fi = coefs_mes[i] * desv_mes / desv_lag
                fis_mes.append(fi)
            # Completa com 0s até ter 12 termos
            fis_mes += [0] * (12 - len(fis_mes))
            fis.append(fis_mes)
        contribs: List[List[float]] = []
        # Para cada mês, compôe as contribuições da maneira recursiva
        for p in range(n_meses):
            matriz_aux = np.zeros((max_lag, n_meses))
            # Atribui a primeira linha da matriz auxiliar com os fis
            for j in range(n_meses):
                matriz_aux[0, j] = fis[p][j]
            contribs_mes = [matriz_aux[0, 0]]
            # Para cada coeficiente, adiciona as contribuições recursivas
            for i in range(1, max_lag):
                aux = (p - i) % n_meses
                for j in range(max_lag):
                    contrib_aux = fis[aux][j]
                    matriz_aux[i, j] = (matriz_aux[i - 1, 0] * contrib_aux
                                        + matriz_aux[i - 1, j + 1])
                contribs_mes.append(matriz_aux[i, 0])
            contribs.append(contribs_mes)
        return contribs

    def verifica_contrib_negativa(self,
                                  ordens: np.ndarray,
                                  contribs: List[List[float]]) -> list:
        """
        """
        contrib_negativa: List[int] = []
        for i, contrib in enumerate(contribs):
            ordem = ordens[i]
            for j in range(ordem):
                if contrib[j] < 0:
                    contrib_negativa.append(i)
        return list(set(contrib_negativa))

    def reducao_ordem(self,
                      ordens_iniciais: np.ndarray,
                      configs: np.ndarray):
        """
        """
        ordens = deepcopy(ordens_iniciais)
        ordens_maximas = deepcopy(ordens_iniciais)
        # Realiza a estimação inicial
        coefs_estimados = self.estima_modelo(ordens, configs)
        # Calcula as contribuições a partir dos desvios
        contribs = self.contribuicoes(coefs_estimados)
        contrib_negativa = self.verifica_contrib_negativa(ordens,
                                                          contribs)
        while True:
            # Se não foi encontrada nenhuma contribuição negativa,
            # então termina o loop.
            if len(contrib_negativa) == 0:
                break
            # Senão, reduz a ordem do mês que teve contribuição negativa
            # em 1 e tenta novamente.
            for mes in contrib_negativa:
                ordens_maximas[mes] -= 1
            # Realiza a escolha da ordem, limitado às ordens máximas
            for p in range(self.periodos):
                ordens[p] = self.escolhe_ordem_modelo(p,
                                                      ordens_maximas[p],
                                                      configs)
            coefs_estimados = self.estima_modelo(ordens, configs)
            contribs = self.contribuicoes(coefs_estimados)
            contrib_negativa = self.verifica_contrib_negativa(ordens,
                                                              contribs)
        return ordens, contribs


class YuleWalkerPARA:
    """
    Conjunto de métodos para cálculos associados com a
    montagem da matriz de autocovariâncias de YW para um
    modelo PAR-A(p).
    """
    def __init__(self,
                 series_por_config: Dict[int, np.ndarray]):

        # O atributo ddof é usado para indicar se o desvio padrão
        # calculado é amostral ou populacional (é a quantia
        # subtraída do denoiminador - 'graus de liberdade')
        self.ddof = 0
        self.sinal = deepcopy(series_por_config)
        self.n_amostras, self.periodos = self.sinal[1].shape
        self._atualiza_tabela_configs(np.ones((2 * self.periodos,),
                                              dtype=np.int64))

    def _atualiza_tabela_configs(self, configs: np.ndarray):
        """
        Gera novamente a tabela de sinais após receber uma
        atualização na tabela de configurações.
        """
        self.tabela_configs = np.reshape(configs,
                                         (configs.size,))
        self.sinal_bkp = np.zeros((self.n_amostras,
                                   2 * self.periodos))
        self.sinal_n = np.zeros((self.n_amostras,
                                 2 * self.periodos))
        self.desvios_sinal = np.zeros((2 * self.periodos,))
        # Lê os sinais brutos e monta o horizonte de 24 meses
        # das configurações respectivas
        p = self.periodos
        for i, c in enumerate(self.tabela_configs):
            self.sinal_bkp[:, i] = deepcopy(self.sinal[c][:, i % p])
        # Gera as médias por período
        self.medias = self._medias_per(deepcopy(self.sinal_bkp))
        self.desvios_medias = np.zeros((self.periodos,))
        # Normaliza o sinal
        for j in range(2 * p):
            med = np.mean(self.sinal_bkp[:, j])
            dsv = np.std(self.sinal_bkp[:, j], ddof=self.ddof)
            self.sinal_n[:, j] = (self.sinal_bkp[:, j] - med) / dsv
            self.desvios_sinal[j] = dsv
        # Normaliza as médias
        self.medias_n = np.zeros_like(self.medias)
        for j in range(p):
            med = np.mean(self.medias[1:, j])
            dsv = np.std(self.medias[1:, j], ddof=self.ddof)
            self.medias_n[1:, j] = (self.medias[1:, j] - med) / dsv
            self.desvios_medias[j] = dsv

    def _medias_per(self,
                    sinal: np.ndarray) -> np.ndarray:
        """
        Calcula a média dos últimos períodos e retorna a matriz
        de médias.

        OBS: Pela forma como é calculada a matriz de médias, a
        entrada `a(i, j)` contém as médias dos 12 períodos anteriores
        a ela, sem considerar a mesma. Ou seja, Um lag `-1` na
        função de covariância segundo o CEPEL significa um lag
        `0` na função de covariância deste código.
        """
        # Coloca todos os dados em sequência para facilitar
        medias = np.zeros((self.n_amostras, self.periodos))
        for i in range(1, self.n_amostras):
            for j in range(self.periodos):
                i_sinal = j
                f_sinal = i_sinal + self.periodos
                # Extrai a parcela do ano anterior
                sinal_anterior = sinal[i - 1,
                                       i_sinal:min([f_sinal, 12])]
                # Extrai a parcela do ano atual
                sinal_atual = sinal[i,
                                    min([f_sinal, 12]):f_sinal]
                # Concatena e calcula a média
                medias[i, j] = np.mean(np.concatenate((sinal_anterior,
                                                       sinal_atual)))
        return medias

    def _autocov(self,
                 p: int,
                 lag: int) -> float:
        """
        Calcula a autocovariância para o sinal normalizado, em
        um período `p` e com lag `lag`. A autocovariância é
        definida em [1] por:

        Gamma(k) = E[(z(t) - E[z(t)]) * (z(t - k) - E[z(t - k)])]

        Para o modelo periódico, convém representar o período de
        cada amostra. Se o total de períodos é P::

        Gamma(p, k) = E[(z(t, p) - E[z(t, p)]) * z(t - k, K) - E[z(t - k, K)])]

        onde K = (p - k) % P.

        **Referências**

        [1] K.W. Hipel A.I McLeod. Time Series Modelling of Water Resources
        and Environmental Systems, Volume 45, Cap. 14. 1994.

        """
        sinal_m = deepcopy(self.sinal_n[:, p])
        sinal_lag = deepcopy(self.sinal_n[:, lag])
        # Se o mês de referência para o cálculo das
        # autocorrelações, com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if lag < self.periodos and p >= self.periodos:
            sinal_m = sinal_m[1:]
            sinal_lag = sinal_lag[:-1]
        u = (1.0 / self.n_amostras) * np.sum(np.multiply(sinal_m,
                                                         sinal_lag))
        return u

    def _cov_media(self,
                   p: int,
                   lag: int) -> float:
        """
        Realiza o cálculo da covariância entre o sinal defasado no
        tempo com a componente da média anual.

        OBS: Pela forma como é calculada a matriz de médias anuais,
        a variável `A(t - 1)`, como no relatório do CEPEL, que da
        origem ao termo `RHO(m - 1)` está associada a um lag `m`
        nesta função.

        Segue o mesmo princípio da autocovariância, porém realizando
        o produto dos dois sinais em questão ao invés do mesmo sinal
        com lag.
        """
        sinal_med = deepcopy(self.medias_n[:, p % self.periodos])
        sinal_lag = deepcopy(self.sinal_n[:, lag])
        # Se o mês de referência para o cálculo das
        # autocorrelações com o lag "volta um ano",
        # então descontamos uma amostra de cada.
        if lag < self.periodos:
            sinal_med = sinal_med[1:]
            sinal_lag = sinal_lag[:-1]
        u = (1.0 / self.n_amostras) * np.sum(np.multiply(sinal_med,
                                                         sinal_lag))
        return u

    def _matriz_extendida(self, p: int, lag: int) -> np.ndarray:
        """
        Retorna a matriz extendida que será usada para montar
        o sistema de equações de Yule-Walker para um período
        `p` e um lag máximo de `lag`.
        """
        ORDEM_MATRIZ = lag + 2
        # Monta a matriz YW
        # print(f"MATRIZ EXTENDIDA p = {p} lag = {lag}")
        mat = np.ones((ORDEM_MATRIZ, ORDEM_MATRIZ))
        for i in range(ORDEM_MATRIZ - 1):
            for j in range(i + 1, ORDEM_MATRIZ - 1):
                m = p - i
                lag = j - i
                col_p = self.periodos + m
                mat[i, j] = self._autocov(col_p,
                                          col_p - lag)
                mat[j, i] = mat[i, j]
        # Obtém os coeficientes
        # Adiciona os termos da média do período
        for i in range(ORDEM_MATRIZ - 1):
            col_p = self.periodos + p
            mat[ORDEM_MATRIZ - 1, i] = self._cov_media(col_p,
                                                       col_p - i)
            mat[i, ORDEM_MATRIZ - 1] = mat[ORDEM_MATRIZ - 1, i]

        return mat

    def _resolve_yw(self,
                    mat: np.ndarray,
                    lag: int) -> List[float]:
        """
        Monta e resolve o sistema de equações de Yule-Walker
        a partir de uma matriz extendida, para um certo período
        `p` e um lag `lag`.
        """
        ORDEM_MATRIZ = lag + 2
        ind_submat = list(range(1, ORDEM_MATRIZ))
        rho_grid = np.ix_(ind_submat, [0])
        yw_grid = np.ix_(ind_submat, ind_submat)

        yw = mat[yw_grid]
        rho = mat[rho_grid]
        coefs_norm = list(np.matmul(np.linalg.inv(yw), rho))
        return [c[0] for c in coefs_norm]

    def estima_modelo(self,
                      ordens: List[int],
                      configs: np.ndarray) -> List[List[float]]:
        """
        Realiza a estimação do modelo `PAR-A(p1, p2, ..., pm)`
        resolvendo o sistema de equações de Yule-Walker para a
        lista de ordens `[p1, p2, ..., pm]` fornecidas.
        """
        self._atualiza_tabela_configs(configs)
        coefs: List[List[float]] = []
        for p in range(self.periodos):
            o = ordens[p]
            mat = self._matriz_extendida(p, o)
            coefs.append(self._resolve_yw(mat, o))

        return coefs

    def facp(self,
             p: int,
             maxlag: int,
             configs: np.ndarray) -> np.ndarray:
        """
        Determina a Função de Autocorrelação Parcial (FACP)
        através do método das correlações condicionadas para
        um período `p` e lags de 1 a `maxlag`.

        O método consiste em dividir a matriz de covariâncias
        em quatro submatrizes:

        SIGMA = [[SIG11, SIG12],
                 [SIG21, SIG22]]
        onde SIG11 e SIG22 são quadradas e SIG12^T = SIG21.

        SIG11 é a matriz de covariância entre `z(t)` e `z(t - k)`

        SIG22 é a matriz de covariâncias de `[z(t - 1), ... z(t - k + 1), m]`,
        onde `m` é a média anual do período anterior.

        SIG12 é a matriz de covariâncias entre `[z(t), z(t - k)]` e
        `[z(t - 1), ... z(t - k + 1), m]`.

        A matriz de covariância condicionada é dada por:

        COND = SIG11 - SIG12 * SIG22^(-1) * SIG21

        A FACP é obtida na entrada [0, 1] ou [1, 0] de COND.
        """
        self._atualiza_tabela_configs(configs)
        # Para cada período, obtém os coeficientes
        acps: List[float] = []
        mat = self._matriz_extendida(p, maxlag)
        # Calcula as correlações condicionais
        for o in range(1, maxlag):
            ind11 = [0, o]
            ind22 = [[maxlag + 1] if maxlag == 1 else
                     list(range(1, o)) + [maxlag + 1]][0]

            if np.array_equal(ind22,
                              np.zeros_like(ind22)):
                phi = mat[0, o + 1] / (np.sqrt(mat[0, 0] *
                                       mat[o + 1, o + 1]))
                acps.append(phi)
                continue

            ix11_grid = np.ix_(ind11, ind11)
            ix12_grid = np.ix_(ind11, ind22)
            ix22_grid = np.ix_(ind22, ind22)
            sig11 = mat[ix11_grid]
            sig12 = mat[ix12_grid]
            sig22 = mat[ix22_grid]

            cond = sig11 - np.matmul(np.matmul(sig12,
                                               np.linalg.inv(sig22)),
                                     sig12.T)

            phi = cond[0, 1] / (np.sqrt(cond[0, 0] * cond[1, 1]))
            acps.append(phi)

        return np.array(acps)

    def corr_cruzada_media(self,
                           p: int,
                           maxlag: int,
                           configs: np.ndarray) -> List[float]:
        """
        """
        self._atualiza_tabela_configs(configs)
        # Para cada período, obtém os coeficientes
        ccruz: List[float] = []
        # Calcula as correlações cruzadas
        for o in range(0, maxlag):
            col_p = self.periodos + p
            ccruz.append(self._cov_media(col_p,
                                         col_p - o))
        return ccruz

    def escolhe_ordem_modelo(self,
                             p: int,
                             max_ordem: int,
                             configs: np.ndarray) -> int:
        """
        """
        interv_conf = 1.96/np.sqrt(self.n_amostras)
        serie_facp = self.facp(p, 11, configs)
        ordem = 1
        for i in range(max_ordem):
            if abs(serie_facp[i]) >= interv_conf:
                ordem = i + 1
        return ordem

    def contribuicoes(self,
                      coefs: List[List[float]],
                      ordens: List[int]):
        """
        """
        fis: List[List[float]] = []
        psis: List[float] = []
        n_meses = len(coefs)
        max_lag = 11
        # Para cada mês, calcula os fis
        # de cada coeficiente e o psi
        for p in range(len(coefs)):
            coefs_mes = coefs[p]
            ordem_mes = len(coefs_mes) - 1
            fis_mes: List[float] = []
            desv_mes = self.desvios_sinal[p + 12]
            # Calcula a contribuição da média
            desv_media = self.desvios_medias[p]
            contrib_media = coefs_mes[-1] * desv_mes / desv_media
            psis.append(contrib_media)
            # Para cada coeficiente, calcula a contribuição própria
            for i in range(ordem_mes):
                desv_lag = self.desvios_sinal[p + 12 - (i + 1)]
                contrib = coefs_mes[i] * desv_mes / desv_lag
                fis_mes.append(contrib)
            # Completa com 0s até ter 12 termos
            fis_mes += [0] * (12 - len(fis_mes))
            fis.append(fis_mes)

        # for m in range(len(fis)):
        #     print(f"Mês {MESES[m]} - Fis = {fis[m][:ordens[m]]} - Psi = {psis[m]}")
        contribs: List[List[float]] = []
        # Para cada mês, compôe as contribuições da maneira recursiva
        for p in range(n_meses):
            matriz_aux = np.zeros((max_lag, n_meses))
            # Atribui a primeira linha da matriz auxiliar com os fis,
            # já somados com as contribuições das suas médias
            for j in range(max_lag):
                matriz_aux[0, j] = fis[p][j] + psis[p] / 12
            contribs_mes = [matriz_aux[0, 0]]
            # Para cada coeficiente, adiciona as contribuições recursivas
            # if p == 5:
            #     print(f"Matriz AUX para o mês {MESES[p]}")
            for i in range(1, max_lag):
                aux = (p - i) % n_meses
                for j in range(max_lag):
                    # Na verdade, era primeiro multiplicado matriz_aux
                    # por fi, chamado de tmp,
                    # e o valor acumulado era tmp * (1 + psi/12).

                    # Backup do código:
                    # tmp = matriz_aux[i - 1, 0] * (fis[aux][j] + psis[aux] / 12)
                    # matriz_aux[i, j] = (tmp
                    #                     + tmp * psis[aux] / 12
                    #                     + matriz_aux[i - 1, j + 1])
                    contrib_aux = fis[aux][j] + psis[aux] / 12
                    matriz_aux[i, j] = (matriz_aux[i - 1, 0] * contrib_aux
                                        + matriz_aux[i - 1, j + 1])
            # if p == 5:
            #     print(matriz_aux[:, :7])
            #     time.sleep(0.5)
                contribs_mes.append(matriz_aux[i, 0])
            contribs.append(contribs_mes)
        return contribs

    def verifica_contrib_negativa(self,
                                  ordens: np.ndarray,
                                  contribs: List[List[float]]) -> list:
        """
        """
        contrib_negativa: List[int] = []
        for i, contrib in enumerate(contribs):
            ordem = ordens[i]
            for j in range(ordem):
                if contrib[j] < 0:
                    contrib_negativa.append(i)
        return list(set(contrib_negativa))

    def reducao_ordem(self,
                      ordens_iniciais: np.ndarray,
                      configs: np.ndarray):
        """
        """
        ordens = deepcopy(ordens_iniciais)
        ordens_maximas = deepcopy(ordens_iniciais)
        # Realiza a estimação inicial
        coefs_estimados = self.estima_modelo(ordens, configs)
        # Calcula as contribuições a partir dos desvios
        contribs = self.contribuicoes(coefs_estimados, ordens)
        # for p in range(self.periodos):
        #         print(f"Mês {MESES[p]} - Ordem: {ordens[p]}")
        #         print(f"    Contribs: {contribs[p][:ordens[p]]}")
        # print("-----------------------------------------------")
        contrib_negativa = self.verifica_contrib_negativa(ordens,
                                                          contribs)
        while True:
            # Se não foi encontrada nenhuma contribuição negativa,
            # então termina o loop.
            if len(contrib_negativa) == 0:
                break
            # Senão, reduz a ordem do mês que teve contribuição negativa
            # em 1 e tenta novamente.
            for mes in contrib_negativa:
                ordens_maximas[mes] -= 1
            # Realiza a escolha da ordem, limitado às ordens máximas
            for p in range(self.periodos):
                ordens[p] = self.escolhe_ordem_modelo(p,
                                                      ordens_maximas[p],
                                                      configs)
            coefs_estimados = self.estima_modelo(ordens, configs)
            contribs = self.contribuicoes(coefs_estimados, ordens)
            # for p in range(self.periodos):
            #     print(f"Mês {MESES[p]} - Ordem: {ordens[p]}")
            #     print(f"    Contribs: {contribs[p][:ordens[p]]}")
            # print("-----------------------------------------------")
            contrib_negativa = self.verifica_contrib_negativa(ordens,
                                                              contribs)
        return ordens, contribs, coefs_estimados
