# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 16
#
# Processar um caso com a funcionalidade PAR(p)-A habilitada
# e verificar a estimação dos parâmetros ajustados do modelo
# através das equações de Yule-Walker estendidas.

# INSTRUÇÕES PARA USO DO SCRIPT DE TESTE
#
# 1- Substituir nas variáveis auxiliares os diretórios onde
#    estão as saídas das execuções do NEWAVE.
#
# 2- Criar um ambiente virtual com o comando:
#    python -m venv ./venv
#
# 3- Ativar o ambiente virtual com um dos comandos:
#    LINUX: source venv/bin/activate
#    WINDOWS: ./venv/Scripts/activate
#
# 4- Instalar os módulos necessários com o comando:
#    python -m pip install -r requirements.txt
#
# 5- Executar no terminal o script desejado. Por ex:
#    python testes/teste16.py
#
# 6- Observar a saída exibida no terminal

from inewave.newave.parp import LeituraPARp
from parpa.yulewalker import YuleWalkerPARA


# Variáveis auxiliares no processo
diretorio_parpa = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_parpa"

# Lê o arquivo parp.dat
parp = LeituraPARp(diretorio_parpa).le_arquivo()

# Realiza a estimação dos coeficientes do modelo
# para a Configuração 1 do SUDESTE, nas ordens
# finais dadas pelo NEWAVE.
entrada = parp.series_energia_ree(1)[1]
coefs = parp.coeficientes_ree(1)
ordens = parp.ordens_finais_ree(1)[2020]
yw = YuleWalkerPARA(entrada)
coefs_estimados = yw.estima_modelo(ordens)

# Exibe a comparação dos coeficientes no terminal,
# com o mesmo número de casas decimais do parp.dat.
print(" parp.dat | Estimado ")
print("--------------------")
for i, m in enumerate(coefs_estimados):
    ordem = len(m)
    mes = f"{i + 1}".rjust(2)
    print(f"   Mês {mes} - Ordem {ordem}")
    print("--------------------")
    for j in range(ordem):
        estimado = "{:1.3f}".format(m[j]).rjust(9)
        oficial = "{:1.3f}".format(coefs[i][j]).rjust(9)
        print(f"{oficial} |{estimado} ")
    print("--------------------")

# # Realiza a verificação de igualdade para todas as
# # configurações de todas as REEs.
# entrada = parp.series[1][ :, :, 0][:, 1:]
# coefs = parp.coeficientes[1][:12, :, 0]
# ordens = parp.ordens[1][0, 1:]
# yw = YuleWalkerPARA(entrada)
# coefs_estimados = yw.estima_modelo(ordens)
