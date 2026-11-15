"""Verifica a exportação do memorial e condições de escoamento."""

import math
import subprocess
import sys
from pathlib import Path

import pytest

from hidraulica_condutos.calculos import (
    problema_tipo_1,
    problema_tipo_7,
    problema_tipo_10,
    viscosidade_agua,
)


def test_memorial_tipo_10_em_arquivo(tmp_path):
    """O texto salvo registra as substituições e mantém arquivos existentes."""
    programa = Path(__file__).resolve().parents[1] / "executar_terminal.py"
    arquivo = tmp_path / "memorial.txt"
    comando = [sys.executable, "-I", "-S", "-X", "utf8", str(programa), "--memorial", str(arquivo)]
    entrada = "\n1,419950794\n184\n\n2\n1104\n84\n68\n25\n"
    execucao = subprocess.run(comando, input=entrada, encoding="utf-8", capture_output=True, check=True, timeout=10)
    memorial = arquivo.read_text(encoding="utf-8")
    assert "Memorial salvo" in execucao.stdout
    assert memorial.rstrip() in execucao.stdout
    for etapa in ("h_p = z₁ − z₂", "J = h_p/L = 16/1104", "D = 184/1000", "Re = V D/ν",
                  "f = 2 g D J/V²", "Colebrook-White isolada", "Q = A V", "Rugosidade: 0.5 mm"):
        assert etapa in memorial

    arquivo.write_text("Conteúdo anterior", encoding="utf-8")
    execucao = subprocess.run(comando, input=entrada, encoding="utf-8", capture_output=True, check=True, timeout=10)
    assert "Não foi possível salvar o memorial" in execucao.stdout
    assert arquivo.read_text(encoding="utf-8") == "Conteúdo anterior"


def test_tipo_7_laminar():
    """Confere a solução de Darcy-Weisbach com Re abaixo de 2000."""
    diametro = 0.05
    velocidade = 0.01
    j = 32 * viscosidade_agua(25) * velocidade / (9.806 * diametro**2)
    memorial = []
    calculado, vazao = problema_tipo_7(50, j, 0.2, 25, memorial=memorial)
    assert calculado == pytest.approx(velocidade)
    assert vazao == pytest.approx(math.pi * diametro**2 / 4 * velocidade * 1000)
    assert any("(laminar)" in linha for linha in memorial)


def test_tipo_7_rejeita_transicao():
    """Um gradiente intermediário não deve retornar uma solução inválida."""
    diametro = 0.05
    viscosidade = viscosidade_agua(25)
    velocidade = 2500 * viscosidade / diametro
    j = 32 * viscosidade * velocidade / (9.806 * diametro**2)
    with pytest.raises(ValueError, match="regime laminar ou turbulento"):
        problema_tipo_7(50, j, 0.2, 25)


def test_tipo_1_nao_avalia_pontos_de_transicao():
    """O limite inicial de 10 m teria Re perto de 3000, mas a raiz é turbulenta."""
    j = 16 / 1104
    diametro, _ = problema_tipo_1(21.2, j, 0.5, 25)
    velocidade, vazao = problema_tipo_7(diametro, j, 0.5, 25)
    assert velocidade > 0
    assert vazao == pytest.approx(21.2, rel=0.001)


def test_tipo_10_rejeita_rugosidade_maior_que_diametro():
    with pytest.raises(ValueError, match="superior ao diâmetro"):
        problema_tipo_10(1.4, 184, 10, 25)


def test_terminal_interrompido():
    """Uma entrada terminada antes do cálculo produz uma mensagem legível."""
    programa = Path(__file__).resolve().parents[1] / "executar_terminal.py"
    execucao = subprocess.run(
        [sys.executable, "-I", "-S", "-X", "utf8", str(programa)],
        input="0,5\n", encoding="utf-8", capture_output=True, timeout=10,
    )
    assert execucao.returncode == 1
    assert "Entrada interrompida." in execucao.stdout
    assert execucao.stderr == ""
