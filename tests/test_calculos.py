
# ============================================================
# TESTES DOS CÁLCULOS HIDRÁULICOS
#
# Verifica se o programa reproduz os exemplos resolvidos
# apresentados na Aula 7.
# ============================================================

from hidraulica_condutos.calculos import problema_tipo_7


def test_problema_tipo_7():
    """
    Testa o exemplo 3 da Aula 7, página 29.

    Dados:
        D = 184 mm
        J = 16 / 1104 m/m
        ε = 0,5 mm
        T = 25 °C

    Resultados aproximados da aula:
        V = 1,42 m/s
        Q = 37,8 L/s
    """

    # Executamos o cálculo com os dados do exercício.
    velocidade, vazao = problema_tipo_7(
        diametro_mm=184,
        perda_unitaria=16 / 1104,
        rugosidade_mm=0.5,
        temperatura=25
    )

    # Comparamos os resultados com os valores da aula.
    # A tolerância considera os arredondamentos do professor.
    assert abs(velocidade - 1.42) < 0.02
    assert abs(vazao - 37.8) < 0.5

# ============================================================
# TESTE DO PROBLEMA TIPO 1 - DIMENSIONAMENTO
# ============================================================

from hidraulica_condutos.calculos import problema_tipo_1


def test_problema_tipo_1():
    """
    Verifica o Exemplo 2 da Aula 7, páginas 26 e 27.

    Dados:
        Q = 47,1 L/s
        J = 16 / 1104 m/m
        ε = 0,06 mm
        T = 25 °C

    Resultado esperado:
        D aproximadamente 184 mm.
    """

    # Executamos a rotina com os dados do professor.
    diametro, velocidade_media = problema_tipo_1(
        vazao_ls=47.1,
        perda_unitaria=16 / 1104,
        rugosidade_mm=0.06,
        temperatura=25,
    )

    # Conferimos o diâmetro com tolerância de 1 mm,
    # considerando o arredondamento da aula.
    assert abs(diametro - 184) < 1

    # Conferimos se a velocidade calculada é positiva.
    assert velocidade_media > 0
