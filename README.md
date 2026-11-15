# Hidráulica: Dimensionamento de Condutos

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição
A ferramenta resolve oito tipos de problemas de dimensionamento, verificação e determinação da rugosidade de condutos sob pressão, conforme a tabela de casos implementados.

O programa considera dois reservatórios interligados por um conduto circular cheio, com perdas de carga distribuídas. A partir dos dados fornecidos pelo usuário, identifica o tipo de problema, calcula as incógnitas e apresenta os resultados e o memorial de cálculo no terminal.
## Instalação

O programa funciona pelo terminal e usa apenas a biblioteca padrão do Python.

### Requisitos

- Python 3.11, 3.12 ou 3.13.
- Sistema operacional Windows, Linux ou macOS.

### Procedimento

1. Acesse o repositório no GitHub.
2. Clique em **Code → Download ZIP**.
3. Extraia os arquivos para uma pasta.
4. Abra o terminal na pasta principal do projeto.
5. Execute:

```bash
python executar_terminal.py
```

Em sistemas que utilizam o comando `python3`, execute:

```bash
python3 executar_terminal.py
```

Após exibir o resultado e o memorial, o programa aguarda mais um **Enter** para sair quando aberto em um terminal interativo.

## Uso

O usuário deverá inserir os dados disponíveis do problema, deixando em branco os campos correspondentes às incógnitas.

O programa identifica automaticamente o tipo de problema e executa os cálculos disponíveis.

### Dados de entrada

- Vazão (Q), em L/s;
- Velocidade (V), em m/s;
- Diâmetro (D), em mm;
- Rugosidade absoluta (ε), em mm;
- Perda de carga unitária (J), em m/m;
- Temperatura da água, em °C.

A perda de carga unitária também poderá ser calculada a partir do comprimento da tubulação e das cotas dos reservatórios.

### Problemas implementados

| Tipo | Categoria | Dados conhecidos | Grandezas calculadas |
| --- | --- | --- | --- |
| 1 | Dimensionamento | Q, J, ε | D, V |
| 2 | Dimensionamento | V, ε, Q | D, J |
| 3 | Rugosidade | V, J, Q | ε, D |
| 4 | Dimensionamento | V, J, ε | D, Q |
| 5 | Verificação | D, Q, ε | V, J |
| 6 | Rugosidade | Q, D, J | ε, V |
| 7 | Verificação | D, J, ε | V, Q |
| 10 | Rugosidade | V, D, J | ε, Q |

Informe a temperatura da água nos oito casos. Os tipos 1 e 4 usam bisseção quando há busca de diâmetro, com intervalo final de até 0,1 mm. Os tipos 3, 6 e 10 determinam a rugosidade pela equação de Colebrook-White para escoamento turbulento.

O arquivo [Casos de uso](exemplos/casos_de_uso.md) apresenta um exercício para cada categoria.

### Resultados

O terminal apresenta os resultados e o memorial de cálculo com os dados de entrada, as conversões de unidades, as equações com substituição numérica e os valores intermediários. Quando há bisseção, o memorial registra as tentativas e o intervalo final. Se J vier das cotas, o memorial registra também o desnível e o comprimento.

Para gravar o memorial em um arquivo de texto UTF-8, execute o programa com a opção `--memorial` e informe um nome novo.

```bash
python executar_terminal.py --memorial memorial_tipo_10.txt
```

Se a combinação de dados não corresponder aos casos implementados ou o cálculo indicar dados incompatíveis, o programa apresenta uma mensagem no terminal.

## Testes

Os testes automatizados estão localizados no diretório [`tests/`](tests/).

O projeto utiliza **Pytest** para verificar o funcionamento dos cálculos hidráulicos e das rotinas de entrada e identificação dos problemas.

Para instalar o projeto e a ferramenta de testes, execute na pasta principal:

```bash
python -m pip install -e . "pytest>=8,<9"
```

Em seguida, execute:

```bash
python -m pytest -v
```

### Verificação automática

O projeto usa **GitHub Actions** para executar as verificações em Linux e Windows:

1. Verificação da sintaxe dos arquivos Python;
2. Instalação das dependências necessárias aos testes;
3. Testes dos cálculos hidráulicos;
4. Testes de identificação automática dos problemas;
5. Testes de entrada de dados e execução pelo terminal.

Essa verificação permite detectar possíveis falhas após modificações no código.

A suíte cobre os oito tipos implementados, as equações exibidas no memorial, a exportação para texto e casos de entrada inválida. O GitHub registra o resultado de cada execução na aba **Actions**.

## Estrutura do projeto

```text
.
├── .github/
│   └── workflows/
│       └── verificacao.yml
├── src/
│   └── hidraulica_condutos/
│       ├── __init__.py
│       ├── calculos.py
│       └── main.py
├── tests/
│   ├── test_calculos.py
│   ├── test_demais_tipos.py
│   ├── test_main.py
│   ├── test_memorial.py
│   └── test_terminal.py
├── exemplos/
│   └── casos_de_uso.md
├── docs/
├── executar_terminal.py
├── README.md
├── LICENSE
├── poetry.lock
└── pyproject.toml
```

### Principais arquivos

- `calculos.py`: implementação das equações e rotinas hidráulicas.
- `main.py`: entrada de dados, identificação dos problemas e apresentação dos resultados pelo terminal.
- `executar_terminal.py`: inicializador do programa pelo terminal.
- `tests/`: testes automatizados.
- `verificacao.yml`: configuração dos testes automáticos no GitHub.

## Desenvolvimento

O desenvolvimento do projeto priorizou a criação de uma ferramenta computacional capaz de automatizar a resolução dos problemas de Hidráulica, identificando as incógnitas e aplicando as equações adequadas para cada situação.

Para isso, são utilizadas as equações da continuidade, Darcy-Weisbach e Colebrook-White, além de relações para a viscosidade cinemática e o número de Reynolds.

O desenvolvimento inicial contemplou os tipos 1 e 7, validados com exercícios resolvidos na disciplina. Os testes dos tipos 2, 3, 4, 5, 6 e 10 reorganizam os dados do exemplo de verificação para conferir se cada rotina recupera as grandezas esperadas.

Posteriormente, o programa foi adaptado para permitir uma execução simplificada pelo terminal, reduzindo as dependências necessárias para sua utilização.

Também foram implementados testes automatizados para facilitar futuras modificações e ampliações do código.

O escopo futuro inclui sistemas hidráulicos mais complexos.

## Autores

**Alunos**

- Diana Pereira Couto (2026/2)
- Lucas da Silva Balensiefer (2026/2)

**Professores orientadores**

- Felipe Pinto da Motta Quevedo
- Felipe Schaedler de Almeida

## Referências

Os arquivos utilizados como apoio para o desenvolvimento do projeto foram os slides e materiais de aula da professora Ana e do professor Manica.

## Licença

Este projeto está distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE).
