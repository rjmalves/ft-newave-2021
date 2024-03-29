# FORÇA-TAREFA DE VALIDAÇÃO DO MODELO NEWAVE V27.04.03
# FEVEREIRO / 2021

# TESTE 06
#
# Processar um caso com a funcionalidade PAR(p)-A habilitada,
# executar o programa NWLISTCF e avaliar:
# 1) impressão dos estados afluências passadas o arquivo estados.rel
# 2) impressão dos coeficientes das afluências passadas nos cortes
#    no arquivo nwlistcf.rel
# 3) o cálculo do termo constante (RHS) de um corte qualquer
# 4) impressão do identificador do corte em substituição ao nº do
#    próximo corte na coluna IREG do arquivo nwlistcf.rel.

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
#    python testes/teste06.py
#
# 6- Observar a saída exibida no terminal.

from inewave.nwlistcf import Nwlistcf, Estados

# OBSERVAÇÃO: TESTE NÃO ESTÁ FUNCIONANDO NO MOMENTO
# DEVIDO A MUDANÇA NO FORMATO DOS ARQUIVOS DO NWLISTCF.

# TODO - ATUALIZAR NA INEWAVE A LEITURA DOS ARQUIVOS
