# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 15
#
# Processar um caso com a funcionalidade PAR(p)-A habilitada
# e verificar a escolha da ordem do modelo.

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
#    python testes/teste15.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.parp import LeituraPARp  # type: ignore
from inewave.config import REES  # type: ignore
from typing import Dict
import numpy as np


# Variáveis auxiliares no processo
diretorio_parpa = ("/home/rogerio/ONS/validacao_newave2743" +
                   "/pmo_2020_11_parpa_sem_redordem")

# Lê o arquivo parp.dat
parp = LeituraPARp(diretorio_parpa).le_arquivo()

# Variáveis auxiliares para armazenar valores
IDS_REES = range(1, len(REES) + 1)
# Número de ordens diferentes por REE
n_dif_ree: Dict[int, float] = {ree: 0
                               for ree in IDS_REES}
ano_n_dif_ree: Dict[int, int] = {ree: 0
                                 for ree in IDS_REES}
periodo_n_dif_ree: Dict[int, int] = {ree: 0
                                     for ree in IDS_REES}
max_sig_n_dif_ree: Dict[int, int] = {ree: 0
                                     for ree in IDS_REES}
ordem_n_dif_ree: Dict[int, int] = {ree: 0
                                   for ree in IDS_REES}
signi_n_dif_ree: Dict[int, int] = {ree: 0
                                   for ree in IDS_REES}

# Lê a FACP do parp.dat e compara com o intervalo de confiança
interv_conf = 1.96/np.sqrt(len(parp.anos_historico))

for ree in IDS_REES:
    print("Escolhendo ordens dos modelos para REE" +
          f" {ree} - {REES[ree - 1]}")
    serie_facp = parp.correlograma_energia_ree(ree)
    mes = 1
    for a, ano in enumerate(parp.anos_estudo):
        ordens_finais = parp.ordens_finais_ree(ree)[ano]
        for p in range(0, 12):
            # Atualiza as variáveis com as máximas diferenças
            ordem = 1
            for i in range(6):
                if abs(serie_facp[mes][i]) >= interv_conf:
                    ordem = i + 1
            dif = abs(ordem != ordens_finais[p])
            if dif > n_dif_ree[ree]:
                n_dif_ree[ree] = dif
                ano_n_dif_ree[ree] = ano
                periodo_n_dif_ree[ree] = p + 1
                ordem_n_dif_ree[ree] = ordens_finais[p]
                signi_n_dif_ree[ree] = ordem
            mes += 1

print("")
print(" REE | MAX. DIF. |  ANO | MES |" +
      " ORDEM ESCOLHIDA | MAX. SIGNIFIC.")
print("--------------------------------" +
      "---------------------------------")
for ree in IDS_REES:
    str_ree = f"{ree}".rjust(2)
    str_n_dif = "{}".format(n_dif_ree[ree]).rjust(8)
    str_ano = "{}".format(ano_n_dif_ree[ree]).rjust(4)
    str_mes = f"{periodo_n_dif_ree[ree]}".rjust(2)
    str_ordem = f"{ordem_n_dif_ree[ree]}".rjust(15)
    str_signi = "{}".format(signi_n_dif_ree[ree]).rjust(14)
    str_linha = f"  {str_ree} |  {str_n_dif} | {str_ano} | "
    str_linha += f" {str_mes} | {str_ordem} | {str_signi}"
    print(str_linha)
print("---------------------------------" +
      "--------------------------------")
print("")
