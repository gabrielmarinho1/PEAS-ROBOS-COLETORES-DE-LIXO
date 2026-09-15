# 🤖 Robô Coletor de Lixo — Agentes Inteligentes (Grid 20x20)

[![Python](https://img.shields.io/badge/Linguagem-Python%20%2F%20NetLogo-blue)](https://github.com)
[![Disciplina](https://img.shields.io/badge/Disciplina-Intelig%C3%AAncia%20Artificial-green)](#)
[![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)](#)

Projeto prático desenvolvido para a disciplina de **Inteligência Artificial**, sob orientação do Prof. Me. Nerval de Jesus Santos Junior. O objetivo é projetar, implementar e comparar quatro diferentes arquiteturas de agentes inteligentes em um ambiente matricial $20 \times 20$.

---

## 📌 Sobre o Problema

O agente **$R_1$** inicia na posição `(1,1)` e tem como missão mapear o ambiente, coletar lixos espalhados e transportá-los até a lixeira **$X$**, localizada em `(20,20)`.

* **Capacidade máxima:** 1 lixo por vez.
* **Lixo Orgânico (+1 pt):** 10 unidades.
* **Lixo Reciclável (+5 pts):** 5 unidades (prioridade de coleta).
* **Visão/Percepção:** Parcialmente observável (8 vizinhos imediatos).

---

## ⚙️ Especificação PEAS

| Componente | Especificação Técnica |
| :--- | :--- |
| **P (Performance)** | Maximizar pontuação (Orgânico +1, Reciclável +5). Minimizar passos, tempo de execução e consumo de energia. Evitar colisões. |
| **E (Environment)** | Matriz $20 \times 20$, ambiente estático, discreto, determinístico, parcialmente observável (visão dos 8 vizinhos) e agente único. |
| **A (Actuators)** | Comandos: `Mover(Esquerda, Direita, Cima, Baixo)`, `Pegar Lixo`, `Soltar Lixo` e `NoOp`. |
| **S (Sensors)** | Posição atual $(x, y)$, sensor de obstáculo, identificador de lixo no local e nos 8 vizinhos, e localização da lixeira. |

---

## 🧠 Arquiteturas Implementadas

### 1. Agente Reativo Simples
Atua com base em regras diretas do tipo **Condição-Ação** observando apenas a percepção local imediata.
* Se estiver sobre o lixo e livre $\rightarrow$ **Pegar Lixo**.
* Se estiver carregando e na posição `(20,20)` $\rightarrow$ **Soltar Lixo**.
* Se vir lixo em 1 dos 8 vizinhos e estiver livre $\rightarrow$ **Mover na direção do lixo**.

### 2. Agente Reativo Baseado em Modelos
Possui um **estado interno/memória** para evitar *loops* e reexploração desnecessária.
* **Memória Interna:** Matriz de visitados $V_{20 \times 20}$ que registra a frequência de acessos a cada célula.
* Flag de estado $C \in \{\text{Livre}, \text{Orgânico}, \text{Reciclável}\}$.

### 3. Agente BDI / Baseado em Objetivos
Planejamento orientado a estados mentais:
* **Crenças (Beliefs):** Mapa conhecido $V_{20 \times 20}$, posição atual $R_1$, estado do inventário $C$ e posição fixada da lixeira $X(20,20)$.
* **Desejos (Desires):** Coletar recicláveis (+5), coletar orgânicos (+1), esvaziar a carga em $X$ e otimizar rotas.
* **Intenções (Intentions):** Se livre $\rightarrow$ busca exploratória focada em recicláveis; Se ocupado $\rightarrow$ rota de menor custo até `(20,20)`.

### 4. Agente Baseado em Utilidade
Avalia o custo-benefício quantitativo de cada ação utilizando a **Distância de Manhattan**:

$$U(\text{Ação}) = \text{Valor do Lixo} - D_{\text{Manhattan}}(\text{PosAgente}, \text{PosLixo}) - D_{\text{Manhattan}}(\text{PosLixo}, X)$$

---

## 📊 Comparativo de Desempenho

Resultados obtidos com a mesma distribuição aleatória inicial dos 15 lixos:

| Arquitetura do Agente | Lixos Coletados | Pontuação Total | Nº de Passos | Tempo de Execução (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **1. Reativo Simples** | 15 | [Preencher] | [Preencher] | [Preencher] |
| **2. Baseado em Modelos** | 15 | [Preencher] | [Preencher] | [Preencher] |
| **3. Baseado em Objetivos** | 15 | [Preencher] | [Preencher] | [Preencher] |
| **4. Baseado em Utilidade** | 15 | [Preencher] | [Preencher] | [Preencher] |

## Função de Desempenho

A função de desempenho do agente considera a coleta de lixo e o custo
de movimentação no ambiente.

- Lixo orgânico coletado: +1 ponto
- Lixo reciclável coletado: +5 pontos
- O agente deve minimizar o número de passos executados
- O agente deve minimizar o tempo de execução
- O agente deve evitar movimentos desnecessários e colisões

A comparação entre as arquiteturas será realizada utilizando a mesma
distribuição inicial de lixo na matriz 20x20.

Para cada agente serão registrados:

- quantidade de lixos coletados;
- pontuação total;
- número de passos;
- tempo de execução.