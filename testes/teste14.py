# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 14
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

from inewave.newave.pmo import PMO
from inewave.newave.parp import PARp
from inewave.config import REES
from typing import Dict
import numpy as np
from parpa.yulewalker import YuleWalkerPARA


# Variáveis auxiliares no processo
diretorio_parpa = "/home/rogerio"

# Lê o arquivo pmo.dat
pmo = PMO.le_arquivo(diretorio_parpa)

# Lê o arquivo parp.dat
parp = PARp.le_arquivo(diretorio_parpa)

# Realiza a verificação de igualdade para todas as
# configurações de todas as REEs.

# Variáveis auxiliares para armazenar valores
IDS_REES = range(1, len(REES) + 1)
# Máxima diferença absoluta por REE
max_dif_ree: Dict[int, float] = {ree: -1e4
                                 for ree in IDS_REES}
ano_max_dif_ree: Dict[int, int] = {ree: 0
                                   for ree in IDS_REES}
periodo_max_dif_ree: Dict[int, int] = {ree: 0
                                       for ree in IDS_REES}
ordem_max_dif_ree: Dict[int, int] = {ree: 0
                                     for ree in IDS_REES}
coef_o_max_dif_ree: Dict[int, float] = {ree: 0
                                        for ree in IDS_REES}
coef_e_max_dif_ree: Dict[int, float] = {ree: 0
                                        for ree in IDS_REES}
# Máxima diferença percentual por REE
max_dif_percent_ree: Dict[int, float] = {ree: -1e4
                                         for ree in IDS_REES}
ano_max_dif_perc_ree: Dict[int, int] = {ree: 0
                                        for ree in IDS_REES}
periodo_max_dif_perc_ree: Dict[int, int] = {ree: 0
                                            for ree in IDS_REES}
ordem_max_dif_perc_ree: Dict[int, int] = {ree: 0
                                          for ree in IDS_REES}
coef_o_max_dif_perc_ree: Dict[int, float] = {ree: 0
                                             for ree in IDS_REES}
coef_e_max_dif_perc_ree: Dict[int, float] = {ree: 0
                                             for ree in IDS_REES}


# Faz a estimação para todas as configurações, no período de estudo
for ree in IDS_REES:
    print(f"Estimando para REE {ree} - {REES[ree - 1]}")
    series_energia = {c + 1: parp.series_energia_ree(ree, c)
                      for c in range(60)}
    yw = YuleWalkerPARA(series_energia)
    coefs = parp.coeficientes_ree(ree)
    mes = 0
    for a, ano in enumerate(parp.anos_estudo):
        ordens_finais = parp.ordens_finais_ree(ree)[a, :]
        # Gera a tabela das configurações do ano anterior e do atual
        cfgs = pmo.configuracoes_entrada_reservatorio
        if a == 0:
            c_atual = cfgs[a, 1:]
            c_ant = list(np.ones_like(c_atual, dtype=np.int64))
            configs = np.array([c_ant, c_atual])
        else:
            c_ant = cfgs[a - 1, 1:]
            c_atual = cfgs[a, 1:]
            configs = np.array([c_ant, c_atual])
        # Realiza a estimação para o ano
        coefs_estimados = yw.estima_modelo(ordens_finais, configs)
        # Atualiza as variáveis com as máximas diferenças
        for p, coefs_p in enumerate(coefs_estimados):
            for i, c in enumerate(coefs_p):
                dif = abs(c - coefs[mes][i])
                dif_percentual = abs(100 * abs(c - coefs[mes][i])
                                     / coefs[p][i])
                if dif > max_dif_ree[ree]:
                    max_dif_ree[ree] = dif
                    ano_max_dif_ree[ree] = ano
                    periodo_max_dif_ree[ree] = p + 1
                    ordem_max_dif_ree[ree] = i + 1
                    coef_e_max_dif_ree[ree] = c
                    coef_o_max_dif_ree[ree] = coefs[p][i]
                if dif_percentual > max_dif_percent_ree[ree]:
                    max_dif_percent_ree[ree] = dif_percentual
                    ano_max_dif_perc_ree[ree] = ano
                    periodo_max_dif_perc_ree[ree] = p + 1
                    ordem_max_dif_perc_ree[ree] = i + 1
                    coef_e_max_dif_perc_ree[ree] = c
                    coef_o_max_dif_perc_ree[ree] = coefs[p][i]
            mes += 1

print("")
print(" REE | MAX. DIF. ABS. | MES | ORDEM |" +
      "  COEF. OFICIAL | COEF. ESTIMADO")
print("----------------------------------------" +
      "-----------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_max_dif = "{:1.9f}".format(max_dif_ree[ree]).rjust(10)
    str_mes = f"{periodo_max_dif_ree[ree]}".rjust(2)
    str_ordem = f"{ordem_max_dif_ree[ree]}"
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_ree[ree]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_ree[ree]).rjust(12)
    str_linha = f"  {str_ree} |    {str_max_dif} |  {str_mes} | "
    str_linha += f"    {str_ordem} |   {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("-----------------------------------------" +
      "----------------------------")
print("")

print(" REE | MAX. DIF. PERC. | MES | ORDEM |" +
      "  COEF. OFICIAL | COEF. ESTIMADO")
print("------------------------------------------" +
      "----------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_max_dif = "{:2.6f}".format(max_dif_percent_ree[ree]).rjust(10)
    str_mes = f"{periodo_max_dif_perc_ree[ree]}".rjust(2)
    str_ordem = f"{ordem_max_dif_perc_ree[ree]}"
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_perc_ree[ree]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_perc_ree[ree]).rjust(12)
    str_linha = f"  {str_ree} |      {str_max_dif} |  {str_mes} | "
    str_linha += f"    {str_ordem} |   {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("------------------------------------------" +
      "----------------------------")
