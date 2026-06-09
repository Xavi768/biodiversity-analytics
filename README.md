# Proyecto de Análisis de Biodiversidad

Un conjunto completo de herramientas para el análisis cuantitativo y cualitativo de la biodiversidad, incluyendo cálculo de índices ecológicos, evaluación de servicios ecosistémicos y visualizaciones estéticas.

## Descripción del Proyecto

Este proyecto proporciona módulos Python para:

1. **Cálculo de índices de diversidad biológica** (Shannon-Wiener, Simpson, Margalef)
2. **Evaluación de servicios ecosistémicos** según el Millennium Ecosystem Assessment
3. **Visualización de datos** con gráficos estándar y estéticos usando paletas naturales

## Requisitos

- Python 3.8+
- pip

## Instalación

### 1. Clonar o descargar el repositorio

```bash
cd /workspace
```

### 2. Instalar dependencias

```bash
pip install pandas numpy scipy matplotlib seaborn plotly scikit-learn
```

### 3. Verificar instalación

```bash
python biodiversity_analysis.py
```

## Estructura del Proyecto

```
/workspace/
├── biodiversity_analysis.py    # Índices de diversidad
├── ecosystem_services.py       # Evaluación de servicios ecosistémicos
├── visualization.py            # Visualizaciones gráficas
├── data/
│   └── sample_data.csv         # Datos de ejemplo
└── README.md                   # Este archivo
```

## Uso de los Módulos

### Módulo 1: biodiversity_analysis.py

Cálculo de índices de diversidad biológica:

```python
from biodiversity_analysis import (
    shannon_wiener_index,
    simpson_index,
    margalef_index,
    species_richness
)

# Datos de abundancia de especies
abundances = [25, 15, 30, 20, 10]

# Calcular índice de Shannon-Wiener
h = shannon_wiener_index(abundances)
print(f"Índice de Shannon-Wiener: {h:.4f}")

# Calcular índice de Simpson
d = simpson_index(abundances)
print(f"Índice de Simpson (D): {d:.4f}")
print(f"Índice de diversidad (1-D): {1-d:.4f}")

# Calcular índice de Margalef
species_count = len(abundances)
total_individuals = sum(abundances)
dm = margalef_index(species_count, total_individuals)
print(f"Índice de Margalef: {dm:.4f}")

# Calcular riqueza de especies
richness = species_richness(abundances)
print(f"Riqueza de especies: {richness}")
```

### Módulo 2: ecosystem_services.py

Evaluación de servicios ecosistémicos según el Millennium Ecosystem Assessment:

```python
from ecosystem_services import EcosystemServicesEvaluator

# Crear evaluador
evaluator = EcosystemServicesEvaluator()

# Ver categorías disponibles
print(evaluator.get_categories())
# ['Aprovisionamiento', 'Regulación', 'Culturales', 'Soporte']

# Registrar servicios
evaluator.register_service(
    "Producción de madera",
    "Aprovisionamiento",
    description="Extracción sostenible de madera",
    quantitative_value=45.5,
    unit="m³/ha/año",
    qualitative_score=4
)

evaluator.register_service(
    "Secuestro de carbono",
    "Regulación",
    description="Captura de CO2 atmosférico",
    quantitative_value=180.0,
    unit="ton CO2/ha",
    qualitative_score=5
)

# Obtener resumen
df = evaluator.get_all_services_summary()
print(df)

# Evaluación integrada cualitativa-cuantitativa
result = evaluator.qualitative_quantitative_assessment("Secuestro de carbono")
print(result['assessment_summary'])

# Comparar categorías
comparison = evaluator.compare_categories()
for cat, stats in comparison.items():
    print(f"{cat}: {stats}")
```

### Módulo 3: visualization.py

Creación de visualizaciones estéticas:

```python
import pandas as pd
import matplotlib.pyplot as plt
from visualization import (
    plot_diversity_bar_chart,
    plot_species_abundance,
    create_artistic_visualization
)

# Cargar datos
df = pd.read_csv('data/sample_data.csv')

# Configurar matplotlib para guardar sin mostrar
plt.switch_backend('Agg')

# Gráfico de barras de índices
indices_df = pd.DataFrame({
    'index_name': ['Shannon', 'Simpson', 'Margalef'],
    'value': [2.85, 0.78, 4.2]
})
fig1 = plot_diversity_bar_chart(indices_df, palette='forest')
fig1.savefig('diversity_indices.png', dpi=300)

# Gráfico de abundancia de especies
fig2 = plot_species_abundance(df, top_n=10, palette='meadow')
fig2.savefig('species_abundance.png', dpi=300)

# Visualización artística tipo burbuja
fig3 = create_artistic_visualization(
    df,
    visualization_type='bubble',
    habitat_column='habitat_type',
    palette='sunset'
)
fig3.savefig('artistic_bubble.png', dpi=300)

# Visualización circular
fig4 = create_artistic_visualization(
    df.head(6),
    visualization_type='pie',
    palette='ocean'
)
fig4.savefig('species_pie.png', dpi=300)
```

## Paletas de Colores Disponibles

El módulo de visualización incluye 5 paletas de colores naturales:

| Paleta | Colores | Uso recomendado |
|--------|---------|-----------------|
| `forest` | Verdes | Bosques, vegetación |
| `ocean` | Azules | Ambientes acuáticos |
| `earth` | Marrones | Suelos, geología |
| `sunset` | Cálidos | Atardeceres, flores |
| `meadow` | Variados | Praderas, diversidad |

## Ejemplos de Interpretación de Índices

### Índice de Shannon-Wiener (H')
- **H' > 3**: Alta diversidad (ecosistema muy diverso)
- **1.5 < H' < 3**: Diversidad moderada
- **H' < 1.5**: Baja diversidad (posible estrés ambiental)

### Índice de Simpson (1-D)
- **> 0.7**: Alta equitatividad (especies bien distribuidas)
- **0.3 - 0.7**: Equitatividad moderada
- **< 0.3**: Baja equitatividad (especies dominantes presentes)

### Índice de Margalef (DMg)
- Valores más altos indican mayor riqueza específica
- Útil para comparar comunidades con diferentes tamaños muestrales

## Datos de Ejemplo

El archivo `data/sample_data.csv` contiene 24 especies con:
- `species_name`: Nombre científico de la especie
- `abundance`: Número de individuos
- `habitat_type`: Tipo de hábitat (bosque, mixto, urbano, etc.)
- `ecosystem_service_type`: Tipo de servicio ecosistémico principal

## Ejecutar Demo Completa

```bash
# Ejecutar cada módulo individualmente
python biodiversity_analysis.py
python ecosystem_services.py
python visualization.py
```

## Autor y Licencia

Proyecto desarrollado para análisis de biodiversidad y educación ambiental.

## Referencias

1. **Millennium Ecosystem Assessment (2005)**. Ecosystems and Human Well-being: Synthesis. Island Press, Washington, DC.
2. **Magurran, A.E. (2004)**. Measuring Biological Diversity. Blackwell Science.
3. **Shannon, C.E. & Weaver, W. (1949)**. The Mathematical Theory of Communication. University of Illinois Press.
4. **Simpson, E.H. (1949)**. Measurement of Diversity. Nature, 163:688.
5. **Margalef, R. (1958)**. Information theory in ecology. General Systems, 3:36-71.
