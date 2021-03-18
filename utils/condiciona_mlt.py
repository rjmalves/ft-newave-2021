from inewave.newave.confhd import LeituraConfhd
from inewave.newave.vazpast import LeituraVazPast, EscritaVazPast
from inewave.config import REES
from typing import List

#     Dados de entrada    #
# Local do caso a ser condicionado
dir_caso = "/home/rogerio/ONS/validacao_newave2745/pmo_2021_01_sul_150_mlt_parp"
# REEs a serem condicionadas
rees = ["SUL", "IGUACU"]
# Porcentagem da MLT
mlt_cond = 1.5
# ----------------------- #

# Postos das usinas nas REEs a serem condicionadas
usinas_rees: List[int] = []

# Lista as usinas nas REES a serem condicionadas
indices_rees = [REES.index(r) + 1 for r in rees]
confhd = LeituraConfhd(dir_caso).le_arquivo()
usinas = confhd.usinas
for _, u in usinas.items():
    if u.ree in indices_rees:
        usinas_rees.append(u.posto)

# Lê o arquivo vazpast, condiciona a alfuência de cada mês pela fração da MLT
# fornecida, somente para as usinas selecionadas, e sobrescreve o arquivo.
vazpast = LeituraVazPast(dir_caso).le_arquivo()
for i, p in enumerate(vazpast.postos):
    if p in usinas_rees:
        vazpast.tabela[i, :] *= mlt_cond

# Escreve o vazpast de saída
EscritaVazPast(dir_caso).escreve_arquivo(vazpast)
