from abc import ABC, abstractmethod

class Modelo(ABC):
    """
    Classe base para qualquer modelo ARIMA ou PAR.
    """

    def __init__(self):
        pass

    @abstractmethod
    def simula(amostras: int):
        pass
