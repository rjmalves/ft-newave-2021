# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 01
#
# Processar estudos com base no PMO/PLD e PEN nas versões
# 27 (versão oficial) e 27.4.3 (em validação), sem a nova
# funcionalidade habilitada.
# Comparar os resultados a partir da análise das impressões
# no PMO.DAT, PARP.DAT e NWLISTOP.

# INSTRUÇÕES PARA USO DO SCRIPT DE TESTE
#
# 1- Substituir nas variáveis auxiliares os diretórios onde
#    foram executadas as respectivas versões do NEWAVE.
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
#    python testes/teste01.py
#
# 6- Observar a saída exibida no terminal.

from inewave.newave.pmo import PMO
from inewave.newave.parp import PARp
from inewave.nwlistop.mediassin import MediasSIN
from inewave.nwlistop.mediasmerc import MediasMerc


# Variáveis auxiliares no processo
diretorio_v270000 = ""
diretorio_v270403 = ""

# Lê os arquivos de cada diretório
pmo_v270000 = PMO.le_arquivo(diretorio_v270000)
pmo_v270403 = PMO.le_arquivo(diretorio_v270403)
parp_v270000 = PARp.le_arquivo(diretorio_v270000)
parp_v270403 = PARp.le_arquivo(diretorio_v270403)
mediassin_v270000 = MediasSIN.le_arquivo(diretorio_v270000)
mediassin_v270403 = MediasSIN.le_arquivo(diretorio_v270403)
mediasmerc_v270000 = MediasMerc.le_arquivo(diretorio_v270000)
mediasmerc_v270403 = MediasMerc.le_arquivo(diretorio_v270403)

# Compara os dados lidos
pmo_iguais = (pmo_v270000.custo_operacao_series_simuladas ==
              pmo_v270403.custo_operacao_series_simuladas)
parp_iguais = (parp_v270000.coeficientes_ree(1) ==
               parp_v270403.coeficientes_ree(1))
mediassin_iguais = mediassin_v270000.medias == mediassin_v270403.medias
mediasmerc_iguais = mediasmerc_v270000.medias == mediasmerc_v270403.medias

print(f"Arquivos pmo.dat iguais: {pmo_iguais}")
print(f"Arquivos parp.dat iguais: {parp_iguais}")
print(f"Arquivos MEDIAS-SIN.CSV iguais: {mediassin_iguais}")
print(f"Arquivos MEDIAS-MERC.CSV iguais: {mediasmerc_iguais}")
