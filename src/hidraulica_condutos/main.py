"""Programa de cálculo de condutos sob pressão pelo terminal."""

import math
from pathlib import Path

from hidraulica_condutos.calculos import (
    litros_para_m3,
    mm_para_m,
    problema_tipo_1,
    problema_tipo_2,
    problema_tipo_3,
    problema_tipo_4,
    problema_tipo_5,
    problema_tipo_6,
    problema_tipo_7,
    problema_tipo_10,
    viscosidade_agua,
)


FORMATOS = {
    "D": "Diâmetro: {:.1f} mm",
    "V": "Velocidade: {:.4f} m/s",
    "Q": "Vazão: {:.4f} L/s",
    "J": "Perda de carga unitária: {:.8g} m/m",
    "e": "Rugosidade: {:.6g} mm",
}
# Para cada caso, os dados e os resultados seguem a ordem da função de cálculo.
CASOS = {
    1: (("Q", "J", "e"), ("D", "V"), problema_tipo_1),
    2: (("V", "e", "Q"), ("D", "J"), problema_tipo_2),
    3: (("V", "J", "Q"), ("e", "D"), problema_tipo_3),
    4: (("V", "J", "e"), ("D", "Q"), problema_tipo_4),
    5: (("D", "Q", "e"), ("V", "J"), problema_tipo_5),
    6: (("Q", "D", "J"), ("e", "V"), problema_tipo_6),
    7: (("D", "J", "e"), ("V", "Q"), problema_tipo_7),
    10: (("V", "D", "J"), ("e", "Q"), problema_tipo_10),
}
TIPOS = {frozenset(caso[0]): tipo for tipo, caso in CASOS.items()}


def ler_numero(mensagem):
    """Lê números com ponto ou vírgula; ENTER significa desconhecido."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")

        if not texto:
            return None

        try:
            numero = float(texto)
            if math.isfinite(numero):
                return numero
        except ValueError:
            pass

        print("Valor inválido. Digite um número ou ENTER.")


def identificar_tipo(dados):
    """Identifica o problema pelas grandezas preenchidas."""
    conhecidos = frozenset(chave for chave, valor in dados.items() if valor is not None)
    return TIPOS.get(conhecidos)


def obter_perda_unitaria(memorial=None):
    """Lê J diretamente ou calcula J pela diferença de cotas."""
    print("\nPERDA DE CARGA")
    print("1 - Informar J")
    print("2 - Calcular pelas cotas dos reservatórios")
    print("ENTER - J desconhecido")

    while True:
        escolha = input("Escolha: ").strip()

        if not escolha:
            return None

        if escolha == "1":
            j = ler_numero("J (m/m): ")
            if j is not None and memorial is not None:
                memorial.append(f"J informado diretamente = {j:.10g} m/m")
            return j

        if escolha != "2":
            print("Escolha 1, 2 ou ENTER.")
            continue

        comprimento = ler_numero("Comprimento L (m): ")
        z1 = ler_numero("Cota do reservatório 1 (m): ")
        z2 = ler_numero("Cota do reservatório 2 (m): ")
        if None in (comprimento, z1, z2):
            print("Informe comprimento e as duas cotas.")
        elif comprimento <= 0 or z1 <= z2:
            print("É necessário L > 0 e z1 > z2.")
        else:
            desnivel = z1 - z2
            j = desnivel / comprimento
            if not math.isfinite(j) or j <= 0:
                print("A perda unitária está fora do intervalo numérico. Confira os dados.")
                continue
            if memorial is not None:
                memorial.extend([
                    f"h_p = z₁ − z₂ = {z1:.10g} − ({z2:.10g}) = {desnivel:.10g} m",
                    f"J = h_p/L = {desnivel:.10g}/{comprimento:.10g} = {j:.10g} m/m",
                ])
            print(f"Perda de carga unitária: {j:.6f} m/m")
            return j


def main(arquivo_memorial=None):
    """Recebe os dados, identifica o tipo e apresenta o resultado."""
    print("\n=== CÁLCULO DE CONDUTOS SOB PRESSÃO ===")
    print("Informe os dados conhecidos. ENTER = desconhecido.\n")

    etapas_perda = []
    dados = {
        "Q": ler_numero("Vazão Q (L/s): "),
        "V": ler_numero("Velocidade V (m/s): "),
        "D": ler_numero("Diâmetro D (mm): "),
        "e": ler_numero("Rugosidade ε (mm): "),
        "J": obter_perda_unitaria(etapas_perda),
    }

    temperatura = ler_numero("\nTemperatura da água (°C): ")

    if temperatura is None:
        print("É necessário informar a temperatura.")
        return

    tipo = identificar_tipo(dados)

    if tipo is None:
        print("\nCombinação de dados não reconhecida.")
        return

    print(f"\nProblema identificado: TIPO {tipo}")

    entradas, saidas, calcular = CASOS[tipo]
    valores_entrada = [dados[chave] for chave in entradas]
    etapas = []
    try:
        viscosidade = viscosidade_agua(temperatura)
        valores_saida = calcular(*valores_entrada, temperatura, memorial=etapas)
        if not all(map(math.isfinite, valores_saida)):
            raise ValueError("Os resultados excedem o limite numérico. Confira os dados.")
    except (ValueError, ArithmeticError, RuntimeError) as erro:
        print(f"\nErro no cálculo: {erro}")
        return

    resultados = [
        FORMATOS[chave].format(valor)
        for chave, valor in zip(saidas, valores_saida, strict=True)
    ]
    print("\nRESULTADOS", *resultados, sep="\n")

    unidades = {"Q": "L/s", "V": "m/s", "D": "mm", "e": "mm", "J": "m/m"}
    dados_formatados = [
        f"{'ε' if chave == 'e' else chave} = {dados[chave]:.10g} {unidades[chave]}"
        for chave in entradas
    ]
    conversoes = []
    for chave, converter, unidade in (
        ("Q", litros_para_m3, "m³/s"), ("D", mm_para_m, "m"), ("e", mm_para_m, "m"),
    ):
        valor = dados[chave]
        if valor is not None:
            simbolo = "ε" if chave == "e" else chave
            conversoes.append(f"{simbolo} = {valor:.10g}/1000 = {converter(valor):.10g} {unidade}")

    memorial = "\n".join([
        "MEMORIAL DE CÁLCULO",
        f"Tipo {tipo}",
        "Dados: " + ", ".join(dados_formatados) + f", T = {temperatura:.10g} °C",
        *etapas_perda, *conversoes,
        "ν = 1,78 × 10⁻⁶/(1 + 0,0337 T + 0,000221 T²)",
        f"ν = 1,78 × 10⁻⁶/(1 + 0,0337 × {temperatura:.10g} + "
        f"0,000221 × ({temperatura:.10g})²) = {viscosidade:.10g} m²/s",
        *etapas,
        "Resultados finais", *resultados,
    ])
    print(f"\n{memorial}")
    if arquivo_memorial is not None:
        try:
            with Path(arquivo_memorial).open("x", encoding="utf-8") as arquivo:
                arquivo.write(memorial + "\n")
            print(f"\nMemorial salvo em {arquivo_memorial}.")
        except OSError as erro:
            print(f"\nNão foi possível salvar o memorial: {erro}")


if __name__ == "__main__":
    main()
