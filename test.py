from parpa.yulewalker import YuleWalkerPAR, YuleWalkerPARA

from inewave.newave.parp import LeituraPARp

# Lê os dados no parp.dat
dir = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_01_oficial_64proc"
parp = LeituraPARp(dir).le_arquivo()
entrada = parp.series[1][ :, :, 0][:, 1:]
ordens = parp.ordens[1][0, 1:]
yw = YuleWalkerPAR(entrada, ordens)
coefs = yw.ajusta_modelo()
print("Yule-Walker Teste | Arquivo parp.dat")
coefs_parp = parp.coeficientes[1][:12, :, 0]
for i, m in enumerate(coefs):
    ordem = len(m)
    print(["{:1.3f} | {:1.3f}"
           .format(m[j], coefs_parp[i][j])
           for j in range(ordem)])


# Teste PAR(p)-A
ywa = YuleWalkerPARA(entrada, ordens)
coefsa = ywa.ajusta_modelo()
print("Yule-Walker-A Teste | Arquivo parp.dat")
coefs_parp = parp.coeficientes[1][:12, :, 0]
for i, m in enumerate(coefsa):
    ordem = len(m)
    print(["{:1.3f} | {:1.3f}"
           .format(m[j], coefs_parp[i][min([j, 5])])
           for j in range(ordem)])
