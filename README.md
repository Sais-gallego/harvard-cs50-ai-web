# Harvard University: CS50 & CS50AI (Computer Science & Artificial Intelligence)

![Build Status](https://github.com/Sais-gallego/harvard-cs50-ai-web/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Course](https://img.shields.io/badge/Harvard-CS50%20%26%20CS50AI-crimson.svg)

Implementaciones completas de laboratorios y proyectos fundamentales del icónico programa de Ciencias de la Computación e Inteligencia Artificial de **Harvard University: CS50 / CS50AI**, creado por **David J. Malan** y **Brian Yu**.

**Autor:** Sergio Andrés Ipuz Saavedra  
**GitHub:** [@Sais-gallego](https://github.com/Sais-gallego)  
**Institución:** Harvard University

---

## 🧠 Núcleos de Inteligencia Artificial y Sistemas

### 1. Conocimiento y Lógica Proposicional (`src/knowledge_and_logic.py`)
- **Model Checking y TT-Entails**: Evaluación exhaustiva de árboles lógicos (`Symbol`, `Not`, `And`, `Or`, `Implication`, `Biconditional`) para verificar implicaciones $KB \models \alpha$.
- **Agente Deductivo para Buscaminas (*Minesweeper AI*)**: Motor que infiere celdas seguras y minas utilizando la regla de inferencia de subconjuntos ($S_1 \subset S_2 \implies S_2 - S_1 = count_2 - count_1$).

### 2. Incertidumbre, Redes Bayesianas y Cadenas de Markov (`src/uncertainty_and_markov.py`)
- **Algoritmo PageRank**:
  - Simulación estocástica por el modelo del navegante aleatorio (*Random Surfer*).
  - Cálculo analítico exacto por iteración de estados de Markov hasta convergencia matemática con factor de amortiguamiento $d=0.85$.
- **Red Bayesiana de Herencia Genética (*Heredity Bayes*)**:
  - Modelado de probabilidades condicionales, tasas de mutación y herencia de rasgos genéticos en árboles familiares.

### 3. Optimización y Satisfacción de Restricciones - CSP (`src/optimization_csp.py`)
- **Algoritmo AC-3 (*Arc Consistency 3*)**:
  - Poda automática de dominios incompatibles en redes de restricciones binarias.
- **Búsqueda con Vuelta Atrás (*Backtracking Search*)**:
  - Heurística de selección por Valores Restantes Mínimos (*MRV*).
  - Generación de configuraciones válidas consistentes para puzles de palabras cruzadas y asignación de recursos.

### 4. Búsqueda en Espacio de Estados y Juegos Adversarios (`src/search_and_games.py`)
- **Fronteras de Búsqueda:** DFS (*Depth-First Search* / LIFO), BFS (*Breadth-First Search* / FIFO) y Búsqueda A* con cola de prioridad guiada por heurísticas admisibles $f(n) = g(n) + h(n)$.
- **Minimax con Poda Alfa-Beta para Tres en Línea (*Tic-Tac-Toe AI*):**
  - Motor de búsqueda óptimo de suma cero que garantiza victoria o empate perfecto explorando el árbol de juego con cortes por poda de ramas redundantes $\alpha \ge \beta$.

### 5. Aprendizaje por Refuerzo y Aprendizaje Supervisado (`src/learning_and_rl.py`)
- **Agente de Q-Learning para Nim:**
  - Aprendizaje de función de valor de acción $Q(s, a)$ mediante la ecuación de actualización de Bellman con tasa de aprendizaje $\alpha$ y factor de descuento $\gamma$.
  - Selección de acciones mediante estrategia de exploración $\epsilon$-greedy.
- **Clasificador k-Vecinos Más Cercanos (*k-NN Classifier*):**
  - Predicción de propensión de compra para visitantes web en CS50 Shopping mediante distancia euclidiana y votación por mayoría, reportando métricas de Sensibilidad (*TPR*) y Especificidad (*TNR*).

---

## 🧪 Pruebas Automatizadas

```bash
python -m unittest discover tests -v
```

### Resultados de la Suite (13/13 Passed ✅)
```text
test_astar_frontier ... ok
test_dfs_and_bfs_frontiers ... ok
test_knn_classifier_shopping ... ok
test_nim_q_learning_update ... ok
test_tictactoe_minimax_defense ... ok
test_tictactoe_minimax_optimal_blocking ... ok
test_minesweeper_ai_inference ... ok
test_propositional_logic_model_check ... ok
test_csp_crossword_solve_with_ac3 ... ok
test_csp_node_consistency ... ok
test_heredity_bayesian_probability ... ok
test_pagerank_markov_iteration ... ok
test_transition_model_distribution ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.003s

OK
```
test_pagerank_markov_iteration (test_uncertainty_and_markov.TestUncertaintyAndMarkov.test_pagerank_markov_iteration) ... ok
test_transition_model_distribution (test_uncertainty_and_markov.TestUncertaintyAndMarkov.test_transition_model_distribution) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

---

## 📁 Estructura del Repositorio

```
harvard-cs50-ai-web/
├── .github/
│   └── workflows/
│       └── ci.yml               # CI Pipeline multi-versión (Python 3.10 - 3.12)
├── src/
│   ├── __init__.py
│   ├── knowledge_and_logic.py  # Model checking e inferencia en buscaminas
│   ├── uncertainty_and_markov.py # PageRank Markoviano y Redes Bayesianas
│   └── optimization_csp.py     # Algoritmo AC-3 y búsqueda con backtracking
├── tests/
│   ├── __init__.py
│   ├── test_knowledge_and_logic.py
│   ├── test_uncertainty_and_markov.py
│   └── test_optimization_csp.py
├── SOLUTIONS.md                 # Fundamentos teóricos, modelos probabilísticos y pruebas formales
├── .gitignore
└── README.md
```

---

## 📜 Licencia

MIT License. Desarrollado con fines formativos de excelencia académica por Sergio Andrés Ipuz Saavedra ([@Sais-gallego](https://github.com/Sais-gallego)).
