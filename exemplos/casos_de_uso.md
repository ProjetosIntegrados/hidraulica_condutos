# Casos de uso

Na raiz do projeto, execute `python executar_terminal.py`. Deixe os campos indicados como **Enter** em branco. O terminal aceita vírgula ou ponto decimal.

| Campo | Dimensionamento, tipo 1 | Verificação, tipo 7 | Rugosidade, tipo 10 |
| --- | ---: | ---: | ---: |
| Vazão Q (L/s) | 47,1 | Enter | Enter |
| Velocidade V (m/s) | Enter | Enter | 1,419950794 |
| Diâmetro D (mm) | Enter | 184 | 184 |
| Rugosidade ε (mm) | 0,06 | 0,5 | Enter |
| Opção para J | 2 | 2 | 2 |
| Comprimento L (m) | 1104 | 1104 | 1104 |
| Cota do reservatório 1 (m) | 84 | 84 | 84 |
| Cota do reservatório 2 (m) | 68 | 68 | 68 |
| Temperatura da água (°C) | 25 | 25 | 25 |

| Resultado | Valores esperados |
| --- | --- |
| Tipo 1 | D = 184,4 mm e V = 1,7631 m/s |
| Tipo 7 | V = 1,4200 m/s e Q = 37,7571 L/s |
| Tipo 10 | ε ≈ 0,5 mm e Q = 37,7571 L/s |

Os tipos 1 e 7 correspondem aos exemplos 2 e 3 da Aula 7. O tipo 10 usa os dados do exemplo 3 para recuperar a rugosidade conhecida. A suíte de testes também cobre os tipos 2, 3, 4, 5 e 6.
