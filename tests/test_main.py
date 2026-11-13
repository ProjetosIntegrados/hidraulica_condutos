
# ============================================================
# TESTES DA INTERFACE PELO TERMINAL
#
# Verifica a identificação automática dos problemas
# e a interpretação dos valores digitados.
#
# Esses testes não modificam os cálculos hidráulicos.
# ============================================================

import pytest

from hidraulica_condutos.main import (
    identificar_tipo,
    ler_numero,
)


# ============================================================
# 1. IDENTIFICAÇÃO DOS TIPOS DE PROBLEMAS
# ============================================================

@pytest.mark.parametrize(
    "conhecidos, tipo_esperado",
    [
        (("Q", "J", "e"), 1),
        (("V", "e", "Q"), 2),
        (("V", "J", "Q"), 3),
        (("V", "J", "e"), 4),
        (("D", "Q", "e"), 5),
        (("Q", "D", "J"), 6),
        (("D", "J", "e"), 7),
        (("V", "D", "J"), 10),
    ],
)
def test_identificacao_tipos(conhecidos, tipo_esperado):
    """
    Verifica as oito combinações de dados cadastradas.

    Atenção: identificação não significa que a rotina
    hidráulica do tipo já esteja implementada.
    """

    # Inicialmente, todas as grandezas são desconhecidas.
    dados = {
        "Q": None,
        "V": None,
        "D": None,
        "e": None,
        "J": None,
    }

    # Preenche apenas as grandezas conhecidas.
    for chave in conhecidos:
        dados[chave] = 1.0

    # Confere o tipo identificado.
    assert identificar_tipo(dados) == tipo_esperado


# ============================================================
# 2. COMBINAÇÕES NÃO RECONHECIDAS
# ============================================================

def test_combinacao_incompleta():
    """Duas grandezas não identificam um tipo cadastrado."""

    dados = {
        "Q": 10.0,
        "V": None,
        "D": None,
        "e": 0.1,
        "J": None,
    }

    assert identificar_tipo(dados) is None


def test_combinacao_com_dados_excedentes():
    """Verifica a rejeição de combinação não cadastrada."""

    dados = {
        "Q": 10.0,
        "V": 2.0,
        "D": 100.0,
        "e": 0.1,
        "J": 0.01,
    }

    assert identificar_tipo(dados) is None


# ============================================================
# 3. ENTRADA DE DADOS
# ============================================================

def test_entrada_com_virgula(monkeypatch):
    """Verifica a interpretação da vírgula decimal."""

    monkeypatch.setattr(
        "builtins.input",
        lambda mensagem: "3,5"
    )

    assert ler_numero("Valor: ") == 3.5


def test_campo_vazio(monkeypatch):
    """Campo vazio representa uma grandeza desconhecida."""

    monkeypatch.setattr(
        "builtins.input",
        lambda mensagem: ""
    )

    assert ler_numero("Valor: ") is None
