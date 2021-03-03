# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 18
#
# Processar um caso não-condicionado utilizando as metodologias
# PAR(p) e PAR(p)-A e comparar a reprodução das autocorrelações
# anual e mensais.

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
#    python testes/teste18.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.parp import LeituraPARp
from inewave.config import REES
from typing import Dict
import numpy as np
from parpa.correlacoesespaciais import CorrelacoesEspaciais


# Variáveis auxiliares no processo
diretorio_parpa = "/home/rogerio/ONS/validacao_newave2743/pmo_2020_11_oficial"

# Lê o arquivo parp.dat
parp = LeituraPARp(diretorio_parpa).le_arquivo()

n_cfgs = len(parp.series_energia_ree(1).keys())
IDS_REES = range(1, len(REES) + 1)
# Organiza as série por configuração e, em seguida, por REE
series_cfgs: Dict[int, Dict[int, np.ndarray]] = {}
for ree in IDS_REES:
    series_ree = parp.series_energia_ree(ree)
    for cfg, serie in series_ree.items():
        if cfg not in series_cfgs:
            series_cfgs[cfg] = {}
        series_cfgs[cfg][ree] = series_ree[cfg]

cfgs = range(1, n_cfgs + 1)
# Realiza a verificação de igualdade para todas as
# configurações de todas as REEs.

# Variáveis auxiliares

# Variaveis CORR ESP ANUAL
max_dif_cfg_an: Dict[int, float] = {cfg: -1e4
                                    for cfg in cfgs}
ree1_max_dif_cfg_an: Dict[int, int] = {cfg: 0
                                       for cfg in cfgs}
ree2_max_dif_cfg_an: Dict[int, int] = {cfg: 0
                                       for cfg in cfgs}
coef_o_max_dif_cfg_an: Dict[int, int] = {cfg: 0
                                         for cfg in cfgs}
coef_e_max_dif_cfg_an: Dict[int, int] = {cfg: 0
                                         for cfg in cfgs}
# Variaveis CORR ESP MENSAL
max_dif_cfg_me: Dict[int, float] = {cfg: -1e4
                                    for cfg in cfgs}
ree1_max_dif_cfg_me: Dict[int, int] = {cfg: 0
                                       for cfg in cfgs}
ree2_max_dif_cfg_me: Dict[int, int] = {cfg: 0
                                       for cfg in cfgs}
mes_max_dif_cfg_me: Dict[int, int] = {cfg: 0
                                      for cfg in cfgs}
coef_o_max_dif_cfg_me: Dict[int, int] = {cfg: 0
                                         for cfg in cfgs}
coef_e_max_dif_cfg_me: Dict[int, int] = {cfg: 0
                                         for cfg in cfgs}

# Calcula as correlações espaciais e compara com o arquivo
corr_esp_an = parp.correlacoes_espaciais_anuais
corr_esp_me = parp.correlacoes_espaciais_mensais
for cfg in cfgs:
    ce = CorrelacoesEspaciais(series_cfgs[cfg])
    print(f"Calculando CORR ESP para CFG {cfg}")
    for ree1 in IDS_REES:
        for ree2 in range(ree1, len(REES) + 1):
            corr_parp = corr_esp_me[cfg][ree1][ree2]
            corr_estimada = ce.corr_espaciais_mensais(ree1, ree2)
            # Atualiza as variáveis com as máximas diferenças
            # Correlações Espaciais Anuais
            corr_parp_an = corr_esp_an[cfg][ree1][ree2]
            corr_estimada_an = ce.corr_espacial_anual(ree1, ree2)
            dif = abs(corr_estimada_an - corr_parp_an)
            if dif > max_dif_cfg_an[cfg]:
                max_dif_cfg_an[cfg] = dif
                ree1_max_dif_cfg_an[cfg] = ree1-1
                ree2_max_dif_cfg_an[cfg] = ree2-1
                coef_e_max_dif_cfg_an[cfg] = corr_estimada_an
                coef_o_max_dif_cfg_an[cfg] = corr_parp_an
            # Correlações Espaciais Mensais
            for i, c in enumerate(corr_estimada):
                oficial = corr_parp[i]
                dif = abs(c - oficial)
                if dif > max_dif_cfg_me[cfg]:
                    max_dif_cfg_me[cfg] = dif
                    ree1_max_dif_cfg_me[cfg] = ree1-1
                    ree2_max_dif_cfg_me[cfg] = ree2-1
                    mes_max_dif_cfg_me[cfg] = i + 1
                    coef_e_max_dif_cfg_me[cfg] = c
                    coef_o_max_dif_cfg_me[cfg] = oficial


print("")
print("CORRELAÇÕES ESPACIAIS MENSAIS")
print(" CFG | MAX. DIF. ABS. | MES |   REE 1   |" +
      "   REE 2   | CORR. OFICIAL | CORR. CALCULADA")
print("-------------------------------------------" +
      "-------------------------------------------")
for cfg in cfgs:
    str_cfg = f"{cfg}".rjust(2)
    str_max_dif = "{:1.9f}".format(max_dif_cfg_me[cfg]).rjust(10)
    str_ree1 = f"{REES[ree1_max_dif_cfg_me[cfg]]}".rjust(10)
    str_ree2 = f"{REES[ree2_max_dif_cfg_me[cfg]]}".rjust(10)
    str_mes = f"{mes_max_dif_cfg_me[cfg]}".rjust(2)
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_cfg_me[cfg]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_cfg_me[cfg]).rjust(12)
    str_linha = f"  {str_cfg} |    {str_max_dif} |  {str_mes} |{str_ree1} "
    str_linha += f"|{str_ree2} |  {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("-------------------------------------------" +
      "-------------------------------------------")
print("")

print("")
print("CORRELAÇÕES ESPACIAIS ANUAIS")
print(" CFG | MAX. DIF. ABS. |   REE 1   |" +
      "   REE 2   | CORR. OFICIAL | CORR. CALCULADA")
print("----------------------------------------" +
      "----------------------------------------")
for cfg in cfgs:
    str_cfg = f"{cfg}".rjust(2)
    str_max_dif = "{:1.9f}".format(max_dif_cfg_an[cfg]).rjust(10)
    str_ree1 = f"{REES[ree1_max_dif_cfg_an[cfg]]}".rjust(10)
    str_ree2 = f"{REES[ree2_max_dif_cfg_an[cfg]]}".rjust(10)
    str_coef_o = "{:1.6f}".format(coef_o_max_dif_cfg_an[cfg]).rjust(12)
    str_coef_e = "{:1.6f}".format(coef_e_max_dif_cfg_an[cfg]).rjust(12)
    str_linha = f"  {str_cfg} |    {str_max_dif} |{str_ree1} "
    str_linha += f"|{str_ree2} |  {str_coef_o} |   {str_coef_e}"
    print(str_linha)
print("-----------------------------------------" +
      "-----------------------------------------")
print("")