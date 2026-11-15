# Hidráulica: Dimensionamento de Condutos

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição

O objetivo do projeto é permitir uma resolução mais rápida e proporcionar uma melhor visualização de problemas relacionados ao dimensionamento e à análise de condutos.

A ferramenta computacional tem como objetivo automatizar a resolução dos nove tipos de problemas básicos abordados na disciplina de Hidráulica, considerando inicialmente um sistema composto por dois reservatórios interligados por um conduto.

A partir das variáveis fornecidas pelo usuário, o programa identifica as incógnitas e aplica os procedimentos de cálculo correspondentes.

Atualmente, estão implementados os problemas dos tipos 1 e 7. As demais rotinas fazem parte das próximas etapas de desenvolvimento.

## Instalação

A versão principal do programa funciona pelo terminal, utilizando Python, sem necessidade de instalar Poetry ou bibliotecas externas.

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

O programa será iniciado diretamente pelo terminal.

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

**Tipo 1 — Dimensionamento**

Dados conhecidos: Q, J e ε.

Incógnitas: D e V.

O programa determina o diâmetro por meio de um procedimento iterativo e calcula a velocidade correspondente.

**Tipo 7 — Verificação**

Dados conhecidos: D, J e ε.

Incógnitas: V e Q.

O programa determina a velocidade e a vazão do escoamento.

### Resultados

Os resultados numéricos são apresentados diretamente no terminal, acompanhados de suas unidades.

O programa também identifica outras combinações de dados, informando quando a rotina correspondente ainda não está implementada.

A interface gráfica desenvolvida anteriormente permanece disponível como alternativa, permitindo visualizar o sistema hidráulico e o memorial de cálculo dos tipos implementados.

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

O projeto também utiliza **GitHub Actions** para executar automaticamente:

1. Verificação da sintaxe dos arquivos Python;
2. Instalação das dependências necessárias aos testes;
3. Testes dos cálculos hidráulicos;
4. Testes de identificação automática dos problemas;
5. Testes de entrada de dados e execução pelo terminal.

Essa verificação permite detectar possíveis falhas após modificações no código.

Na última execução validada, **18 testes automatizados foram aprovados**.

A aprovação dos testes indica que as funcionalidades verificadas continuam apresentando os resultados esperados, mas não substitui uma validação completa de todas as situações hidráulicas possíveis.

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
│       ├── interface.py
│       └── main.py
├── tests/
│   ├── test_calculos.py
│   ├── test_main.py
│   └── test_terminal.py
├── exemplos/
├── docs/
├── executar.py
├── executar_terminal.py
├── README.md
├── LICENSE
├── poetry.lock
└── pyproject.toml
```

### Principais arquivos

- `calculos.py`: implementação das equações e rotinas hidráulicas.
- `main.py`: entrada de dados, identificação dos problemas e apresentação dos resultados pelo terminal.
- `interface.py`: interface gráfica opcional.
- `executar_terminal.py`: inicializador da versão simplificada.
- `executar.py`: inicializador da interface gráfica.
- `tests/`: testes automatizados.
- `verificacao.yml`: configuração dos testes automáticos no GitHub.

## Desenvolvimento

O desenvolvimento do projeto priorizou a criação de uma ferramenta computacional capaz de automatizar a resolução dos problemas de Hidráulica, identificando as incógnitas e aplicando as equações adequadas para cada situação.

Para isso, são utilizadas as equações da continuidade, Darcy-Weisbach e Colebrook-White, além de relações para a viscosidade cinemática e o número de Reynolds.

O desenvolvimento inicial contemplou os tipos 1 e 7, permitindo validar os cálculos com exercícios resolvidos na disciplina.

Posteriormente, o programa foi adaptado para permitir uma execução simplificada pelo terminal, reduzindo as dependências necessárias para sua utilização.

Também foram implementados testes automatizados para facilitar futuras modificações e ampliações do código.

O objetivo futuro permanece sendo a implementação dos demais tipos de problemas e a possibilidade de ampliação para sistemas hidráulicos mais complexos.

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