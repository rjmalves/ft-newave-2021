# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 14
#
# Processar um caso com a funcionalidade PAR(p)-A habilitada
# e verificar o processo de redução automática da ordem do modelo.

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
#    python testes/teste14.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.pmo import LeituraPMO  # type: ignore
from inewave.newave.parp import LeituraPARp  # type: ignore
from inewave.config import REES  # type: ignore
from typing import Dict
import numpy as np
from parpa.yulewalker import YuleWalkerPAR


# Variáveis auxiliares no processo
diretorio_parp = "/home/rogerio/ONS/validacao_newave2745/pmo_2021_01_sul_50_mlt_parp"

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


# Faz a estimação para as ordens iniciais do modelo PAR(p)-A
for ree in IDS_REES:
    print(f"Reduzindo ordens para REE {ree} - {REES[ree - 1]}")
    series_energia = parp.series_energia_ree(ree)
    yw = YuleWalkerPAR(series_energia)
    contribs = parp.contribuicoes_ree(ree)
    mes = 0
    for a, ano in enumerate(parp.anos_estudo):
        ordens_originais = parp.ordens_originais_ree(ree)[ano]
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
        # Calcula as ordens finais partindo das ordens inciais
        ordens_finais, contribs_estimadas = yw.reducao_ordem(ordens_originais, configs)
        ordens = parp.ordens_finais_ree(ree)[ano]
        # print(f"Ordens originais:        {ordens_originais}")
        # print(f"Ordens finais estimadas: {ordens_finais}")
        # print(f"Ordens finais NEWAVE:    {ordens}")
        # Atualiza as variáveis com as máximas diferenças
        # print(contribs_estimadas)
        for m, o in enumerate(ordens_finais):
            dif = abs(o - ordens[m])
            if dif > max_dif_ree[ree]:
                max_dif_ree[ree] = dif
                if dif > 0:
                    ano_max_dif_ree[ree] = ano
                    periodo_max_dif_ree[ree] = mes + 1
                    coef_e_max_dif_ree[ree] = o
                    coef_o_max_dif_ree[ree] = ordens[m]
            mes += 1

print("")
print(" REE | MAX. DIF. |  ANO  | MES |" +
      "  ORD. OFICIAL | ORD. ESTIMADA")
print("----------------------------------" +
      "-----------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_max_dif = f"{max_dif_ree[ree]}".rjust(8)
    str_mes = f"{periodo_max_dif_ree[ree]}".rjust(2)
    str_ano = f"{ano_max_dif_ree[ree]}".rjust(4)
    str_coef_o = f"{coef_o_max_dif_ree[ree]}".rjust(12)
    str_coef_e = f"{coef_e_max_dif_ree[ree]}".rjust(12)
    str_linha = f"  {str_ree} | {str_max_dif}  |  {str_ano} | "
    str_linha += f" {str_mes} |  {str_coef_o} |  {str_coef_e}"
    print(str_linha)
print("-----------------------------------" +
      "----------------------------")
print("")
