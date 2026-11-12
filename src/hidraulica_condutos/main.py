
# ============================================================
# PROJETO: CÁLCULO DE CONDUTOS SOB PRESSÃO
# MÓDULO: INTERFACE PRINCIPAL
#
# Recebe os dados do usuário, identifica automaticamente
# o tipo de problema e executa a rotina disponível.
# ============================================================

# Importamos as rotinas hidráulicas implementadas.
from hidraulica_condutos.calculos import (
    problema_tipo_1,
    problema_tipo_7,
)

def ler_numero(mensagem):
    """
    Solicita um número ao usuário.

    Se o campo ficar vazio, retorna None, indicando
    que a grandeza é desconhecida.

    Aceita tanto vírgula quanto ponto decimal.
    """
    while True:
        texto = input(mensagem).strip()

        if texto == "":
            return None

        try:
            return float(texto.replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número ou ENTER.")


# Combinações de dados conhecidas na Aula 7.
# Cada conjunto representa um tipo de problema.
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


def identificar_tipo(dados):
    """
    Identifica o problema a partir das grandezas preenchidas.

    As grandezas desconhecidas possuem valor None.
    """
    conhecidos = frozenset(
        nome for nome, valor in dados.items()
        if valor is not None
    )

    return TIPOS.get(conhecidos)


def obter_perda_unitaria():
    """
    Permite informar J diretamente ou calculá-lo
    a partir das cotas dos reservatórios e do comprimento.
    """
    print("\nPERDA DE CARGA")
    print("1 - Informar J diretamente")
    print("2 - Calcular J pelas cotas dos reservatórios")
    print("ENTER - Não informar J")

    while True:
        opcao = input("Escolha: ").strip()

        if opcao == "":
            return None

        if opcao == "1":
            return ler_numero("J (m/m): ")

        if opcao == "2":
            comprimento = ler_numero("Comprimento L (m): ")
            cota_1 = ler_numero("Cota do reservatório 1 (m): ")
            cota_2 = ler_numero("Cota do reservatório 2 (m): ")

            if None in (comprimento, cota_1, cota_2):
                print("Preencha os três valores.")
                continue

            if comprimento <= 0 or cota_1 <= cota_2:
                print("Informe L > 0 e cota 1 > cota 2.")
                continue

            # Para os reservatórios da proposta:
            # hp = z1 - z2 e J = hp / L.
            perda = (cota_1 - cota_2) / comprimento

            print(f"Perda de carga unitária: {perda:.6f} m/m")
            return perda

        print("Escolha 1, 2 ou pressione ENTER.")


def main():
    """Executa a interface principal do programa."""

    print("=" * 48)
    print("       CÁLCULO DE CONDUTOS SOB PRESSÃO")
    print("=" * 48)
    print("\nInforme os dados conhecidos.")
    print("Deixe em branco as grandezas desconhecidas.\n")

    # Dados fornecidos pelo usuário.
    # As unidades são convertidas nas funções de cálculo.
    dados = {
        "Q": ler_numero("Vazão Q (L/s): "),
        "V": ler_numero("Velocidade V (m/s): "),
        "D": ler_numero("Diâmetro D (mm): "),
        "e": ler_numero("Rugosidade ε (mm): "),
        "J": obter_perda_unitaria(),
    }

    # A temperatura é necessária para calcular a
    # viscosidade cinemática da água.
    temperatura = ler_numero("\nTemperatura da água (°C): ")

    if temperatura is None:
        print("É necessário informar a temperatura.")
        return

    # Identificação automática pela combinação de dados.
    tipo = identificar_tipo(dados)

    if tipo is None:
        print("\nCombinação de dados não reconhecida.")
        print("Confira as grandezas informadas.")
        return

    print(f"\nProblema identificado: TIPO {tipo}")

      # Executamos a rotina correspondente ao tipo identificado.
    if tipo == 1:
        try:
            # O tipo 1 recebe Q, J e rugosidade.
            # O resultado contém diâmetro e velocidade.
            diametro, velocidade_media = problema_tipo_1(
                vazao_ls=dados["Q"],
                perda_unitaria=dados["J"],
                rugosidade_mm=dados["e"],
                temperatura=temperatura,
            )

            print("\nRESULTADOS")
            print(f"Diâmetro: {diametro:.3f} mm")
            print(f"Velocidade: {velocidade_media:.4f} m/s")

        except (ValueError, ZeroDivisionError, OverflowError) as erro:
            print(f"\nErro no cálculo: {erro}")

    elif tipo == 7:
        try:
            velocidade, vazao = problema_tipo_7(
                diametro_mm=dados["D"],
                perda_unitaria=dados["J"],
                rugosidade_mm=dados["e"],
                temperatura=temperatura,
            )

            print("\nRESULTADOS")
            print(f"Velocidade: {velocidade:.4f} m/s")
            print(f"Vazão: {vazao:.4f} L/s")

        except (ValueError, ZeroDivisionError, OverflowError) as erro:
            print(f"\nErro no cálculo: {erro}")

    else:
        print("Este tipo foi identificado corretamente,")
        print("mas sua rotina de cálculo ainda será implementada.")


# Executa a função main somente quando este arquivo
# é iniciado diretamente como módulo principal.
if __name__ == "__main__":
    main()
