# Instruções para criação do projeto

> **Este arquivo pertence ao template e deve ser excluído depois que a configuração inicial do projeto estiver concluída.**

## 1. Criar o repositório

Crie um novo repositório no GitHub utilizando este repositório como template.

O novo repositório será independente do template original.

## 2. Renomear o pacote Python

O template utiliza `nome_do_projeto` como nome provisório do pacote.

Renomeie:

```text
src/nome_do_projeto/
````

para o nome do seu projeto utilizando `snake_case`.

Por exemplo:

```text
src/analise_estrutural/
```

Atualize também o `pyproject.toml`:

```toml
name = "analise_estrutural"
packages = [{ include = "analise_estrutural", from = "src" }]
```

O nome do repositório no GitHub pode seguir outra convenção, como:

```text
analise-estrutural
```

## 3. Atualizar o `pyproject.toml`

Preencha as informações do projeto:

* `name`
* `version`
* `description`
* `authors`

Verifique se o nome definido em `packages` corresponde ao diretório criado em `src/`.

Não altere a restrição de versão do Python sem verificar a compatibilidade do projeto.

## 4. Configurar o ambiente

Certifique-se de ter Python compatível e Poetry instalados.

Na raiz do projeto, execute:

```bash
poetry install
```

O Poetry criará/configurará o ambiente virtual e instalará as dependências.

O arquivo `poetry.lock` será gerado para este projeto. Depois de criado, ele deve ser mantido no repositório.

## 5. Configurar o VS Code

Abra a pasta raiz do projeto no VS Code.

Selecione como interpretador Python o ambiente virtual criado pelo Poetry.

Para projetos que utilizem notebooks, selecione esse mesmo ambiente como kernel do Jupyter.

## 6. Organizar o projeto

O código principal deve ficar em:

```text
src/nome_do_projeto/
```

Os testes automatizados devem ficar em:

```text
tests/
```

Os exemplos e notebooks devem ficar em:

```text
exemplos/
```

Documentação complementar pode ficar em:

```text
docs/
```

Mantenha uma separação clara entre código, testes, exemplos e documentação.

## 7. Testes

Execute os testes com:

```bash
poetry run pytest
```

Novas funcionalidades devem, sempre que possível, ser acompanhadas de testes correspondentes.

## 8. README

Atualize o `README.md` com as informações reais do projeto.

Remova ou substitua os textos de exemplo e os placeholders.

## 9. Autores e referências

Preencha a seção `Autores` com todos os alunos (semestre da turma) e professores envolvidos.

Na seção `Referências`, registre as principais fontes técnicas utilizadas no desenvolvimento, como normas, artigos, livros e documentação de bibliotecas.

## 10. Licença

Verifique os dados presentes no arquivo `LICENSE` e substitua os placeholders pelos dados apropriados.

## 11. Verificação antes do primeiro commit

Antes do primeiro commit, verifique:

* [ ] nome do projeto atualizado;
* [ ] nome do pacote atualizado;
* [ ] `pyproject.toml` atualizado;
* [ ] autores preenchidos;
* [ ] semestre informado;
* [ ] README revisado;
* [ ] licença revisada;
* [ ] nenhum dado pessoal desnecessário incluído;

Depois de concluir a configuração, exclua:

```text
INSTRUCOES_TEMPLATE.md
```

## 12. Controle de versão

Faça commits pequenos e coerentes, com mensagens que descrevam as alterações realizadas.

Por exemplo:

```bash
git add .
git commit -m "Configura estrutura inicial do projeto"
```

Durante o desenvolvimento, procure manter cada commit associado a uma alteração ou tarefa bem definida.

```

