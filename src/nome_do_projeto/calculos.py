
import math

# ============================================================
# PROJETO: CÁLCULO DE CONDUTOS SOB PRESSÃO
# MÓDULO: CÁLCULOS HIDRÁULICOS
#
# Este arquivo reúne as equações fundamentais utilizadas
# na resolução dos problemas de condutos simples.
#
# Referência: Aula 7 - Rotina de cálculo de condutos simples
# ============================================================


# Aceleração da gravidade em m/s².
# Foi adotado o mesmo valor utilizado nos exemplos da aula.
GRAVIDADE = 9.806


# ============================================================
# 1. CONVERSÃO DE UNIDADES
# ============================================================

def mm_para_m(valor_mm):
    """
    Converte uma medida de milímetros para metros.

    A conversão é necessária porque as equações hidráulicas
    trabalham com as unidades do Sistema Internacional (SI).
    """

    # Um metro corresponde a 1000 milímetros.
    return valor_mm / 1000


def litros_para_m3(vazao_ls):
    """
    Converte uma vazão de litros por segundo para m³/s.
    """

    # Um metro cúbico corresponde a 1000 litros.
    return vazao_ls / 1000


# ============================================================
# 2. VISCOSIDADE CINEMÁTICA DA ÁGUA
# ============================================================

def viscosidade_agua(temperatura):
    """
    Calcula a viscosidade cinemática da água em função
    da temperatura, conforme a equação da Aula 7.

    Entrada:
        temperatura: temperatura da água em °C

    Saída:
        viscosidade cinemática em m²/s
    """

    # A temperatura influencia a viscosidade da água.
    # Esta equação permite calcular a viscosidade sem
    # precisar consultar uma tabela para cada temperatura.

    viscosidade = 1.78e-6 / (
        1 + 0.0337 * temperatura + 0.000221 * temperatura**2
    )

    return viscosidade


# ============================================================
# 3. EQUAÇÃO DA CONTINUIDADE
# ============================================================

def area_conduto(diametro):
    """
    Calcula a área da seção transversal de um tubo circular.

    Equação:
        A = pi * D² / 4

    Entrada:
        diametro: diâmetro interno do tubo em metros

    Saída:
        área em m²
    """

    area = math.pi * diametro**2 / 4

    return area


def velocidade(vazao, diametro):
    """
    Calcula a velocidade média do escoamento.

    Pela equação da continuidade:
        Q = A * V

    Isolando a velocidade:
        V = Q / A

    Entradas:
        vazao: vazão em m³/s
        diametro: diâmetro interno em metros

    Saída:
        velocidade em m/s
    """

    # Calculamos primeiro a área do tubo.
    area = area_conduto(diametro)

    # Dividimos a vazão pela área para obter a velocidade.
    velocidade_media = vazao / area

    return velocidade_media


# ============================================================
# 4. NÚMERO DE REYNOLDS
# ============================================================

def reynolds(velocidade_media, diametro, viscosidade):
    """
    Calcula o número de Reynolds do escoamento.

    Equação:
        Re = V * D / viscosidade

    O número de Reynolds é adimensional e permite
    identificar o regime de escoamento.

    Conforme a Aula 7:
        Re < 2000: escoamento laminar
        Re > 4000: escoamento turbulento

    A faixa intermediária exige tratamento específico.
    """

    numero_reynolds = (
        velocidade_media * diametro / viscosidade
    )

    return numero_reynolds


# ============================================================
# 5. EQUAÇÃO DE DARCY-WEISBACH
# ============================================================

def perda_carga_unitaria(fator_atrito, velocidade_media, diametro):
    """
    Calcula a perda de carga unitária do conduto.

    Equação:
        J = f * V² / (D * 2 * g)

    Entradas:
        fator_atrito: fator de perda de carga linear
        velocidade_media: velocidade em m/s
        diametro: diâmetro interno em metros

    Saída:
        J: perda de carga unitária em m/m
    """

    # O fator de atrito representa a resistência hidráulica
    # associada ao escoamento dentro da tubulação.
    #
    # A velocidade aparece elevada ao quadrado:
    # quanto maior a velocidade, maior tende a ser a perda.

    J = (
        fator_atrito * velocidade_media**2
        / (diametro * 2 * GRAVIDADE)
    )

    return J


# ============================================================
# 6. FATOR DE ATRITO - COLEBROOK-WHITE
# ============================================================

def fator_atrito(re, diametro, rugosidade):
    """
    Calcula o fator de perda de carga linear (f).

    Entradas:
        re: número de Reynolds
        diametro: diâmetro interno em metros
        rugosidade: rugosidade absoluta em metros

    Para escoamento laminar:
        f = 64 / Re

    Para escoamento turbulento:
        utiliza a equação de Colebrook-White.

    Como Colebrook-White é uma equação implícita,
    o fator f é calculado por tentativas sucessivas.
    """

    # Verificamos se os valores fornecidos são fisicamente
    # válidos antes de iniciar os cálculos.
    if re <= 0 or diametro <= 0 or rugosidade < 0:
        raise ValueError("Parâmetros hidráulicos inválidos.")

    # Para escoamento laminar, o fator depende apenas
    # do número de Reynolds.
    if re < 2000:
        return 64 / re

    # A Aula 7 apresenta a região entre 2000 e 4000
    # separadamente. Por enquanto, não aplicaremos
    # Colebrook-White automaticamente nessa faixa.
    if re <= 4000:
        raise ValueError(
            "Regime de transição entre laminar e turbulento: "
            "o método ainda não foi definido."
        )

    # Adotamos uma estimativa inicial para o fator de atrito.
    # Esse valor será atualizado durante as iterações.
    f = 0.02

    # O programa realizará no máximo 100 tentativas.
    for _ in range(100):

        # Calculamos a expressão que aparece dentro
        # do logaritmo da equação de Colebrook-White.
        argumento = (
            rugosidade / (3.71 * diametro)
            + 2.51 / (re * math.sqrt(f))
        )

        # Aplicamos a equação de Colebrook-White para
        # obter uma nova estimativa do fator de atrito.
        novo_f = (-2 * math.log10(argumento)) ** -2

        # Comparamos o novo valor com o valor anterior.
        # Se a diferença for suficientemente pequena,
        # consideramos que o cálculo convergiu.
        if abs(novo_f - f) < 1e-10:
            return novo_f

        # Caso ainda não tenha convergido, utilizamos
        # o novo valor como estimativa da próxima tentativa.
        f = novo_f

    # Se as 100 tentativas não forem suficientes,
    # informamos que o método não convergiu.
    raise RuntimeError(
        "O cálculo de Colebrook-White não convergiu."
    )

# ============================================================
# 7. PROBLEMA TIPO 7 - VERIFICAÇÃO
# ============================================================

def problema_tipo_7(diametro_mm, perda_unitaria, rugosidade_mm,
                    temperatura):
    """
    Resolve o problema tipo 7 da Aula 7.

    Dados conhecidos:
        D: diâmetro interno em mm
        J: perda de carga unitária em m/m
        ε: rugosidade absoluta em mm
        T: temperatura da água em °C

    Incógnitas:
        V: velocidade média em m/s
        Q: vazão em L/s

    Referência: Aula 7, páginas 23 e 29.
    """

    # 1. Convertemos os dados para o Sistema Internacional.
    diametro = mm_para_m(diametro_mm)
    rugosidade = mm_para_m(rugosidade_mm)

    # 2. Calculamos a viscosidade cinemática da água.
    viscosidade = viscosidade_agua(temperatura)

    # 3. Verificamos se os dados hidráulicos são válidos.
    if diametro <= 0 or perda_unitaria <= 0 or rugosidade < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    # 4. Calculamos a expressão auxiliar sqrt(2*g*J*D).
    # Ela aparece na equação explícita do problema tipo 7.
    auxiliar = math.sqrt(
        2 * GRAVIDADE * perda_unitaria * diametro
    )

    # 5. Calculamos os dois termos dentro do logaritmo.
    termo_rugosidade = rugosidade / (3.71 * diametro)

    termo_viscosidade = (
        2.51 * viscosidade / (diametro * auxiliar)
    )

    # 6. Aplicamos a equação do tipo 7, apresentada
    # na página 23 da aula, para obter a velocidade.
    velocidade_media = (
        -2 * auxiliar
        * math.log10(termo_rugosidade + termo_viscosidade)
    )

    # 7. Pela continuidade, calculamos a vazão em m³/s.
    vazao_m3s = area_conduto(diametro) * velocidade_media

    # 8. Convertemos a vazão de m³/s para L/s.
    vazao_ls = vazao_m3s * 1000

    # 9. Retornamos os dois resultados para o programa.
    return velocidade_media, vazao_ls

# ============================================================
# 8. PROBLEMA TIPO 1 - DIMENSIONAMENTO
# ============================================================

def problema_tipo_1(vazao_ls, perda_unitaria, rugosidade_mm,
                    temperatura, registrar_iteracoes=False):
    """
    Resolve o problema tipo 1 da Aula 7.

    Dados conhecidos:
        Q: vazão em L/s
        J: perda de carga unitária em m/m
        ε: rugosidade absoluta em mm
        T: temperatura da água em °C

    Incógnitas:
        D: diâmetro interno em mm
        V: velocidade média em m/s

    Método:
        Tentativas sucessivas para determinar o diâmetro.

    Referência: Aula 7, páginas 21 e 27.
    """

    # 1. Verificamos se os dados fornecidos são válidos.
    if vazao_ls <= 0 or perda_unitaria <= 0 or rugosidade_mm < 0:
        raise ValueError("Os dados do conduto são inválidos.")

    # 2. Convertemos as unidades para o Sistema Internacional.
    vazao = litros_para_m3(vazao_ls)
    rugosidade = mm_para_m(rugosidade_mm)

    # 3. Calculamos a viscosidade cinemática da água.
    viscosidade = viscosidade_agua(temperatura)

    # 4. Definimos uma função auxiliar.
    # Para um diâmetro escolhido, ela calcula a perda
    # de carga unitária correspondente à vazão informada.
    def calcular_j(diametro):

        # Pela continuidade, calculamos a velocidade.
        velocidade_media = velocidade(vazao, diametro)

        # Calculamos o número de Reynolds.
        re = reynolds(
            velocidade_media, diametro, viscosidade
        )

        # Determinamos o fator de atrito.
        f = fator_atrito(re, diametro, rugosidade)

        # Calculamos J pela equação de Darcy-Weisbach.
        return perda_carga_unitaria(
            f, velocidade_media, diametro
        )

    # 5. Estabelecemos os limites iniciais de busca.
    # O diâmetro procurado deve produzir o J informado.
    diametro_minimo = 0.001
    diametro_maximo = 10.0

    # Verificamos se a solução está dentro dos limites.
    if not (
        calcular_j(diametro_minimo) >= perda_unitaria
        and calcular_j(diametro_maximo) <= perda_unitaria
    ):
        raise ValueError(
            "Não foi possível encontrar o diâmetro "
            "dentro dos limites de cálculo."
        )
    # Lista que armazenará as tentativas do dimensionamento.
    # Cada registro contém o diâmetro, J calculado e o erro.
    historico_iteracoes = []
    # 6. Aplicamos o método da bisseção.
    #
    # A cada tentativa, testamos o diâmetro intermediário
    # e comparamos a perda calculada com a perda desejada.
    for _ in range(200):

        diametro = (
            diametro_minimo + diametro_maximo
        ) / 2

        j_calculado = calcular_j(diametro)
        # Calculamos o erro relativo da perda de carga.
        erro_percentual = (
            abs(j_calculado - perda_unitaria)
            / perda_unitaria
        ) * 100

        # Guardamos os resultados desta tentativa.
        historico_iteracoes.append({
            "iteracao": len(historico_iteracoes) + 1,
            "diametro_mm": diametro * 1000,
            "j_calculado": j_calculado,
            "erro_percentual": erro_percentual,
        })
        # Se J calculado for maior que o desejado,
        # precisamos aumentar o diâmetro.
        if j_calculado > perda_unitaria:
            diametro_minimo = diametro

        # Caso contrário, diminuímos o diâmetro.
        else:
            diametro_maximo = diametro

        # Encerramos quando a diferença entre os
        # limites for menor que 0,000000001 metro.
        if diametro_maximo - diametro_minimo < 1e-9:
            break

    # 7. Calculamos o diâmetro final pela média
    # dos dois limites encontrados.
    diametro = (
        diametro_minimo + diametro_maximo
    ) / 2

    # 8. Calculamos a velocidade correspondente.
    velocidade_media = velocidade(vazao, diametro)

    # 9. Convertemos o diâmetro de metros para mm.
    diametro_mm = diametro * 1000

    # 10. Retornamos os resultados.
        # Quando solicitado, retornamos também as iterações
    # para apresentar no memorial de cálculo.
    if registrar_iteracoes:
        return diametro_mm, velocidade_media, historico_iteracoes

    # Mantemos o retorno original para não afetar
    # os testes e outras partes do programa.
    return diametro_mm, velocidade_media