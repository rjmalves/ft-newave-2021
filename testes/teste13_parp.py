# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 13
#
# Processar um caso com a funcionalidade PAR(p)-A habilitada e
# verificar no arquivo PARP.DAT o cálculo das autocorrelações
# parciais através do método de correlações condicionadas.

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
#    python testes/teste13.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.pmo import LeituraPMO  # type: ignore
from inewave.newave.parp import LeituraPARp  # type: ignore
from inewave.config import REES  # type: ignore
from typing import Dict
import numpy as np
from parpa.yulewalker import YuleWalkerPAR  # type: ignore


# Variáveis auxiliares no processo
diretorio_parp = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_oficial"

# Lê o arquivo pmo.dat
pmo = LeituraPMO(diretorio_parp).le_arquivo()

# Lê o arquivo parp.dat
parp = LeituraPARp(diretorio_parp).le_arquivo()

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


# Calcula as autocorrelações parciais e compara com o arquivo
# Calcula a FACP para o período
for ree in IDS_REES:
    print(f"Calculando FACP para REE {ree} - {REES[ree - 1]}")
    series_energia = parp.series_energia_ree(ree)
    yw = YuleWalkerPAR(series_energia)
    serie_facp = parp.correlograma_energia_ree(ree)
    mes = 1
    for a, ano in enumerate(parp.anos_estudo):
        ordens_finais = parp.ordens_finais_ree(ree)[ano]
        # Gera a tabela das configurações do ano anterior e do atual
        cfgs = pmo.configuracoes_entrada_reservatorio
        if a == 0:
            c_atual = cfgs.configs_por_ano[ano]
            c_ant = list(np.ones_like(c_atual, dtype=np.int64))
            configs = np.array([c_ant, c_atual])
        else:
            a_ant = parp.anos_estudo[a - 1]
            c_ant = cfgs.configs_por_ano[a_ant]
            c_atual = cfgs.configs_por_ano[ano]
            configs = np.array([c_ant, c_atual])
        for p in range(0, 12):
            facp = yw.facp(p, 12, configs)
            # Atualiza as variáveis com as máximas diferenças
            for i, c in enumerate(facp):
                oficial = serie_facp[mes][i]
                dif = abs(c - oficial)
                dif_percentual = 100 * abs(c - oficial) / oficial
                if dif > max_dif_ree[ree]:
                    max_dif_ree[ree] = dif
                    max_dif_percent_ree[ree] = dif_percentual
                    ano_max_dif_ree[ree] = ano
                    periodo_max_dif_ree[ree] = mes
                    ordem_max_dif_ree[ree] = i + 1
                    coef_e_max_dif_ree[ree] = c
                    coef_o_max_dif_ree[ree] = oficial
                if dif_percentual > max_dif_percent_ree[ree]:
                    max_dif_percent_ree[ree] = dif_percentual
                    ano_max_dif_perc_ree[ree] = ano
                    periodo_max_dif_perc_ree[ree] = mes
                    ordem_max_dif_perc_ree[ree] = i + 1
                    coef_e_max_dif_perc_ree[ree] = c
                    coef_o_max_dif_perc_ree[ree] = oficial
            mes += 1

print("")
print(" REE | MAX. DIF. ABS. | MES | LAG |" +
      " FACP  OFICIAL | FACP CALCULADA")
print("--------------------------------" +
      "-----------------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_max_dif = "{:1.9f}".format(max_dif_ree[ree]).rjust(10)
    str_mes = f"{periodo_max_dif_ree[ree]}".rjust(2)
    str_lag = f"{ordem_max_dif_ree[ree]}".rjust(2)
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_ree[ree]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_ree[ree]).rjust(12)
    str_linha = f"  {str_ree} |    {str_max_dif} |  {str_mes} | "
    str_linha += f" {str_lag} |  {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("---------------------------------" +
      "----------------------------------")
print("")

print(" REE | MAX. DIF. PERC. | MES | LAG |" +
      " FACP  OFICIAL | FACP CALCULADA")
print("----------------------------------" +
      "----------------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_max_dif = "{:2.6f}".format(max_dif_percent_ree[ree]).rjust(10)
    str_mes = f"{periodo_max_dif_perc_ree[ree]}".rjust(2)
    str_lag = f"{ordem_max_dif_ree[ree]}".rjust(2)
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_perc_ree[ree]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_perc_ree[ree]).rjust(12)
    str_linha = f"  {str_ree} |      {str_max_dif} |  {str_mes} | "
    str_linha += f" {str_lag} |  {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("----------------------------------" +
      "----------------------------------")
