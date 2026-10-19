# Soluciones Técnicas y Fundamentos de IA: Harvard CS50 / CS50AI

**Autor:** Sergio Andrés Ipuz Saavedra  
**GitHub:** [@Sais-gallego](https://github.com/Sais-gallego)  
**Institución:** Harvard University  
**Cursos:** CS50: Introduction to Computer Science & CS50AI: Introduction to Artificial Intelligence with Python  
**Profesor:** David J. Malan & Brian Yu

---

## 1. Módulos y Algoritmos Implementados

### 1.1 Lógica Proposicional e Inferencia en Buscaminas (`src/knowledge_and_logic.py`)
- **AST Proposicional y Model Checking (TT-Entails)**:
  - Estructura de árbol sintáctico abstracto para proposiciones: `Symbol`, `Not`, `And`, `Or`, `Implication`, `Biconditional`.
  - Verificación exhaustiva de modelos: $KB \models \alpha$ mediante recursión en ramas verdaderas/falsas enumerando todos los modelos booleanos posibles.
- **Motor de Inferencia Lógica para Buscaminas (*Minesweeper AI*)**:
  - Sentencias de conocimiento en forma de conjuntos de celdas no determinadas con cardinalidad de minas: $\{c_1, c_2, \dots, c_k\} = n$.
  - Deducción de subconjuntos: si $S_1 \subseteq S_2$, entonces $(S_2 \setminus S_1) = (n_2 - n_1)$.
  - Marcado automático e iterativo de casillas seguras y minas neutralizando ambigüedades.

### 1.2 Incertidumbre, Redes Bayesianas y Cadenas de Markov (`src/uncertainty_and_markov.py`)
- **Algoritmo PageRank**:
  - *Random Surfer Model*: Simulación estocástica Monte Carlo de saltos entre páginas web con factor de amortiguación $d = 0.85$.
  - *Iterative Markov Transition*: Convergencia analítica del vector estacionario de PageRank:
    $$PR(p) = \frac{1-d}{N} + d \sum_{i \in \text{in}(p)} \frac{PR(i)}{|\text{out}(i)|}$$
- **Red Bayesiana de Herencia Genética (*Heredity Bayes*)**:
  - Probabilidad conjunta y condicionada de mutación y transmisión del gen de una o dos copias de padres a hijos.
  - Expresión fenotípica marginal del rasgo según penetrancia genética.

### 1.3 Optimización y Problemas de Satisfacción de Restricciones (CSP) (`src/optimization_csp.py`)
- **Algoritmo AC-3 (*Arc Consistency 3*)**:
  - Verificación y poda de dominios de variables para asegurar consistencia de arcos binarios.
  - Cola de arcos dinámicamente actualizada tras cada poda de dominio.
- **Búsqueda con Vuelta Atrás (*Backtracking Search*)**:
  - Heurística de Valores Restantes Mínimos (MRV - *Minimum Remaining Values*).
  - Poda temprana al detectar estados inconsistentes con la asignación previa.

---

## 2. Cobertura de Pruebas Automatizadas

La suite en `tests/` ejecuta 7 pruebas unitarias de extremo a extremo:
- `test_knowledge_and_logic.py`: Puzle de caballeros y villanos con model checking y deducción lógica de casillas seguras/minas en buscaminas.
- `test_uncertainty_and_markov.py`: Convergencia iterativa de PageRank, distribución del modelo de transición y probabilidad conjunta bayesiana.
- `test_optimization_csp.py`: Resolución de crucigrama con AC-3 y verificación de consistencia de nodos.

**Resultado:** 100% de pruebas aprobadas en tiempo ultra-rápido (< 0.002s).
