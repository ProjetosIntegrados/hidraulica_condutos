"""Cálculos hidráulicos para condutos simples sob pressão.

Unidades internas: m, m³/s, m/s e m²/s.
Referência: Aula 7 da disciplina de Hidráulica.
"""

import math

GRAVIDADE = 9.806  # m/s²
TOLERANCIA_DIAMETRO_MM = 0.1
DIAMETRO_MINIMO_M = 0.001
DIAMETRO_MAXIMO_M = 10.0


def mm_para_m(valor_mm):
    """Converte milímetros em metros."""
    return valor_mm / 1000


def litros_para_m3(vazao_ls):
    """Converte L/s em m³/s."""
    return vazao_ls / 1000


def viscosidade_agua(temperatura):
    """Calcula a viscosidade cinemática da água (m²/s), conforme a Aula 7."""
    viscosidade = 1.78e-6 / (
        1 + 0.0337 * temperatura + 0.000221 * temperatura**2
    )
    if not math.isfinite(viscosidade) or viscosidade <= 0:
        raise ValueError("A temperatura não produziu uma viscosidade positiva e finita.")
    return viscosidade


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


def _registrar(memorial, linha):
    """Acrescenta uma etapa ao memorial solicitado pelo chamador."""
    if memorial is not None:
        memorial.append(linha)


def fator_atrito(re, diametro, rugosidade, *, memorial=None):
    """Calcula f pela expressão laminar ou pela iteração de Colebrook-White."""
    if re <= 0 or diametro <= 0 or not 0 <= rugosidade < diametro:
        raise ValueError("O diâmetro e Re devem ser positivos, com 0 ≤ ε < D.")

    if re < 2000:
        f = 64 / re
        _registrar(memorial, f"f = 64 / Re = 64 / {re:.10g} = {f:.10g} (laminar)")
        return f

    if re <= 4000:
        raise ValueError("Regime de transição (2000 ≤ Re ≤ 4000) sem método definido.")

    _registrar(
        memorial,
        "Colebrook-White: f_novo = [-2 log10(ε/(3,71 D) + 2,51/(Re √f))]⁻²",
    )
    _registrar(memorial, f"ε/(3,71 D) = {rugosidade:.10g}/(3,71 × {diametro:.10g}); Re = {re:.10g}")
    f = 0.02
    _registrar(memorial, "Estimativa inicial f = 0,02; parada quando |f_novo − f| < 10⁻¹⁰.")
    for iteracao in range(1, 101):
        argumento = rugosidade / (3.71 * diametro) + 2.51 / (re * math.sqrt(f))
        novo_f = (-2 * math.log10(argumento)) ** -2
        if memorial is not None:
            memorial.append(
                f"  f, iteração {iteracao}: f anterior = {f:.10g}; "
                f"f_novo = [-2 log10({argumento:.10g})]⁻² = {novo_f:.10g}"
            )
        if abs(novo_f - f) < 1e-10:
            return novo_f
        f = novo_f

    raise RuntimeError("O cálculo de Colebrook-White não convergiu.")


def problema_tipo_7(diametro_mm, perda_unitaria, rugosidade_mm, temperatura, *, memorial=None):
    """Tipo 7: conhecidos D, J, ε e T; determina V (m/s) e Q (L/s)."""
    diametro = mm_para_m(diametro_mm)
    rugosidade = mm_para_m(rugosidade_mm)
    viscosidade = viscosidade_agua(temperatura)

    if diametro <= 0 or perda_unitaria <= 0 or not 0 <= rugosidade < diametro:
        raise ValueError("Informe D e J positivos, com 0 ≤ ε < D.")

    # Primeiro verifica se a solução explícita do regime laminar é aplicável.
    v_laminar = GRAVIDADE * perda_unitaria * diametro**2 / (32 * viscosidade)
    re_laminar = reynolds(v_laminar, diametro, viscosidade)
    if re_laminar < 2000:
        velocidade_media = v_laminar
        _registrar(memorial,
                   f"V = g J D²/(32ν) = {GRAVIDADE} × {perda_unitaria:.10g} × "
                   f"{diametro:.10g}²/(32 × {viscosidade:.10g}) = {velocidade_media:.10g} m/s")
        _registrar(memorial, f"Re = V D/ν = {re_laminar:.10g} (laminar)")
    else:
        auxiliar = math.sqrt(2 * GRAVIDADE * perda_unitaria * diametro)
        termo_rugosidade = rugosidade / (3.71 * diametro)
        termo_viscosidade = 2.51 * viscosidade / (diametro * auxiliar)
        velocidade_media = -2 * auxiliar * math.log10(termo_rugosidade + termo_viscosidade)
        re = reynolds(velocidade_media, diametro, viscosidade)
        if re <= 4000:
            raise ValueError("Os dados não produziram solução em regime laminar ou turbulento.")

        _registrar(memorial,
                   f"U = √(2 g J D) = √(2 × {GRAVIDADE} × {perda_unitaria:.10g} × "
                   f"{diametro:.10g}) = {auxiliar:.10g} m/s")
        _registrar(memorial, "Colebrook-White e Darcy-Weisbach: V = −2 U log10(ε/(3,71 D) + 2,51ν/(D U))")
        _registrar(memorial,
                   f"V = −2 × {auxiliar:.10g} × log10({termo_rugosidade:.10g} + "
                   f"{termo_viscosidade:.10g}) = {velocidade_media:.10g} m/s")
        _registrar(memorial,
                   f"Re = V D/ν = {velocidade_media:.10g} × {diametro:.10g}/"
                   f"{viscosidade:.10g} = {re:.10g} (turbulento)")

    if memorial is not None:
        f = 2 * GRAVIDADE * diametro * perda_unitaria / velocidade_media**2
        _registrar(memorial,
                   f"f = 2 g D J/V² = 2 × {GRAVIDADE} × {diametro:.10g} × "
                   f"{perda_unitaria:.10g}/{velocidade_media:.10g}² = {f:.10g}")
    return velocidade_media, _vazao_pela_continuidade(diametro, velocidade_media, memorial)


def _buscar_diametro(perda, j_alvo, inferior, superior, historico, memorial):
    """Encontra D por bisseção em um intervalo onde J(D) é decrescente."""
    if inferior > superior or not perda(inferior) >= j_alvo >= perda(superior):
        raise ValueError("Sem solução turbulenta no intervalo de diâmetros. Confira os dados e o regime.")

    _registrar(memorial, f"Bisseção: D inicial entre {inferior * 1000:.10g} e {superior * 1000:.10g} mm.")
    tolerancia = f"{TOLERANCIA_DIAMETRO_MM:g}".replace(".", ",")
    _registrar(memorial, f"Alvo J = {j_alvo:.10g} m/m; largura final de até {tolerancia} mm.")
    _registrar(memorial, "Em cada tentativa: D = (D inferior + D superior)/2.")
    _registrar(memorial, "Se J(D) > J alvo, atualiza D inferior; nos demais casos, atualiza D superior.")
    tolerancia_m = mm_para_m(TOLERANCIA_DIAMETRO_MM)
    iteracao = 0
    while superior - inferior > tolerancia_m:
        diametro = (inferior + superior) / 2
        j = perda(diametro)
        iteracao += 1
        if historico is not None or memorial is not None:
            erro = abs(j - j_alvo) / j_alvo * 100
            if historico is not None:
                historico.append({
                    "iteracao": iteracao, "diametro_mm": diametro * 1000,
                    "j_calculado": j, "erro_percentual": erro,
                })
            _registrar(memorial,
                       f"  D, iteração {iteracao}: {diametro * 1000:.10g} mm; J(D) = {j:.10g} m/m; "
                       f"diferença relativa = {erro:.6g}%")

        if j > j_alvo:
            inferior = diametro
        else:
            superior = diametro

    diametro = (inferior + superior) / 2
    _registrar(memorial,
               f"D final = ({inferior * 1000:.10g} + {superior * 1000:.10g})/2 "
               f"= {diametro * 1000:.10g} mm após {iteracao} iterações.")
    return diametro


def problema_tipo_1(
    vazao_ls, perda_unitaria, rugosidade_mm, temperatura, registrar_iteracoes=False,
    *, memorial=None,
):
    """Tipo 1: conhecidos Q, J, ε e T; determina D (mm) e V (m/s)."""
    if vazao_ls <= 0 or perda_unitaria <= 0 or rugosidade_mm < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    vazao = litros_para_m3(vazao_ls)
    rugosidade = mm_para_m(rugosidade_mm)
    viscosidade = viscosidade_agua(temperatura)
    historico = [] if registrar_iteracoes else None

    # Para Q fixa, J laminar = 128νQ/(πgD⁴) e Re é inversamente proporcional a D.
    diametro_laminar = (128 * viscosidade * vazao / (math.pi * GRAVIDADE * perda_unitaria)) ** 0.25
    re_laminar = reynolds(velocidade(vazao, diametro_laminar), diametro_laminar, viscosidade)
    if re_laminar < 2000:
        diametro = diametro_laminar
        if not DIAMETRO_MINIMO_M <= diametro <= DIAMETRO_MAXIMO_M or rugosidade >= diametro:
            raise ValueError("Diâmetro fora dos limites de cálculo.")
        _registrar(memorial,
                   f"D = [128νQ/(πgJ)]^(1/4) = [128 × {viscosidade:.10g} × {vazao:.10g}/"
                   f"(π × {GRAVIDADE} × {perda_unitaria:.10g})]^(1/4) = {diametro:.10g} m (laminar)")
    else:
        # Limita as tentativas a Re > 4000, evitando avaliar pontos de transição.
        superior = min(DIAMETRO_MAXIMO_M, vazao / (1000 * math.pi * viscosidade) * (1 - 1e-12))
        inferior = max(DIAMETRO_MINIMO_M, math.nextafter(rugosidade, math.inf))

        def perda(d):
            return _calcular_j(velocidade(vazao, d), d, rugosidade_mm, temperatura)

        _registrar(memorial, "Em cada tentativa: A = πD²/4, V = Q/A, Re = VD/ν e J(D) = fV²/(2gD).")
        diametro = _buscar_diametro(perda, perda_unitaria, inferior, superior, historico, memorial)

    velocidade_media = _velocidade_pela_continuidade(vazao, diametro, memorial)
    if memorial is not None:
        memorial.append("Verificação da perda unitária no diâmetro final")
        _calcular_j(velocidade_media, diametro, rugosidade_mm, temperatura, memorial)
    if historico is not None:
        return diametro * 1000, velocidade_media, historico
    return diametro * 1000, velocidade_media


def _vazao_pela_continuidade(diametro, velocidade_media, memorial):
    area = area_conduto(diametro)
    vazao = area * velocidade_media
    _registrar(memorial, f"A = π D²/4 = π × {diametro:.10g}²/4 = {area:.10g} m²")
    _registrar(memorial, f"Q = A V = {area:.10g} × {velocidade_media:.10g} = {vazao:.10g} m³/s = {vazao * 1000:.10g} L/s")
    return vazao * 1000


def _velocidade_pela_continuidade(vazao, diametro, memorial):
    area = area_conduto(diametro)
    velocidade_media = vazao / area
    _registrar(memorial, f"A = π D²/4 = π × {diametro:.10g}²/4 = {area:.10g} m²")
    _registrar(memorial, f"V = Q/A = {vazao:.10g}/{area:.10g} = {velocidade_media:.10g} m/s")
    return velocidade_media


def _diametro_pela_continuidade(vazao_ls, velocidade_media, memorial):
    """Calcula D em metros pela relação D = √(4Q / (πV))."""
    if velocidade_media <= 0 or vazao_ls <= 0:
        raise ValueError("A velocidade e a vazão devem ser positivas.")

    vazao = litros_para_m3(vazao_ls)
    diametro = math.sqrt(4 * vazao / (math.pi * velocidade_media))
    _registrar(memorial,
               f"D = √(4Q/(πV)) = √(4 × {vazao:.10g}/(π × {velocidade_media:.10g})) "
               f"= {diametro:.10g} m = {diametro * 1000:.10g} mm")
    return diametro


def _calcular_j(velocidade_media, diametro, rugosidade_mm, temperatura, memorial=None):
    """Calcula J com V e D em unidades do SI."""
    viscosidade = viscosidade_agua(temperatura)
    re = reynolds(velocidade_media, diametro, viscosidade)
    _registrar(memorial,
               f"Re = V D/ν = {velocidade_media:.10g} × {diametro:.10g}/"
               f"{viscosidade:.10g} = {re:.10g}")
    f = fator_atrito(re, diametro, mm_para_m(rugosidade_mm), memorial=memorial)
    j = perda_carga_unitaria(f, velocidade_media, diametro)
    _registrar(memorial,
               f"J = f V²/(2 g D) = {f:.10g} × {velocidade_media:.10g}²/"
               f"(2 × {GRAVIDADE} × {diametro:.10g}) = {j:.10g} m/m")
    return j


def problema_tipo_2(velocidade_media, rugosidade_mm, vazao_ls, temperatura, *, memorial=None):
    """Tipo 2: determina D (mm) e J (m/m) a partir de V, ε e Q."""
    diametro = _diametro_pela_continuidade(vazao_ls, velocidade_media, memorial)
    j = _calcular_j(velocidade_media, diametro, rugosidade_mm, temperatura, memorial)
    return diametro * 1000, j


def problema_tipo_5(diametro_mm, vazao_ls, rugosidade_mm, temperatura, *, memorial=None):
    """Tipo 5: determina V (m/s) e J (m/m) a partir de D, Q e ε."""
    if diametro_mm <= 0 or vazao_ls <= 0:
        raise ValueError("O diâmetro e a vazão devem ser positivos.")

    diametro = mm_para_m(diametro_mm)
    velocidade_media = _velocidade_pela_continuidade(litros_para_m3(vazao_ls), diametro, memorial)
    j = _calcular_j(velocidade_media, diametro, rugosidade_mm, temperatura, memorial)
    return velocidade_media, j


def problema_tipo_4(velocidade_media, perda_unitaria, rugosidade_mm, temperatura, *, memorial=None):
    """Tipo 4: determina D (mm) e Q (L/s) a partir de V, J e ε."""
    if velocidade_media <= 0 or perda_unitaria <= 0 or rugosidade_mm < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    viscosidade = viscosidade_agua(temperatura)
    rugosidade = mm_para_m(rugosidade_mm)
    diametro_laminar = math.sqrt(32 * viscosidade * velocidade_media / (GRAVIDADE * perda_unitaria))
    if reynolds(velocidade_media, diametro_laminar, viscosidade) < 2000:
        diametro = diametro_laminar
        if not DIAMETRO_MINIMO_M <= diametro <= DIAMETRO_MAXIMO_M or rugosidade >= diametro:
            raise ValueError("Diâmetro fora dos limites de cálculo.")
        _registrar(memorial,
                   f"D = √(32νV/(gJ)) = √(32 × {viscosidade:.10g} × {velocidade_media:.10g}/"
                   f"({GRAVIDADE} × {perda_unitaria:.10g})) = {diametro:.10g} m (laminar)")
    else:
        # Para V fixa, Re cresce com D. A busca turbulenta começa acima de Re = 4000.
        inferior = max(
            DIAMETRO_MINIMO_M, math.nextafter(rugosidade, math.inf),
            4000 * viscosidade / velocidade_media * (1 + 1e-12),
        )

        def perda(d):
            return _calcular_j(velocidade_media, d, rugosidade_mm, temperatura)

        _registrar(memorial, "Em cada tentativa: Re = VD/ν e J(D) = fV²/(2gD).")
        diametro = _buscar_diametro(perda, perda_unitaria, inferior, DIAMETRO_MAXIMO_M, None, memorial)

    vazao = _vazao_pela_continuidade(diametro, velocidade_media, memorial)
    if memorial is not None:
        memorial.append("Verificação da perda unitária no diâmetro final")
        _calcular_j(velocidade_media, diametro, rugosidade_mm, temperatura, memorial)
    return diametro * 1000, vazao


def _determinar_rugosidade(velocidade_media, diametro, perda_unitaria, temperatura, memorial):
    """Isola ε em Colebrook-White depois de obter f por Darcy-Weisbach."""
    if velocidade_media <= 0 or diametro <= 0 or perda_unitaria <= 0:
        raise ValueError("A velocidade, o diâmetro e a perda unitária devem ser positivos.")

    viscosidade = viscosidade_agua(temperatura)
    re = reynolds(velocidade_media, diametro, viscosidade)
    if re <= 4000:
        raise ValueError("A rugosidade por Colebrook-White exige escoamento turbulento (Re > 4000).")

    raiz_f = math.sqrt(2 * GRAVIDADE * diametro * perda_unitaria) / velocidade_media
    termo_atrito = 10 ** (-1 / (2 * raiz_f))
    termo_viscosidade = 2.51 / (re * raiz_f)
    if termo_atrito < termo_viscosidade and not math.isclose(termo_atrito, termo_viscosidade, rel_tol=1e-8):
        raise ValueError("Os dados resultam em rugosidade negativa.")

    rugosidade = 3.71 * diametro * max(0, termo_atrito - termo_viscosidade)
    if rugosidade >= diametro:
        raise ValueError("Os dados resultam em rugosidade igual ou superior ao diâmetro.")

    _registrar(memorial,
               f"Re = V D/ν = {velocidade_media:.10g} × {diametro:.10g}/"
               f"{viscosidade:.10g} = {re:.10g} (turbulento)")
    _registrar(memorial,
               f"f = 2 g D J/V² = 2 × {GRAVIDADE} × {diametro:.10g} × "
               f"{perda_unitaria:.10g}/{velocidade_media:.10g}² = {raiz_f**2:.10g}")
    _registrar(memorial, "Colebrook-White isolada: ε = 3,71 D [10^(−1/(2√f)) − 2,51/(Re √f)]")
    _registrar(memorial,
               f"ε = 3,71 × {diametro:.10g} × ({termo_atrito:.10g} − {termo_viscosidade:.10g}) "
               f"= {rugosidade:.10g} m = {rugosidade * 1000:.10g} mm")
    return rugosidade * 1000


def problema_tipo_3(velocidade_media, perda_unitaria, vazao_ls, temperatura, *, memorial=None):
    """Tipo 3: determina ε (mm) e D (mm) a partir de V, J e Q."""
    diametro = _diametro_pela_continuidade(vazao_ls, velocidade_media, memorial)
    rugosidade = _determinar_rugosidade(velocidade_media, diametro, perda_unitaria, temperatura, memorial)
    return rugosidade, diametro * 1000


def problema_tipo_6(vazao_ls, diametro_mm, perda_unitaria, temperatura, *, memorial=None):
    """Tipo 6: determina ε (mm) e V (m/s) a partir de Q, D e J."""
    if diametro_mm <= 0:
        raise ValueError("O diâmetro deve ser positivo.")

    diametro = mm_para_m(diametro_mm)
    velocidade_media = _velocidade_pela_continuidade(litros_para_m3(vazao_ls), diametro, memorial)
    rugosidade = _determinar_rugosidade(velocidade_media, diametro, perda_unitaria, temperatura, memorial)
    return rugosidade, velocidade_media


def problema_tipo_10(velocidade_media, diametro_mm, perda_unitaria, temperatura, *, memorial=None):
    """Tipo 10: determina ε (mm) e Q (L/s) a partir de V, D e J."""
    diametro = mm_para_m(diametro_mm)
    rugosidade = _determinar_rugosidade(velocidade_media, diametro, perda_unitaria, temperatura, memorial)
    return rugosidade, _vazao_pela_continuidade(diametro, velocidade_media, memorial)
