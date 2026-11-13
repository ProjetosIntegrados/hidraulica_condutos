
# ============================================================
# TESTES DA EXECUÇÃO COMPLETA PELO TERMINAL
#
# Simula a entrada de dados pelo usuário e verifica
# se o programa identifica e resolve os problemas.
# ============================================================

from hidraulica_condutos.main import main, ler_numero


def simular_entrada(monkeypatch, respostas):
    """
    Substitui temporariamente o teclado por respostas
    previamente definidas para o teste.
    """
    entradas = iter(respostas)

    monkeypatch.setattr(
        "builtins.input",
        lambda mensagem="": next(entradas)
    )


def test_terminal_tipo_1(monkeypatch, capsys):
    """Verifica o dimensionamento completo do tipo 1."""

    # Dados do exemplo da Aula 7.
    simular_entrada(monkeypatch, [
        "47,1",  # Vazão Q
        "",      # Velocidade desconhecida
        "",      # Diâmetro desconhecido
        "0,06",  # Rugosidade
        "2",     # Calcular J pelas cotas
        "1104",  # Comprimento
        "84",    # Cota 1
        "68",    # Cota 2
        "25",    # Temperatura
    ])

    # Executa o programa como se fosse um usuário.
    main()

    # Captura o texto apresentado no terminal.
    saida = capsys.readouterr().out

    assert "Problema identificado: TIPO 1" in saida
    assert "Diâmetro: 184.426 mm" in saida
    assert "Velocidade: 1.7631 m/s" in saida


def test_terminal_tipo_7(monkeypatch, capsys):
    """Verifica a execução completa do tipo 7."""

    simular_entrada(monkeypatch, [
        "",      # Vazão desconhecida
        "",      # Velocidade desconhecida
        "184",   # Diâmetro
        "0,5",   # Rugosidade
        "2",     # Calcular J pelas cotas
        "1104",  # Comprimento
        "84",    # Cota 1
        "68",    # Cota 2
        "25",    # Temperatura
    ])

    main()

    saida = capsys.readouterr().out

    assert "Problema identificado: TIPO 7" in saida
    assert "Velocidade: 1.4200 m/s" in saida
    assert "Vazão: 37.7571 L/s" in saida


def test_temperatura_ausente(monkeypatch, capsys):
    """Verifica se o programa detecta a falta de temperatura."""

    simular_entrada(monkeypatch, [
        "", "", "", "", "", ""
    ])

    main()

    saida = capsys.readouterr().out

    assert "É necessário informar a temperatura." in saida


def test_entrada_invalida(monkeypatch, capsys):
    """Verifica se uma entrada inválida pode ser corrigida."""

    simular_entrada(monkeypatch, [
        "abc",
        "3,5",
    ])

    resultado = ler_numero("Valor: ")
    saida = capsys.readouterr().out

    assert "Valor inválido" in saida
    assert resultado == 3.5
