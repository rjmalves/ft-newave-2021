from parpa.base.modelo import Modelo
import numpy as np
from typing import List

np.random.seed(42)

class PAR(Modelo):
    """
    """
    def __init__(self,
                 coefs: List[List[float]]):
        super().__init__()
        self.periodos = len(coefs)
        self.coefs = coefs

    def simula(self,
               amostras: int,
               valor_inicial: float = 0.0) -> List[float]:
        # Determina a maior ordem
        max_ordem = 0
        for p in range(self.periodos):
            max_ordem = max([max_ordem, len(self.coefs[p])])
        # Gera as saídas iniciais
        saida = [valor_inicial] * max_ordem
        n_iniciais = len(saida)
        for a in range(n_iniciais, amostras):
            # Determina o período a ser utilizado
            p = a % self.periodos
            # Aplica o modelo do período
            s = 0
            for i, coef in enumerate(self.coefs[p]):
                s += coef * saida[-(i+1)]
            s += np.random.randn()
            saida.append(s)
        return np.array(saida)
