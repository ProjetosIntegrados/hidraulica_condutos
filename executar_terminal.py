
# ============================================================
# PROJETO: CÁLCULO DE CONDUTOS SOB PRESSÃO
# ARQUIVO: executar_terminal.py
#
# Objetivo:
# Iniciar a versão do programa pelo terminal,
# sem exigir a instalação do Poetry.
#
# Requisito: Python compatível instalado no computador.
# ============================================================

import sys
from pathlib import Path


# Identifica a pasta onde este arquivo está localizado.
pasta_projeto = Path(__file__).resolve().parent

# Localiza a pasta "src", que contém nosso pacote Python.
pasta_src = pasta_projeto / "src"

# Adiciona "src" aos caminhos de pesquisa do Python.
# Isso permite importar o pacote sem instalar o projeto.
sys.path.insert(0, str(pasta_src))


# Importa a função principal do programa pelo terminal.
from hidraulica_condutos.main import main


# Inicia o programa quando este arquivo for executado.
if __name__ == "__main__":
    main()
