
"""
Interface gráfica para o cálculo de condutos forçados.

O programa utiliza Tkinter para criar a janela e aproveita
as rotinas hidráulicas existentes no arquivo calculos.py.

Tipos implementados:
    Tipo 1: Q, J e rugosidade conhecidos.
    Tipo 7: D, J e rugosidade conhecidos.
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox

from hidraulica_condutos.calculos import (
    problema_tipo_1,
    problema_tipo_7,
    viscosidade_agua,
    mm_para_m,
    litros_para_m3,
    reynolds,
    fator_atrito,
    GRAVIDADE,
)


class InterfaceCondutos:
    """Controla os campos, cálculos, desenho e memorial."""

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Dimensionamento de Condutos Forçados")
        self.janela.geometry("1120x780")
        self.janela.minsize(900, 650)

        # Guardamos os campos para consultar os valores digitados.
        self.campos = {}

        # Criamos a estrutura visual da janela.
        self.criar_interface()

    def criar_interface(self):
        """Monta todos os componentes da interface gráfica."""

        # Título principal.
        titulo = ttk.Label(
            self.janela,
            text="CÁLCULO DE CONDUTOS FORÇADOS",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=(15, 5))

        subtitulo = ttk.Label(
            self.janela,
            text="Sistema entre dois reservatórios — Tipos 1 e 7",
        )
        subtitulo.pack(pady=(0, 15))

        # Dividimos a janela em dois lados.
        conteudo = ttk.Frame(self.janela, padding=12)
        conteudo.pack(fill="both", expand=True)

        esquerda = ttk.Frame(conteudo)
        esquerda.pack(side="left", fill="y", padx=(0, 15))

        direita = ttk.Frame(conteudo)
        direita.pack(side="left", fill="both", expand=True)

        # Área de entrada dos dados.
        entrada = ttk.LabelFrame(
            esquerda, text="Dados de entrada", padding=12
        )
        entrada.pack(fill="x")

        self.adicionar_campo(entrada, "Q", "Vazão Q (L/s)")
        self.adicionar_campo(entrada, "V", "Velocidade V (m/s)")
        self.adicionar_campo(entrada, "D", "Diâmetro D (mm)")
        self.adicionar_campo(entrada, "e", "Rugosidade ε (mm)")
        self.adicionar_campo(entrada, "T", "Temperatura (°C)")
        self.adicionar_campo(entrada, "L", "Comprimento L (m)")
        self.adicionar_campo(entrada, "z1", "Cota reservatório 1 (m)")
        self.adicionar_campo(entrada, "z2", "Cota reservatório 2 (m)")

        # Também permitimos informar J diretamente.
        self.adicionar_campo(entrada, "J", "Perda unitária J (m/m)")

        orientacao = ttk.Label(
            entrada,
            text=(
                "Deixe Q ou D em branco, conforme a incógnita.\n"
                "Informe J diretamente OU L e as duas cotas.\n"
                "A temperatura e a rugosidade são obrigatórias."
            ),
            justify="left",
            wraplength=290,
        )
        orientacao.pack(pady=10)

        # Botão que executa o cálculo.
        botao = ttk.Button(
            entrada,
            text="CALCULAR",
            command=self.calcular,
        )
        botao.pack(fill="x", pady=8)

        # Botão para limpar os campos e resultados.
        limpar = ttk.Button(
            entrada,
            text="LIMPAR",
            command=self.limpar,
        )
        limpar.pack(fill="x")

        # Área dos resultados.
        resultados = ttk.LabelFrame(
            esquerda, text="Resultados", padding=12
        )
        resultados.pack(fill="x", pady=12)

        self.texto_resultados = ttk.Label(
            resultados,
            text="Preencha os dados e clique em CALCULAR.",
            justify="left",
            wraplength=290,
        )
        self.texto_resultados.pack(anchor="w")

        # Área do esquema hidráulico.
        esquema = ttk.LabelFrame(
            direita, text="Esquema hidráulico", padding=8
        )
        esquema.pack(fill="x")

        self.desenho = tk.Canvas(
            esquema,
            height=250,
            background="white",
            highlightthickness=0,
        )
        self.desenho.pack(fill="x")
        self.desenhar_reservatorios()   
        # Botão para copiar o memorial.
        copiar = ttk.Button(
            direita,
            text="COPIAR MEMORIAL",
            command=self.copiar_memorial,
        )
        copiar.pack(
            side="top",
            anchor="e",
            pady=(8, 4),
        )
        # Área do memorial de cálculo.
        memorial_frame = ttk.LabelFrame(
            direita, text="Memorial de cálculo", padding=8
        )
        memorial_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.memorial = tk.Text(
            memorial_frame,
            wrap="word",
            font=("Consolas", 10),
            height=15,
        )
        self.memorial.pack(
            side="left", fill="both", expand=True
        )

        # Barra de rolagem do memorial.
        rolagem = ttk.Scrollbar(
            memorial_frame,
            orient="vertical",
            command=self.memorial.yview,
        )
        rolagem.pack(side="right", fill="y")
        self.memorial.configure(yscrollcommand=rolagem.set)



    def adicionar_campo(self, quadro, chave, descricao):
        """Cria um campo de entrada e o registra pelo nome."""

        linha = ttk.Frame(quadro)
        linha.pack(fill="x", pady=4)

        ttk.Label(
            linha,
            text=descricao,
            width=24,
        ).pack(side="left")

        entrada = ttk.Entry(linha, width=15)
        entrada.pack(side="right")

        self.campos[chave] = entrada

    def ler_valor(self, chave):
        """Lê um número, aceitando ponto ou vírgula decimal."""

        texto = self.campos[chave].get().strip()

        # Campo vazio representa uma grandeza desconhecida.
        if not texto:
            return None

        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            raise ValueError(
                f"Valor inválido no campo {chave}: {texto}"
            )

        # Evitamos valores infinitos e NaN.
        if not math.isfinite(valor):
            raise ValueError(
                f"O campo {chave} precisa ter um valor finito."
            )

        return valor

    def calcular(self):
        """Identifica o problema e executa a rotina hidráulica."""

        try:
            # Lemos todos os campos da janela.
            dados = {
                chave: self.ler_valor(chave)
                for chave in self.campos
            }

            temperatura = dados["T"]
            rugosidade = dados["e"]

            if temperatura is None or rugosidade is None:
                raise ValueError(
                    "Informe a temperatura e a rugosidade."
                )

            if rugosidade < 0:
                raise ValueError(
                    "A rugosidade não pode ser negativa."
                )

            # J pode ser informado diretamente ou calculado
            # pela diferença de cotas dos reservatórios.
            j = dados["J"]
            comprimento = dados["L"]
            z1 = dados["z1"]
            z2 = dados["z2"]

            if j is None:
                if None in (comprimento, z1, z2):
                    raise ValueError(
                        "Informe J ou preencha L, z1 e z2."
                    )

                if comprimento <= 0 or z1 <= z2:
                    raise ValueError(
                        "É necessário L > 0 e z1 > z2."
                    )

                j = (z1 - z2) / comprimento

            if j <= 0:
                raise ValueError(
                    "A perda unitária J deve ser positiva."
                )

            # Por enquanto, trabalhamos apenas com os tipos
            # 1 e 7, que já possuem rotinas validadas.
            vazao = dados["Q"]
            velocidade_informada = dados["V"]
            diametro = dados["D"]

            if velocidade_informada is not None:
                raise ValueError(
                    "Nesta versão, deixe V em branco. "
                    "Os tipos 1 e 7 calculam a velocidade."
                )

            if vazao is not None and diametro is None:
                tipo = 1

                                # Solicitamos também o histórico de tentativas
                # utilizado no dimensionamento do diâmetro.
                (
                    diametro_resultado,
                    velocidade_resultado,
                    historico_iteracoes,
                ) = problema_tipo_1(
                    vazao_ls=vazao,
                    perda_unitaria=j,
                    rugosidade_mm=rugosidade,
                    temperatura=temperatura,
                    registrar_iteracoes=True,
                )

                vazao_resultado = vazao

            elif diametro is not None and vazao is None:
                tipo = 7
                # O tipo 7 utiliza uma solução direta.
                # Portanto, não possui histórico de bisseção.
                historico_iteracoes = []
                velocidade_resultado, vazao_resultado = (
                    problema_tipo_7(
                        diametro_mm=diametro,
                        perda_unitaria=j,
                        rugosidade_mm=rugosidade,
                        temperatura=temperatura,
                    )
                )

                diametro_resultado = diametro

            else:
                raise ValueError(
                    "Para o tipo 1, informe Q e deixe D vazio.\n"
                    "Para o tipo 7, informe D e deixe Q vazio."
                )

            # Calculamos as grandezas intermediárias
            # necessárias para apresentar o memorial.
            d_metros = mm_para_m(diametro_resultado)
            q_m3s = litros_para_m3(vazao_resultado)
            viscosidade = viscosidade_agua(temperatura)

            re = reynolds(
                velocidade_resultado,
                d_metros,
                viscosidade,
            )

            f = fator_atrito(
                re,
                d_metros,
                mm_para_m(rugosidade),
            )

            # Exibimos os resultados principais.
            self.texto_resultados.config(
                text=(
                    f"Problema identificado: TIPO {tipo}\n\n"
                    f"Diâmetro: {diametro_resultado:.3f} mm\n"
                    f"Velocidade: {velocidade_resultado:.4f} m/s\n"
                    f"Vazão: {vazao_resultado:.4f} L/s\n"
                    f"Perda unitária: {j:.6f} m/m"
                )
            )

            # Geramos o memorial detalhado.
            self.gerar_memorial(
                tipo=tipo,
                dados=dados,
                j=j,
                diametro_mm=diametro_resultado,
                velocidade_media=velocidade_resultado,
                vazao_ls=vazao_resultado,
                viscosidade=viscosidade,
                re=re,
                f=f,
                q_m3s=q_m3s,                historico_iteracoes=historico_iteracoes,
            )

            # Atualizamos o esquema dos reservatórios.
            self.desenhar_reservatorios(
                z1=z1,
                z2=z2,
                comprimento=comprimento,
                vazao=vazao_resultado,
                diametro=diametro_resultado,
            )

        except (ValueError, ZeroDivisionError, OverflowError) as erro:
            messagebox.showerror("Erro no cálculo", str(erro))
    def gerar_memorial(
        self, tipo, dados, j, diametro_mm,
        velocidade_media, vazao_ls, viscosidade,
        re, f, q_m3s, historico_iteracoes
    ):
        """Monta o memorial com equações e valores calculados."""

        diametro_m = mm_para_m(diametro_mm)
        rugosidade_m = mm_para_m(dados["e"])

        area = math.pi * diametro_m**2 / 4

        # Calculamos J novamente pela equação de Darcy-Weisbach
        # para conferir o resultado obtido.
        j_verificacao = (
            f * velocidade_media**2
            / (2 * GRAVIDADE * diametro_m)
        )

        texto = f"""
MEMORIAL DE CÁLCULO — CONDUTOS FORÇADOS
=============================================

1. IDENTIFICAÇÃO DO PROBLEMA

Tipo identificado: {tipo}

Tipo 1: conhecidos Q, J e rugosidade.
Tipo 7: conhecidos D, J e rugosidade.

2. DADOS E CONVERSÃO DE UNIDADES

Temperatura da água: {dados['T']:.2f} °C
Rugosidade absoluta: {dados['e']:.4f} mm
Rugosidade em metros: {rugosidade_m:.8f} m

Vazão: {vazao_ls:.4f} L/s
Q = {q_m3s:.8f} m³/s

Diâmetro: {diametro_mm:.4f} mm
D = {diametro_m:.8f} m

Perda de carga unitária:
J = {j:.8f} m/m

3. VISCOSIDADE CINEMÁTICA

ν = 1,78 × 10⁻⁶ /
    (1 + 0,0337 T + 0,000221 T²)

ν = {viscosidade:.10f} m²/s

4. EQUAÇÃO DA CONTINUIDADE

A = π D² / 4
A = {area:.8f} m²

Q = A × V
V = Q / A

V = {velocidade_media:.6f} m/s

5. NÚMERO DE REYNOLDS

Re = V × D / ν

Re = {re:.2f}

6. FATOR DE ATRITO

Regime considerado:
{"Laminar" if re < 2000 else "Turbulento"}

Equação utilizada:
{"f = 64 / Re" if re < 2000 else "Colebrook-White"}

f = {f:.8f}

7. EQUAÇÃO DE DARCY-WEISBACH

J = f × V² / (2 × g × D)

g = {GRAVIDADE:.3f} m/s²

J calculado = {j_verificacao:.8f} m/m
J informado = {j:.8f} m/m

8. RESULTADOS FINAIS

TIPO {tipo}

Diâmetro = {diametro_mm:.3f} mm
Velocidade = {velocidade_media:.4f} m/s
Vazão = {vazao_ls:.4f} L/s

=============================================
Observação:
O tipo 1 determina o diâmetro por bisseção.
O tipo 7 utiliza a solução da equação hidráulica.
"""

        # Acrescenta todas as iterações do dimensionamento
        # quando o problema identificado é do tipo 1.
        if tipo == 1:
            texto += """

9. HISTÓRICO DO DIMENSIONAMENTO POR BISSEÇÃO

A cada tentativa, o programa calcula a perda de
carga para um diâmetro e ajusta o intervalo de busca.

Iter. | D (mm)       | J calculado   | Erro (%)
------------------------------------------------
"""

            # Percorre o histórico gerado pela função
            # problema_tipo_1, na ordem das tentativas.
            for tentativa in historico_iteracoes:
                texto += (
                    f"{tentativa['iteracao']:5d} | "
                    f"{tentativa['diametro_mm']:12.6f} | "
                    f"{tentativa['j_calculado']:.9f} | "
                    f"{tentativa['erro_percentual']:.6f}\n"
                )

            # Informa o critério utilizado para
            # encerrar as tentativas sucessivas.
            texto += (
                "\nCritério de parada: intervalo entre "
                "os limites de diâmetro menor que 10⁻⁹ m.\n"
            )

        self.memorial.delete("1.0", tk.END)
        self.memorial.insert(tk.END, texto.strip())

    def desenhar_reservatorios(
        self, z1=None, z2=None, comprimento=None,
        vazao=None, diametro=None
    ):
        """Desenha um esquema ilustrativo de dois reservatórios."""

        tela = self.desenho
        tela.delete("all")

        # Reservatório de montante.
        tela.create_rectangle(
            30, 45, 145, 155,
            outline="#334155", width=3,
        )
        tela.create_rectangle(
            32, 78, 143, 153,
            fill="#93c5fd", outline="",
        )

        # Reservatório de jusante.
        tela.create_rectangle(
            405, 100, 520, 205,
            outline="#334155", width=3,
        )
        tela.create_rectangle(
            407, 135, 518, 203,
            fill="#93c5fd", outline="",
        )

        # Tubulação entre os reservatórios.
        tela.create_line(
            145, 145, 255, 145,
            255, 190, 405, 190,
            fill="#64748b", width=12,
            joinstyle="round",
        )
        tela.create_line(
            145, 145, 255, 145,
            255, 190, 405, 190,
            fill="#60a5fa", width=6,
            joinstyle="round",
        )

        # Seta indicando o sentido do escoamento.
        tela.create_line(
            315, 190, 355, 190,
            arrow=tk.LAST,
            fill="#1d4ed8", width=3,
        )

        tela.create_text(
            88, 25, text="Reservatório 1",
            font=("Arial", 11, "bold"),
        )
        tela.create_text(
            462, 80, text="Reservatório 2",
            font=("Arial", 11, "bold"),
        )

        # Identificação das cotas.
        if z1 is not None:
            tela.create_text(
                88, 65, text=f"z1 = {z1:g} m"
            )

        if z2 is not None:
            tela.create_text(
                462, 120, text=f"z2 = {z2:g} m"
            )

        # Identificação das grandezas calculadas.
        if comprimento is not None:
            tela.create_text(
                300, 115, text=f"L = {comprimento:g} m"
            )

        if diametro is not None:
            tela.create_text(
                320, 160, text=f"D = {diametro:.2f} mm"
            )

        if vazao is not None:
            tela.create_text(
                340, 215, text=f"Q = {vazao:.2f} L/s"
            )

        tela.create_text(
            275, 240,
            text="Esquema ilustrativo — sem escala",
            fill="#64748b",
        )

    def copiar_memorial(self):
        """Copia o memorial para a área de transferência."""

        texto = self.memorial.get("1.0", tk.END).strip()

        if not texto:
            messagebox.showinfo(
                "Memorial",
                "Realize um cálculo antes de copiar."
            )
            return

        self.janela.clipboard_clear()
        self.janela.clipboard_append(texto)

        messagebox.showinfo(
            "Memorial",
            "Memorial copiado com sucesso!"
        )
    def limpar(self):
        """Apaga os dados informados e os resultados."""
        # Limpa todos os campos de entrada.
        for campo in self.campos.values():
            campo.delete(0, tk.END)

        # Restaura a mensagem inicial dos resultados.
        self.texto_resultados.config(
            text="Preencha os dados e clique em CALCULAR."
        )

        # Apaga o memorial de cálculo.
        self.memorial.delete("1.0", tk.END)

        # Redesenha os reservatórios sem valores.
        self.desenhar_reservatorios()
def main():
    """Inicia a aplicação gráfica."""

    janela = tk.Tk()
    InterfaceCondutos(janela)
    janela.mainloop()


# Este bloco permite executar a interface como módulo Python.
if __name__ == "__main__":
    main()
