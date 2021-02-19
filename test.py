from parpa.par import PAR
from parpa.yulewalker import YuleWalkerPAR

import matplotlib.pyplot as plt

# Coefs:  PHI1 ... PHIp
m = [0.295, 0.378]
m2 = [0.295, -0.178]
modelo = PAR([m, m2])
ordens = [2, 2]
saida = modelo.simula(1000)
yw = YuleWalkerPAR(saida, ordens)
coefs = yw.ajusta_modelo()
print(f"ajuste PAR = {coefs}")
plt.plot(saida)
plt.savefig("teste.png")

