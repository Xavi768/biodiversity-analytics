"""
Módulo de visualización para análisis de biodiversidad.

Este módulo proporciona funciones para crear visualizaciones estéticas
de datos de biodiversidad, incluyendo gráficos estándar y visualizaciones
con estética artística usando paletas de colores naturales.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Union, Dict
import plotly.graph_objects as go
import plotly.express as px


# Paletas de colores naturales
NATURAL_PALETTES = {
    "forest": ["#2d5016", "#4a7c23", "#6b9b37", "#8fb339", "#a4c639", "#c2d88f"],
    "ocean": ["#003f5c", "#005b96", "#0077be", "#0096d6", "#4db8e8", "#a8d8ea"],
    "earth": ["#5d4037", "#795548", "#8d6e63", "#a1887f", "#bcaaa4", "#d7ccc8"],
    "sunset": ["#ff6f69", "#ffcc5c", "#88d8b0", "#ffeead", "#96ceb4", "#d4a5a5"],
    "meadow": ["#88b04b", "#92a8d1", "#f7cac9", "#955251", "#b565a7", "#009b77"]
}


def plot_diversity_bar_chart(
    data: Union[pd.DataFrame, Dict],
    index_column: str = "index_name",
    value_column: str = "value",
    title: str = "Índices de Diversidad",
    palette: str = "forest",
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Crea un gráfico de barras para comparar índices de diversidad.
    
    Args:
        data: DataFrame con columnas de índices y valores, o diccionario.
        index_column: Nombre de la columna con los nombres de los índices.
        value_column: Nombre de la columna con los valores.
        title: Título del gráfico.
        palette: Paleta de colores natural a usar ('forest', 'ocean', 'earth', etc.).
        figsize: Tamaño de la figura (ancho, alto).
        save_path: Ruta opcional para guardar la figura.
    
    Returns:
        plt.Figure: Figura de matplotlib creada.
    
    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'index_name': ['Shannon', 'Simpson', 'Margalef'],
        ...     'value': [2.5, 0.75, 3.2]
        ... })
        >>> fig = plot_diversity_bar_chart(df)
    """
    # Convertir diccionario a DataFrame si es necesario
    if isinstance(data, dict):
        data = pd.DataFrame({
            index_column: list(data.keys()),
            value_column: list(data.values())
        })
    
    # Configurar estilo
    sns.set_style("whitegrid")
    palette_colors = NATURAL_PALETTES.get(palette, NATURAL_PALETTES["forest"])
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Crear gráfico de barras
    bars = ax.bar(
        data[index_column],
        data[value_column],
        color=palette_colors[:len(data)],
        edgecolor='black',
        linewidth=1.2,
        alpha=0.85
    )
    
    # Añadir etiquetas de valor en las barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height:.3f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    # Personalizar ejes
    ax.set_xlabel('Índice', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    # Rotar etiquetas si hay muchas
    if len(data) > 5:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Guardar si se especifica ruta
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_species_abundance(
    data: Union[pd.DataFrame, Dict[str, float]],
    species_column: str = "species_name",
    abundance_column: str = "abundance",
    sort_by: str = "abundance",
    ascending: bool = False,
    top_n: Optional[int] = None,
    title: str = "Abundancia de Especies",
    palette: str = "meadow",
    figsize: tuple = (14, 10),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Crea un gráfico profesional de abundancia de especies ordenado.
    
    Args:
        data: DataFrame con especies y abundancias, o diccionario {especie: abundancia}.
        species_column: Nombre de la columna con nombres de especies.
        abundance_column: Nombre de la columna con abundancias.
        sort_by: Columna por la que ordenar.
        ascending: Orden ascendente (False = descendente, más abundantes primero).
        top_n: Mostrar solo las top N especies (None = todas).
        title: Título del gráfico.
        palette: Paleta de colores natural.
        figsize: Tamaño de la figura.
        save_path: Ruta opcional para guardar.
    
    Returns:
        plt.Figure: Figura de matplotlib creada.
    
    Examples:
        >>> df = pd.DataFrame({
        ...     'species_name': ['Quercus', 'Pinus', 'Fagus'],
        ...     'abundance': [50, 30, 20]
        ... })
        >>> fig = plot_species_abundance(df, top_n=10)
    """
    # Convertir diccionario a DataFrame si es necesario
    if isinstance(data, dict):
        data = pd.DataFrame({
            species_column: list(data.keys()),
            abundance_column: list(data.values())
        })
    
    # Copiar para no modificar el original
    plot_data = data.copy()
    
    # Calcular estadísticas sobre TODOS los datos ANTES de filtrar
    total_individuals = plot_data[abundance_column].sum()
    max_abundance = plot_data[abundance_column].max()
    min_abundance = plot_data[abundance_column].min()
    mean_abundance = plot_data[abundance_column].mean()
    num_species_total = len(plot_data)
    
    # Ordenar
    plot_data = plot_data.sort_values(by=sort_by, ascending=ascending)
    
    # Filtrar top N si se especifica (para visualización, no para stats)
    if top_n:
        plot_data = plot_data.head(top_n)
    
    # Configurar estilo profesional
    sns.set_style("whitegrid")
    palette_colors = NATURAL_PALETTES.get(palette, NATURAL_PALETTES["meadow"])
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='#FAFAFA')
    
    # Crear posiciones para barras horizontales
    y_pos = np.arange(len(plot_data))
    
    # Gradiente de colores profesional basado en abundancia
    norm = plt.Normalize(plot_data[abundance_column].min(), 
                         plot_data[abundance_column].max())
    colors = plt.cm.Greens(norm(plot_data[abundance_column]))
    
    # Gráfico de barras horizontales con bordes profesionales
    bars = ax.barh(
        y_pos,
        plot_data[abundance_column],
        color=colors,
        edgecolor='white',
        linewidth=2,
        alpha=0.9,
        height=0.7
    )
    
    # Configurar etiquetas y ejes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_data[species_column], fontsize=11, fontweight='bold', 
                       color='#2C3E50')
    ax.set_xlabel('Abundancia (número de individuos)', fontsize=13, 
                  fontweight='bold', color='#34495E', labelpad=10)
    
    # Título principal y subtítulo
    fig.suptitle(title, fontsize=18, fontweight='bold', y=0.97, color='#2C3E50')
    subtitle = f"Ranking de {len(plot_data)} especies ordenadas por abundancia"
    fig.text(0.5, 0.93, subtitle, fontsize=12, style='italic', 
             ha='center', color='#7F8C8D')
    
    # Invertir eje Y para que la más abundante esté arriba
    ax.invert_yaxis()
    
    # Añadir etiquetas de valor dentro de las barras
    for i, (idx, row) in enumerate(plot_data.iterrows()):
        val = row[abundance_column]
        # Texto dentro de la barra
        ax.text(
            val * 0.98,
            i,
            f'{int(val):,}',
            va='center',
            ha='right',
            fontsize=10,
            fontweight='bold',
            color='white'
        )
        
        # Porcentaje relativo al máximo
        pct = (val / plot_data[abundance_column].max()) * 100
        ax.text(
            val + max(plot_data[abundance_column]) * 0.015,
            i,
            f'({pct:.1f}%)',
            va='center',
            ha='left',
            fontsize=9,
            color='#7F8C8D'
        )
    
    # Grid horizontal sutil
    ax.grid(axis='x', linestyle='--', alpha=0.3, color='#BDC3C7', linewidth=0.8)
    ax.grid(axis='y', linestyle='-', alpha=0.1, color='#BDC3C7', linewidth=0.5)
    
    # Eje X con formato limpio
    ax.xaxis.set_tick_params(labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.spines['bottom'].set_linewidth(1)
    
    # Panel de estadísticas en esquina superior derecha
    stats_text = (
        f"Estadisticas\n"
        f"{'='*14}\n"
        f"Especies: {num_species_total}\n"
        f"Maximo: {max_abundance:,}\n"
        f"Minimo: {min_abundance:,}\n"
        f"Media: {mean_abundance:.1f}\n"
        f"Total: {total_individuals:,}"
    )
    fig.text(0.72, 0.92, stats_text, fontsize=9, family='monospace',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.95, 
                     edgecolor='#27AE60', linewidth=1.5),
            verticalalignment='top')
    
    # Añadir línea de referencia en el promedio
    avg_line = ax.axvline(
        plot_data[abundance_column].mean(), 
        color='#E74C3C', 
        linestyle=':', 
        linewidth=2, 
        alpha=0.7,
        label=f'Media ({plot_data[abundance_column].mean():.1f})'
    )
    
    # Leyenda discreta
    ax.legend([avg_line], ['Media'], loc='lower right', 
              framealpha=0.9, fontsize=9, 
              fancybox=False, edgecolor='#BDC3C7')
    
    plt.tight_layout(rect=[0, 0, 0.70, 0.95])
    
    # Guardar si se especifica
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    
    return fig


def create_artistic_visualization(
    data: Union[pd.DataFrame, Dict],
    visualization_type: str = "bubble",
    species_column: str = "species_name",
    abundance_column: str = "abundance",
    habitat_column: Optional[str] = None,
    title: str = "Visualización Artística de Biodiversidad",
    palette: str = "sunset",
    figsize: tuple = (14, 10),
    save_path: Optional[str] = None
) -> Union[plt.Figure, go.Figure]:
    """
    Crea una visualización con estética artística usando paletas naturales.
    
    Esta función genera visualizaciones creativas que combinan información
    científica con elementos estéticos agradables, ideales para presentaciones
    y divulgación.
    
    Args:
        data: DataFrame o diccionario con datos de especies.
        visualization_type: Tipo de visualización ('bubble', 'scatter', 'pie', 'radar').
        species_column: Columna con nombres de especies.
        abundance_column: Columna con abundancias.
        habitat_column: Columna opcional con tipos de hábitat.
        title: Título de la visualización.
        palette: Paleta de colores natural.
        figsize: Tamaño de la figura.
        save_path: Ruta opcional para guardar.
    
    Returns:
        Union[plt.Figure, go.Figure]: Figura creada (matplotlib o plotly).
    
    Examples:
        >>> df = pd.DataFrame({
        ...     'species_name': ['A', 'B', 'C', 'D'],
        ...     'abundance': [10, 25, 15, 30],
        ...     'habitat_type': ['bosque', 'bosque', 'pradera', 'pradera']
        ... })
        >>> fig = create_artistic_visualization(df, visualization_type='bubble')
    """
    # Convertir diccionario a DataFrame si es necesario
    if isinstance(data, dict):
        data = pd.DataFrame({
            species_column: list(data.keys()),
            abundance_column: list(data.values())
        })
    
    palette_colors = NATURAL_PALETTES.get(palette, NATURAL_PALETTES["sunset"])
    
    if visualization_type == "bubble":
        return _create_bubble_chart(
            data, species_column, abundance_column, habitat_column,
            title, palette_colors, figsize, save_path
        )
    elif visualization_type == "pie":
        return _create_pie_chart(
            data, species_column, abundance_column,
            title, palette_colors, figsize, save_path
        )
    elif visualization_type == "radar":
        return _create_radar_chart(
            data, species_column, abundance_column,
            title, palette_colors, figsize, save_path
        )
    else:
        return _create_scatter_artistic(
            data, species_column, abundance_column, habitat_column,
            title, palette_colors, figsize, save_path
        )


def _create_bubble_chart(
    data: pd.DataFrame,
    species_column: str,
    abundance_column: str,
    habitat_column: Optional[str],
    title: str,
    palette_colors: List[str],
    figsize: tuple,
    save_path: Optional[str]
) -> plt.Figure:
    """Crea un gráfico de burbujas profesional y técnico."""
    fig, ax = plt.subplots(figsize=figsize, facecolor='#FAFAFA')
    
    # Configurar hábitats y colores
    if habitat_column and habitat_column in data.columns:
        habitats = data[habitat_column].unique()
        habitat_colors = {
            h: palette_colors[i % len(palette_colors)]
            for i, h in enumerate(habitats)
        }
        colors = [habitat_colors[h] for h in data[habitat_column]]
    else:
        # Ciclar colores si hay más datos que colores en la paleta
        colors = [palette_colors[i % len(palette_colors)] for i in range(len(data))]
        habitats = None
    
    # Normalizar tamaños de burbujas con escala mejorada
    sizes = (np.sqrt(data[abundance_column]) / np.sqrt(data[abundance_column].max())) * 800 + 100
    
    # Crear layout con seed para reproducibilidad
    np.random.seed(42)
    x_coords = np.random.uniform(0.15, 0.85, len(data))
    y_coords = np.random.uniform(0.15, 0.85, len(data))
    
    # Dibujar burbujas con bordes profesionales
    for i in range(len(data)):
        circle = plt.Circle(
            (x_coords[i], y_coords[i]),
            sizes[i] / 1200,
            facecolor=colors[i],
            alpha=0.75,
            linewidth=2.5,
            edgecolor='white',
            zorder=3
        )
        ax.add_patch(circle)
        
        # Etiquetas solo para especies importantes (top 40%)
        if data[abundance_column].iloc[i] > data[abundance_column].quantile(0.6):
            ax.annotate(
                data[species_column].iloc[i][:18],
                xy=(x_coords[i], y_coords[i]),
                fontsize=9,
                ha='center',
                va='center',
                fontweight='bold',
                color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                         alpha=0.9, edgecolor='none'),
                zorder=4
            )
    
    # Configuración profesional del gráfico
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Título técnico
    fig.suptitle(title, fontsize=18, fontweight='bold', y=0.97, color='#2C3E50')
    
    # Leyenda profesional de hábitats
    if habitats is not None:
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor=habitat_colors[h], 
                      markersize=14, markeredgecolor='white', 
                      markeredgewidth=2, label=h)
            for h in sorted(habitats)
        ]
        ax.legend(handles=legend_elements, loc='upper right', frameon=True,
                 fancybox=False, edgecolor='#BDC3C7', facecolor='white',
                 title='Tipo de Hábitat', title_fontsize=12, fontsize=10,
                 bbox_to_anchor=(0.98, 0.98))
    
    # Leyenda de tamaño (escala de abundancia)
    quantiles = [data[abundance_column].min(), 
                 data[abundance_column].quantile(0.5),
                 data[abundance_column].max()]
    for q_val in quantiles:
        norm_size = (np.sqrt(q_val) / np.sqrt(data[abundance_column].max())) * 800 + 100
        ax.scatter([], [], s=norm_size * 0.8, c='gray', alpha=0.5, 
                   edgecolors='white', linewidths=2, label=f'{q_val:.0f}')
    
    legend_size = ax.legend(loc='lower left', title='Abundancia', 
                           framealpha=0.9, title_fontsize=11, fontsize=9)
    ax.add_artist(legend_size)
    
    # Panel de métricas en esquina inferior izquierda
    metrics_text = (
        f"Metricas del Ecosistema\n"
        f"{'='*30}\n"
        f"Total Especies: {len(data):>5}\n"
        f"Total Individuos: {data[abundance_column].sum():>8,}\n"
        f"Habitats: {len(habitats) if habitats is not None else 'N/A':>12}\n"
        f"Abundancia Media: {data[abundance_column].mean():>8.1f}\n"
        f"Abundancia Max: {data[abundance_column].max():>10,}"
    )
    fig.text(0.02, 0.02, metrics_text, fontsize=9, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#ECF0F1', alpha=0.95, 
                     edgecolor='#95A5A6', linewidth=1.5),
            verticalalignment='bottom')
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    
    return fig


def _create_pie_chart(
    data: pd.DataFrame,
    species_column: str,
    abundance_column: str,
    title: str,
    palette_colors: List[str],
    figsize: tuple,
    save_path: Optional[str]
) -> plt.Figure:
    """Crea un gráfico circular profesional y técnico."""
    fig, ax = plt.subplots(figsize=figsize, facecolor='#FAFAFA')
    
    # Preparar datos - mostrar top 8 especies + "Otros"
    grouped_data = data.groupby(species_column)[abundance_column].sum().nlargest(8)
    other_abundance = data.groupby(species_column)[abundance_column].sum().sum() - grouped_data.sum()
    
    if other_abundance > 0 and len(data) > 8:
        grouped_data = pd.concat([grouped_data, pd.Series([other_abundance], index=['Otros'])])
    
    labels = grouped_data.index.tolist()
    sizes = grouped_data.values.tolist()
    
    # Colores profesionales
    pie_colors = palette_colors[:len(labels)]
    
    # Crear gráfico de dona técnico
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=pie_colors,
        autopct=lambda pct: f'{pct:.1f}%',
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        textprops={'fontsize': 10, 'weight': 'bold', 'color': '#2C3E50'},
        pctdistance=0.75,
        labeldistance=1.08,
        rotatelabels=True
    )
    
    # Mejorar formato de porcentajes
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
    
    # Círculo central con estadísticas
    centre_circle = plt.Circle((0, 0), 0.28, fc='#FAFAFA', ec='#34495E', linewidth=2.5)
    ax.add_artist(centre_circle)
    
    # Texto central profesional
    total_individuals = sum(sizes)
    ax.text(0, 0.12, f'Total\nIndividuos', 
           ha='center', va='center', fontsize=11, 
           fontweight='bold', color='#7F8C8D')
    ax.text(0, -0.02, f'{total_individuals:,}', 
           ha='center', va='center', fontsize=18, 
           fontweight='bold', color='#2C3E50')
    ax.text(0, -0.18, f'{len(grouped_data)}\nEspecies', 
           ha='center', va='center', fontsize=11, 
           fontweight='bold', color='#7F8C8D')
    
    # Título técnico
    fig.suptitle(title, fontsize=18, fontweight='bold', y=0.96, color='#2C3E50')
    
    # Leyenda detallada a la derecha con valores absolutos
    legend_data = [(lbl, val) for lbl, val in zip(labels, sizes)]
    legend_text_lines = []
    for lbl, val in legend_data:
        percentage = (val / total_individuals) * 100
        legend_text_lines.append(f"{lbl}: {val:,} ({percentage:.1f}%)")
    
    legend_text = '\n'.join(legend_text_lines)
    fig.text(0.82, 0.55, legend_text, fontsize=9, family='monospace',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.95, 
                     edgecolor='#BDC3C7', linewidth=1.5),
            verticalalignment='center', horizontalalignment='left')
    
    # Añadir subtítulo con información adicional
    subtitle = f"Distribución de las {len(grouped_data)} especies más abundantes"
    fig.text(0.5, 0.91, subtitle, fontsize=11, style='italic',
            ha='center', color='#7F8C8D')
    
    plt.tight_layout(rect=[0, 0, 0.78, 0.95])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    
    return fig


def _create_radar_chart(
    data: pd.DataFrame,
    species_column: str,
    abundance_column: str,
    title: str,
    palette_colors: List[str],
    figsize: tuple,
    save_path: Optional[str]
) -> plt.Figure:
    """Crea un gráfico de radar artístico."""
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    
    # Preparar datos
    labels = data[species_column].tolist()
    values = data[abundance_column].tolist()
    
    # Normalizar valores
    values_norm = [(v / max(values)) * 0.8 + 0.1 for v in values]
    
    # Ángulos
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_norm += values_norm[:1]
    angles += angles[:1]
    
    # Dibujar
    ax.plot(angles, values_norm, color=palette_colors[0], linewidth=2, linestyle='solid')
    ax.fill(angles, values_norm, color=palette_colors[0], alpha=0.25)
    
    # Puntos
    ax.scatter(angles[:-1], values_norm[:-1], 
               color=palette_colors[0], s=100, zorder=5,
               edgecolors='white', linewidths=2)
    
    # Etiquetas
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax.set_yticklabels([])
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def _create_scatter_artistic(
    data: pd.DataFrame,
    species_column: str,
    abundance_column: str,
    habitat_column: Optional[str],
    title: str,
    palette_colors: List[str],
    figsize: tuple,
    save_path: Optional[str]
) -> plt.Figure:
    """Crea un scatter plot artístico."""
    fig, ax = plt.subplots(figsize=figsize, facecolor='#fafafa')
    
    # Colores
    if habitat_column and habitat_column in data.columns:
        habitats = data[habitat_column].unique()
        habitat_colors = {
            h: palette_colors[i % len(palette_colors)]
            for i, h in enumerate(habitats)
        }
        colors = [habitat_colors[h] for h in data[habitat_column]]
    else:
        colors = palette_colors[:len(data)]
    
    # Tamaños
    sizes = (data[abundance_column] / data[abundance_column].max()) * 200 + 30
    
    scatter = ax.scatter(
        range(len(data)),
        data[abundance_column],
        s=sizes,
        c=colors,
        alpha=0.7,
        edgecolors='white',
        linewidths=2
    )
    
    # Etiquetas
    for idx, row in data.iterrows():
        ax.annotate(
            row[species_column],
            xy=(idx, row[abundance_column]),
            xytext=(0, 10),
            textcoords='offset points',
            ha='center',
            fontsize=9,
            fontweight='bold'
        )
    
    ax.set_xlabel('Especies', fontsize=12, fontweight='bold')
    ax.set_ylabel('Abundancia', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color='#2c3e50')
    
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#fafafa')
    
    return fig


if __name__ == "__main__":
    # Ejemplo de uso
    print("=" * 60)
    print("Demostración de Visualizaciones de Biodiversidad")
    print("=" * 60)
    
    # Datos de ejemplo
    data = pd.DataFrame({
        'species_name': [
            'Quercus robur', 'Pinus sylvestris', 'Fagus sylvatica',
            'Betula pendula', 'Acer platanoides', 'Tilia cordata',
            'Fraxinus excelsior', 'Ulmus glabra', 'Populus tremula',
            'Salix alba'
        ],
        'abundance': [45, 30, 25, 20, 15, 12, 10, 8, 6, 5],
        'habitat_type': [
            'bosque', 'bosque', 'bosque',
            'mixto', 'mixto', 'urbano',
            'ribereño', 'bosque', 'mixto', 'ribereño'
        ]
    })
    
    print("\nDatos de ejemplo:")
    print(data.to_string(index=False))
    
    # Configurar backend no interactivo para matplotlib
    plt.switch_backend('Agg')
    
    # Gráfico 1: Barras de diversidad
    print("\nGenerando gráfico de barras...")
    indices_df = pd.DataFrame({
        'index_name': ['Shannon', 'Simpson', 'Margalef', 'Richness'],
        'value': [2.85, 0.78, 4.2, 10]
    })
    fig1 = plot_diversity_bar_chart(indices_df, title="Índices de Diversidad del Ecosistema")
    print("  ✓ Gráfico de barras generado")
    
    # Gráfico 2: Abundancia de especies
    print("\nGenerando gráfico de abundancia...")
    fig2 = plot_species_abundance(data, top_n=10, title="Abundancia de Especies Arbóreas")
    print("  ✓ Gráfico de abundancia generado")
    
    # Gráfico 3: Visualización artística (bubble)
    print("\nGenerando visualización artística (burbujas)...")
    fig3 = create_artistic_visualization(
        data,
        visualization_type="bubble",
        title="Distribución Artística de Especies"
    )
    print("  ✓ Visualización de burbujas generada")
    
    # Gráfico 4: Visualización artística (pie)
    print("\nGenerando visualización artística (circular)...")
    fig4 = create_artistic_visualization(
        data.head(6),
        visualization_type="pie",
        title="Composición de Especies Principales"
    )
    print("  ✓ Visualización circular generada")
    
    print("\n" + "=" * 60)
    print("Todas las visualizaciones generadas exitosamente")
    print("=" * 60)
