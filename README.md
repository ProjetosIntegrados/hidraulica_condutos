# Hidráulica: dimensionamento de condutos

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição

O objetivo do projeto será permitir uma resolução mais rápida e proporcionar uma melhor visualização de problemas relacionados ao dimensionamento e à análise de condutos. A ferramenta computacional será capaz de automatizar a resolução dos nove tipos de problemas básicos abordados na disciplina de Hidráulica, considerando inicialmente um sistema composto por dois reservatórios interligados por um conduto. A partir das variáveis fornecidas pelo usuário, o programa deverá identificar as incógnitas e realizar os procedimentos necessários para sua determinação.

## Instalação

Descreva os requisitos e os procedimentos necessários para instalar o projeto.

Por exemplo:

```bash
poetry install
install matplotlib
````

## Uso

O usuário deverá inserir os dados disponíveis do problema, e o programa será responsável por identificar o tipo de problema, determinar as incógnitas e realizar os cálculos necessários. Ao final, a ferramenta deverá apresentar o memorial de cálculo, os resultados obtidos e uma representação visual do sistema analisado.

```python
# Exemplo de uso
```

## Testes

Os testes automatizados estão no diretório [`tests/`](tests/).

Para executá-los:

```bash
poetry run pytest
```

## Estrutura do projeto

```text
.
├── src/
│   └── hidraulica_condutos/
│       ├── __init__.py/        
│       ├── calculos.py/         #Adiciona interface gráfica e memorial de cálculo
│       ├── interface.py/        #Interface para inserção de dados
│       └── main.py/             #Implementa cálculos hidráulicos dos tipos 1 e 7
├── tests/
│   └── test_calculos.py         #Testes automatizados conforme exemplos de aula
├── exemplos/
├── docs/
├── README.md
├── LICENSE
└── pyproject.toml
```

## Desenvolvimento

O desenvolvimento do projeto priorizou a criação de uma ferramenta computacional capaz de automatizar a resolução dos nove tipos de problemas de hidráulica, identificando as incógnitas e aplicando as equações adequadas para cada situação. Para isso, é necessário implementar os métodos de cálculo, incluindo processos iterativos, validação dos dados de entrada e apresentação dos resultados por meio de um memorial de cálculo e de uma representação visual do sistema hidráulico. Além disso, a ferramenta possuirá uma interface intuitiva e didática, adequada aos estudantes de Engenharia Civil, e uma estrutura modular que facilite futuras modificações e ampliações para a análise de sistemas hidráulicos mais complexos.

## Autores

**Alunos**

* Diana Pereira Couto (2026/2)
* Lucas da Silva Balensiefer (2026/2)

**Professores orientadores**

* Felipe Pinto da Motta Quevedo
* Felipe Schaedler de Almeida

## Referências

Os arquivos utilizados de apoio para o desenvolvimento do projeto foram os slides e material de aula da professora Ana e do professor Manica.

## Licença

Este projeto está distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE).

```



