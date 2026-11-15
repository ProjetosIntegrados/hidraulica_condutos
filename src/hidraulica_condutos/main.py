"""Programa de cálculo de condutos sob pressão pelo terminal."""

import math

from hidraulica_condutos.calculos import (
    TOLERANCIA_DIAMETRO_MM,
    problema_tipo_1,
    problema_tipo_7,
)


# Combinações de grandezas conhecidas.
TIPOS = {
    frozenset(("Q", "J", "e")): 1,
    frozenset(("V", "e", "Q")): 2,
    frozenset(("V", "J", "Q")): 3,
    frozenset(("V", "J", "e")): 4,
    frozenset(("D", "Q", "e")): 5,
    frozenset(("Q", "D", "J")): 6,
    frozenset(("D", "J", "e")): 7,
    frozenset(("V", "D", "J")): 10,
}


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


def obter_perda_unitaria():
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
            return ler_numero("J (m/m): ")

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
            j = (z1 - z2) / comprimento
            print(f"Perda de carga unitária: {j:.6f} m/m")
            return j


def main():
    """Recebe os dados, identifica o tipo e apresenta o resultado."""
    print("\n=== CÁLCULO DE CONDUTOS SOB PRESSÃO ===")
    print("Informe os dados conhecidos. ENTER = desconhecido.\n")

    dados = {
        "Q": ler_numero("Vazão Q (L/s): "),
        "V": ler_numero("Velocidade V (m/s): "),
        "D": ler_numero("Diâmetro D (mm): "),
        "e": ler_numero("Rugosidade ε (mm): "),
        "J": obter_perda_unitaria(),
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

    if tipo not in (1, 7):
        print("Este tipo ainda não possui cálculo implementado.")
        return

    j, rugosidade = dados["J"], dados["e"]
    try:
        if tipo == 1:
            diametro, velocidade = problema_tipo_1(dados["Q"], j, rugosidade, temperatura)
            tolerancia = f"{TOLERANCIA_DIAMETRO_MM:g}".replace(".", ",")
            metodo = f"Diâmetro por bisseção com intervalo final de até {tolerancia} mm."
            resultados = (f"Diâmetro: {diametro:.1f} mm", f"Velocidade: {velocidade:.4f} m/s")
        else:
            velocidade, vazao = problema_tipo_7(dados["D"], j, rugosidade, temperatura)
            metodo = "Velocidade por Colebrook-White e Darcy-Weisbach. Vazão por Q = A × V."
            resultados = (f"Velocidade: {velocidade:.4f} m/s", f"Vazão: {vazao:.4f} L/s")
    except (ValueError, ZeroDivisionError, OverflowError) as erro:
        print(f"\nErro no cálculo: {erro}")
        return

    print("\nRESULTADOS", *resultados, sep="\n")
    print("\nMEMORIAL RESUMIDO")
    print(f"J utilizado: {j:.8g} m/m")
    print(metodo)


if __name__ == "__main__":
    main()
