"""
Script de prueba inicial para el proyecto de análisis de biodiversidad.

Este script carga los datos de ejemplo y calcula los índices de diversidad
para verificar que todos los módulos funcionen correctamente.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo

from biodiversity_analysis import (
    shannon_wiener_index,
    simpson_index,
    margalef_index,
    species_richness
)

from ecosystem_services import EcosystemServicesEvaluator

from visualization import (
    plot_diversity_bar_chart,
    plot_species_abundance,
    create_artistic_visualization
)


def main():
    print("=" * 70)
    print("PRUEBA INICIAL - Proyecto de Análisis de Biodiversidad")
    print("=" * 70)
    
    # -------------------------------------------------------------------------
    # PASO 1: Cargar datos de ejemplo
    # -------------------------------------------------------------------------
    print("\n[PASO 1] Cargando datos de ejemplo...")
    try:
        df = pd.read_csv('data/sample_data.csv')
        print(f"  ✓ Datos cargados exitosamente")
        print(f"    - Número de especies: {len(df)}")
        print(f"    - Columnas: {list(df.columns)}")
    except FileNotFoundError:
        print("  ✗ Error: No se encontró el archivo data/sample_data.csv")
        return
    except Exception as e:
        print(f"  ✗ Error al cargar datos: {e}")
        return
    
    # -------------------------------------------------------------------------
    # PASO 2: Calcular índices de diversidad
    # -------------------------------------------------------------------------
    print("\n[PASO 2] Calculando índices de diversidad...")
    
    abundances = df['abundance'].tolist()
    total_individuals = sum(abundances)
    species_count = len(df)
    
    # Índice de Shannon-Wiener
    shannon = shannon_wiener_index(abundances)
    print(f"  ✓ Índice de Shannon-Wiener (H'): {shannon:.4f}")
    
    # Índice de Simpson
    simpson = simpson_index(abundances)
    print(f"  ✓ Índice de Simpson (D): {simpson:.4f}")
    print(f"    Índice de diversidad (1-D): {1-simpson:.4f}")
    
    # Índice de Margalef
    margalef = margalef_index(species_count, total_individuals)
    print(f"  ✓ Índice de Margalef (DMg): {margalef:.4f}")
    
    # Riqueza de especies
    richness = species_richness(df['species_name'].tolist())
    print(f"  ✓ Riqueza de especies: {richness}")
    
    # Interpretación
    print("\n  Interpretación:")
    if shannon > 3:
        print("    - Diversidad: ALTA (ecosistema muy diverso)")
    elif shannon > 1.5:
        print("    - Diversidad: MODERADA")
    else:
        print("    - Diversidad: BAJA (posible estrés ambiental)")
    
    if simpson < 0.3:
        print("    - Equitatividad: ALTA (especies bien distribuidas)")
    elif simpson < 0.7:
        print("    - Equitatividad: MODERADA")
    else:
        print("    - Equitatividad: BAJA (especies dominantes presentes)")
    
    # -------------------------------------------------------------------------
    # PASO 3: Probar módulo de servicios ecosistémicos
    # -------------------------------------------------------------------------
    print("\n[PASO 3] Probando evaluación de servicios ecosistémicos...")
    
    evaluator = EcosystemServicesEvaluator()
    
    # Registrar servicios basados en los datos
    for _, row in df.iterrows():
        evaluator.register_service(
            service_name=row['species_name'],
            category=row['ecosystem_service_type'],
            quantitative_value=float(row['abundance']),
            unit="individuos",
            qualitative_score=np.random.randint(3, 6)
        )
    
    print(f"  ✓ Servicios registrados: {len(evaluator.services)}")
    
    # Obtener resumen
    summary_df = evaluator.get_all_services_summary()
    print(f"  ✓ Resumen generado: {len(summary_df)} servicios")
    
    # Comparar categorías
    comparison = evaluator.compare_categories()
    print(f"  ✓ Categorías comparadas: {len(comparison)}")
    for cat, stats in comparison.items():
        print(f"    - {cat}: {stats['count']} servicios")
    
    # -------------------------------------------------------------------------
    # PASO 4: Probar visualizaciones
    # -------------------------------------------------------------------------
    print("\n[PASO 4] Generando visualizaciones...")
    
    # Gráfico de barras de diversidad
    indices_df = pd.DataFrame({
        'index_name': ['Shannon', 'Simpson (1-D)', 'Margalef', 'Richness'],
        'value': [shannon, 1-simpson, margalef, richness]
    })
    fig1 = plot_diversity_bar_chart(indices_df, title="Índices de Diversidad")
    print("  ✓ Gráfico de barras generado")
    
    # Gráfico de abundancia
    fig2 = plot_species_abundance(df, top_n=10, title="Top 10 Especies por Abundancia")
    print("  ✓ Gráfico de abundancia generado")
    
    # Visualización artística
    fig3 = create_artistic_visualization(
        df,
        visualization_type='bubble',
        habitat_column='habitat_type',
        title="Distribución Artística de Especies"
    )
    print("  ✓ Visualización artística generada")
    
    # -------------------------------------------------------------------------
    # PASO 5: Resumen final
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("RESUMEN DE LA PRUEBA")
    print("=" * 70)
    print(f"\nDatos analizados:")
    print(f"  - Especies totales: {species_count}")
    print(f"  - Individuos totales: {total_individuals}")
    print(f"  - Tipos de hábitat: {df['habitat_type'].nunique()}")
    
    print(f"\nÍndices calculados:")
    print(f"  - Shannon-Wiener: {shannon:.4f}")
    print(f"  - Simpson (1-D): {1-simpson:.4f}")
    print(f"  - Margalef: {margalef:.4f}")
    
    print(f"\nServicios ecosistémicos:")
    for cat, stats in comparison.items():
        print(f"  - {cat}: {stats['count']} especies")
    
    print(f"\nVisualizaciones: 3 gráficos generados exitosamente")
    
    print("\n" + "=" * 70)
    print("¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
