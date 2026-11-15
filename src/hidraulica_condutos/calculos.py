"""Cálculos hidráulicos para condutos simples sob pressão.

Unidades internas: m, m³/s, m/s e m²/s.
Referência: Aula 7 da disciplina de Hidráulica.
"""

import math

GRAVIDADE = 9.806  # m/s²
TOLERANCIA_DIAMETRO_MM = 0.1


def mm_para_m(valor_mm):
    """Converte milímetros em metros."""
    return valor_mm / 1000


def litros_para_m3(vazao_ls):
    """Converte L/s em m³/s."""
    return vazao_ls / 1000


def viscosidade_agua(temperatura):
    """Calcula a viscosidade cinemática da água (m²/s), conforme a Aula 7."""
    return 1.78e-6 / (
        1 + 0.0337 * temperatura + 0.000221 * temperatura**2
    )


def area_conduto(diametro):
    """Área interna do tubo circular (m²): A = πD²/4."""
    return math.pi * diametro**2 / 4


def velocidade(vazao, diametro):
    """Velocidade média (m/s) pela continuidade: V = Q/A."""
    return vazao / area_conduto(diametro)


def reynolds(velocidade_media, diametro, viscosidade):
    """Número de Reynolds: Re = V D / ν."""
    return velocidade_media * diametro / viscosidade


def perda_carga_unitaria(fator_atrito, velocidade_media, diametro):
    """Darcy-Weisbach: J = f V² / (2 g D), em m/m."""
    return fator_atrito * velocidade_media**2 / (diametro * 2 * GRAVIDADE)


def fator_atrito(re, diametro, rugosidade):
    """Calcula f: regime laminar ou Colebrook-White para turbulento."""
    if re <= 0 or diametro <= 0 or rugosidade < 0:
        raise ValueError("Parâmetros hidráulicos inválidos.")

    if re < 2000:
        return 64 / re

    # A faixa de transição não possui método definido no projeto.
    if re <= 4000:
        raise ValueError(
            "Regime de transição entre laminar e turbulento: "
            "o método ainda não foi definido."
        )

    # Colebrook-White: atualiza f até convergir ou atingir 100 iterações.
    f = 0.02
    for _ in range(100):
        argumento = rugosidade / (3.71 * diametro) + 2.51 / (re * math.sqrt(f))
        novo_f = (-2 * math.log10(argumento)) ** -2
        if abs(novo_f - f) < 1e-10:
            return novo_f
        f = novo_f

    raise RuntimeError("O cálculo de Colebrook-White não convergiu.")


def problema_tipo_7(diametro_mm, perda_unitaria, rugosidade_mm, temperatura):
    """Tipo 7: conhecidos D, J, ε e T; determina V (m/s) e Q (L/s)."""
    diametro = mm_para_m(diametro_mm)
    rugosidade = mm_para_m(rugosidade_mm)
    viscosidade = viscosidade_agua(temperatura)

    if diametro <= 0 or perda_unitaria <= 0 or rugosidade < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    # Equação explícita apresentada na Aula 7.
    auxiliar = math.sqrt(2 * GRAVIDADE * perda_unitaria * diametro)
    termo_rugosidade = rugosidade / (3.71 * diametro)
    termo_viscosidade = 2.51 * viscosidade / (diametro * auxiliar)
    velocidade_media = -2 * auxiliar * math.log10(
        termo_rugosidade + termo_viscosidade
    )

    vazao_m3s = area_conduto(diametro) * velocidade_media
    vazao_ls = vazao_m3s * 1000
    return velocidade_media, vazao_ls


def problema_tipo_1(
    vazao_ls, perda_unitaria, rugosidade_mm, temperatura, registrar_iteracoes=False
):
    """Tipo 1: conhecidos Q, J, ε e T; determina D (mm) e V (m/s).

    Com registrar_iteracoes=True, retorna também o histórico do método
    da bisseção, utilizado pela interface gráfica no memorial de cálculo.
    """
    if vazao_ls <= 0 or perda_unitaria <= 0 or rugosidade_mm < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    vazao = litros_para_m3(vazao_ls)
    rugosidade = mm_para_m(rugosidade_mm)
    viscosidade = viscosidade_agua(temperatura)

    def calcular_j(diametro):
        """Obtém J para um diâmetro de tentativa."""
        velocidade_media = velocidade(vazao, diametro)
        re = reynolds(velocidade_media, diametro, viscosidade)
        f = fator_atrito(re, diametro, rugosidade)
        return perda_carga_unitaria(f, velocidade_media, diametro)

    # Intervalo de busca original: diâmetros de 1 mm a 10 m.
    diametro_minimo = 0.001
    diametro_maximo = 10.0
    if not (
        calcular_j(diametro_minimo) >= perda_unitaria
        and calcular_j(diametro_maximo) <= perda_unitaria
    ):
        raise ValueError(
            "Não foi possível encontrar o diâmetro "
            "dentro dos limites de cálculo."
        )

    tolerancia_m = mm_para_m(TOLERANCIA_DIAMETRO_MM)
    historico = [] if registrar_iteracoes else None
    # Cada tentativa reduz o intervalo pela metade.
    while diametro_maximo - diametro_minimo > tolerancia_m:
        diametro = (diametro_minimo + diametro_maximo) / 2
        j_calculado = calcular_j(diametro)

        if historico is not None:
            erro_percentual = abs(j_calculado - perda_unitaria) / perda_unitaria * 100
            historico.append({
                "iteracao": len(historico) + 1,
                "diametro_mm": diametro * 1000,
                "j_calculado": j_calculado,
                "erro_percentual": erro_percentual,
            })

        if j_calculado > perda_unitaria:
            diametro_minimo = diametro
        else:
            diametro_maximo = diametro

    diametro = (diametro_minimo + diametro_maximo) / 2
    diametro_mm = diametro * 1000
    velocidade_media = velocidade(vazao, diametro)

    if historico is not None:
        return diametro_mm, velocidade_media, historico
    return diametro_mm, velocidade_media