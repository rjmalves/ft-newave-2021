from parpa.par import PAR
from parpa.yulewalker import YuleWalkerPAR, YuleWalkerPARA

from inewave.newave.parp import LeituraPARp
import numpy as np
import matplotlib.pyplot as plt


# Fixa o seed para números aleatórios
np.random.seed(42)

# Teste PAR(p)
dir = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_01_oficial_64proc"
parp = LeituraPARp(dir).le_arquivo()
entrada = np.array(parp.series[1][ :, :, 0][:, 1:])
ordens = parp.ordens[1][0, 1:]
yw = YuleWalkerPAR(entrada)
coefs = yw.estima_modelo(ordens)
print("Yule-Walker Teste | Arquivo parp.dat")
coefs_parp = parp.coeficientes[1][:12, :, 0]
for i, m in enumerate(coefs):
    ordem = len(m)
    print(["{:1.3f} | {:1.3f}"
           .format(m[j], coefs_parp[i][j])
           for j in range(ordem)])

# Simulação PAR(p)

# Normaliza a entrada por coluna, salvando as médias
# e os desvios.
n_amostras, n_periodos = entrada.shape
medias = np.zeros((n_periodos, ))
desvios = np.zeros((n_periodos, ))
for j in range(n_periodos):
    media = np.mean(entrada[:, j])
    medias[j] = media
    desvio = np.std(entrada[:, j], ddof=0)
    desvios[j] = desvio
    entrada[:, j] = (entrada[:, j] - media) / desvio

# Serializa a entrada
entrada = list(entrada.reshape(n_amostras * n_periodos,))[-12:]
# Cria e executa o modelo PAR(p) estimado, fornecendo
# como valores iniciais os últimos 12 meses.
modelo_parp = PAR(coefs)
saida = modelo_parp.simula(60, entrada)

# Denormaliza a saída
for j in range(len(saida)):
    p = j % n_periodos
    saida[j] = desvios[p] * saida[j] + medias[p]

# Gera o gráfico
plt.figure(figsize=(16, 9))
plt.plot(saida)
plt.tight_layout()
plt.savefig("saidas/saida_parp.png")
plt.close()

# Teste PAR(p)-A
dir = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_parpa"
parp = LeituraPARp(dir).le_arquivo()
entrada = parp.series[1][ :, :, 0][:, 1:]
ordens = parp.ordens[1][0, 1:]
yw = YuleWalkerPARA(entrada)
coefs = yw.estima_modelo(ordens)
print("Yule-Walker Teste | Arquivo parp.dat")
coefs_parp = parp.coeficientes[1][:12, :, 0]
for i, m in enumerate(coefs):
    ordem = len(m)
    print(["{:1.3f} | {:1.3f}"
           .format(m[j], coefs_parp[i][j])
           for j in range(ordem)])
