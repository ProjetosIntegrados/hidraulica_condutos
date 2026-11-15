"""Verifica os seis casos adicionais pelo inicializador do terminal."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

from hidraulica_condutos.calculos import problema_tipo_4, problema_tipo_10


# Valores coerentes do Exemplo 3 da Aula 7. Mudamos os dados fornecidos
# para verificar se cada rotina recupera as grandezas ocultadas.
REFERENCIA = {"D": 184, "e": 0.5, "V": 1.419950794157626, "Q": 37.75711670736717}
J_REFERENCIA = 16 / 1104


@pytest.mark.parametrize(
    "tipo, conhecidos, esperados, equacao",
    [
        (2, {"V", "Q", "e"}, {"Diâmetro": 184, "Perda de carga unitária": J_REFERENCIA}, "D = √(4Q/(πV))"),
        (3, {"V", "Q", "J"}, {"Rugosidade": 0.5, "Diâmetro": 184}, "Colebrook-White isolada"),
        (4, {"V", "J", "e"}, {"Diâmetro": 184, "Vazão": 37.7571}, "D final ="),
        (5, {"D", "Q", "e"}, {"Velocidade": 1.42, "Perda de carga unitária": J_REFERENCIA}, "J = f V²/(2 g D)"),
        (6, {"D", "Q", "J"}, {"Rugosidade": 0.5, "Velocidade": 1.42}, "V = Q/A"),
        (10, {"D", "V", "J"}, {"Rugosidade": 0.5, "Vazão": 37.7571}, "Q = A V"),
    ],
)
def test_demais_tipos_pelo_terminal(tipo, conhecidos, esperados, equacao):
    """Confere a identificação e os resultados sem instalar o pacote."""
    respostas = [str(REFERENCIA[chave]) if chave in conhecidos else "" for chave in "QVDe"]
    respostas.extend(["1", str(J_REFERENCIA)] if "J" in conhecidos else [""])
    respostas.append("25")

    inicializador = Path(__file__).resolve().parents[1] / "executar_terminal.py"
    execucao = subprocess.run(
        [sys.executable, "-I", "-S", "-X", "utf8", str(inicializador)],
        input="\n".join(respostas) + "\n",
        capture_output=True,
        encoding="utf-8",
        check=True,
        timeout=10,
    )
    assert f"Problema identificado: TIPO {tipo}\n" in execucao.stdout
    resultados, memorial = execucao.stdout.split("\nRESULTADOS\n")[1].split("\nMEMORIAL DE CÁLCULO\n")
    assert equacao in memorial and "m²/s" in memorial
    linhas = re.findall(r"^([^:\n]+): ([\d.eE+-]+)", resultados, re.M)
    valores = {nome: float(valor) for nome, valor in linhas}
    assert valores.keys() == esperados.keys()
    for nome, valor in esperados.items():
        # O arredondamento do diâmetro influi na vazão calculada no tipo 4.
        tolerancia = 0.02 if tipo == 4 and nome == "Vazão" else 1e-7
        assert valores[nome] == pytest.approx(valor, abs=tolerancia)


def test_tipo_4_em_regime_laminar():
    """Recupera 50 mm a partir da perda unitária laminar teórica."""
    diametro, vazao = problema_tipo_4(0.01, 1.1730785205473436e-5, 0.2, 25)
    assert diametro == pytest.approx(50, rel=1e-3)
    assert vazao == pytest.approx(0.019635, rel=1e-3)


@pytest.mark.parametrize(
    "velocidade, perda, mensagem",
    [(0.01, J_REFERENCIA, "turbulento"), (REFERENCIA["V"], 0.001, "negativa")],
)
def test_tipo_10_rejeita_rugosidade_sem_solucao(velocidade, perda, mensagem):
    """Rejeita inferência em regime laminar e dados incompatíveis."""
    with pytest.raises(ValueError, match=mensagem):
        problema_tipo_10(velocidade, 184, perda, 25)
