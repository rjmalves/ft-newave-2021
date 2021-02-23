from parpa.base.modelo import Modelo
import numpy as np
from typing import List


class AR(Modelo):
    """
    """
    def __init__(self,
                 coefs: List[float]):
        super().__init__()
        self.coefs = coefs

    def simula(self,
               amostras: int,
               valores_iniciais: List[float] = None) -> List[float]:
        # Gera as saídas iniciais
        if valores_iniciais is None:
            saida = [0.0] * len(self.coefs)
        else:
            saida = valores_iniciais
        n_iniciais = len(saida)
        for _ in range(n_iniciais, amostras):
            s = 0
            for i, coef in enumerate(self.coefs):
                s += coef * saida[-(i+1)]
            s += np.random.randn()
            saida.append(s)
        print(len(saida))
        return saida
