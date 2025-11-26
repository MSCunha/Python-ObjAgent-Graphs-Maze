# 💻 Atividade da Unidade I – Inteligência Artificial: Busca

## 👥 Autores
* Amanda Mikely Abreu Macedo
* Gabriela Torres de Queiroz
* Matheus Silva Cunha
---
## 📌 Descrição do Problema

O objetivo deste projeto é:

✔ Modelar um problema de busca em um labirinto como um grafo

✔ Implementar o algoritmo A* (A-Star) para encontrar o melhor caminho entre duas posições

✔ Apresentar a evolução da busca através de visualizações:

  * Exploração dos nós

  * Grafo de busca gerado

  * Ações relativas de movimento (esquerda, direita, frente, retorno)

  * Caminho final encontrado

O programa:

1. Gera um labirinto aleatório

2. Define automaticamente posição inicial e final

3. Executa o A* passo a passo

4. Desenha em tempo real:

 * O labirinto e os nós já visitados

 * A árvore de busca em NetworkX

 * Ações do agente (virou à esquerda, direita, etc.)

 * Exibe o caminho final quando o objetivo é encontrado

Você pode ver um curto vídeo explicativo e demonstrativo do projeto clicando [aqui](https://youtu.be/unJeexx_BUo?si=b_swa4bNMY462gD2)

---

### Estrutura do Projeto

```
Projeto/
├── agente.py             # Implementação do A*
├── grafos.py             # Construção e exibição do grafo em NetworkX
├── acoes.py              # Visualização das ações do agente
├── mazeGen.py            # Gerador de labirintos
├── main.py               # Arquivo principal para execução
├── requirements.txt      # Dependências do Python
└── README.md             # Este documento


```
---

## 🔧 Instruções de compilação e uso

### 1.Pré-requisitos
Python 3.10 ou superior

Pip instalado

### 2.Instalar dependências

No terminal do projeto, execute:
```bash
pip install -r requirements.txt
```
As principais bibliotecas utilizadas são:

 * networkx

 * numpy

 * matplotlib

### 3.Executar o Projeto
Basta rodar:
```bash
python main.py
```
Se o seu sistema abrir o Matplotlib em modo de janela interativa, você verá:

 * à direita → o labirinto e a exploração do A*

 * acima à esquerda → o grafo das escolhas

 * abaixo à esquerda → um grafo simples indicando ações:

  * virar à esquerda

  * virar à direita

  * seguir reto

  * retorno

Quando o objetivo for encontrado, o caminho final será destacado em vermelho.

### 4.Encerrando a execução

Feche as janelas do Matplotlib para finalizar.

### 5.Funcionalidades

Como Funciona o A*

O algoritmo mantém:

 * open_set: nós a serem explorados

 * came_from: árvore de reconstrução do caminho

 * g_score: custo acumulado até cada nó

 * f_score = g(n) + h(n), onde:

A heurística utilizada foi:
```
distância de Manhattan
h = |x1 - x2| + |y1 - y2|
```
### 6.Modificações e Reprodutibilidade

É possível alterar:

 * Dimensão do labirinto

 * Posição inicial

 * Seed aleatória

 * Representação gráfica

Isso garante que o experimento seja completamente reproduzível.

## 🔄 Contribuição

Contribuições são bem-vindas! Envie pull requests ou abra issues com sugestões.

---

## 🏅 Reconhecimentos e Direitos Autorais
* Outros repositórios: https://github.com/MSCunha, https://github.com/gabrielaqueirxz

* Agradecimentos: Universidade Federal do Maranhão (UFMA), Professor Alex Oliveira Barradas Filho, e colegas de curso.


---

## 🛡️ Licença

@Copyright/License

Este material é resultado de um trabalho acadêmico para a disciplina Inteligência Artificial, sobre a orientação do professor Dr. Alex Oliveira Barradas Filho, semestre letivo 2025.2, curso Ciência e Tecnologia, na Universidade Federal do Maranhão (UFMA). Todo o material sob esta licença é software livre: pode ser usado para fins acadêmicos e comerciais sem nenhum custo. Não há papelada, nem royalties, nem restrições de "copyleft" do tipo GNU. Ele é licenciado sob os termos da licença MIT reproduzida abaixo e, portanto, é compatível com GPL e também se qualifica como software de código aberto. É de domínio público. Os detalhes legais estão abaixo. O espírito desta licença é que você é livre para usar este material para qualquer finalidade, sem nenhum custo. O único requisito é que, se você usá-los, nos dê crédito.

Copyright © 2025 Educational Material

Este material está licenciado sob a Licença MIT. É permitido o uso, cópia, modificação, e distribuição deste material para qualquer fim, desde que acompanhado deste aviso de direitos autorais.
