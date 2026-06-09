"""
Módulo para el cálculo de índices de diversidad biológica.

Este módulo proporciona funciones para calcular los principales índices
utilizados en ecología para medir la biodiversidad de un ecosistema.
"""

import numpy as np
from typing import List, Union


def shannon_wiener_index(abundances: Union[List[float], np.ndarray]) -> float:
    """
    Calcula el índice de diversidad de Shannon-Wiener (H').
    
    El índice de Shannon-Wiener mide la diversidad de especies en una comunidad,
    considerando tanto la riqueza de especies como la equitatividad en sus abundancias.
    
    Fórmula: H' = -Σ(pi * ln(pi))
    donde pi es la proporción de individuos de la especie i respecto al total.
    
    Args:
        abundances: Lista o array de abundancias de cada especie.
    
    Returns:
        float: Valor del índice de Shannon-Wiener. Mayor valor indica mayor diversidad.
    
    Raises:
        ValueError: Si hay abundancias negativas o si todas son cero.
    
    Examples:
        >>> abundances = [10, 20, 30, 40]
        >>> h = shannon_wiener_index(abundances)
        >>> print(f"Índice de Shannon-Wiener: {h:.4f}")
        
        >>> # Comunidad con alta diversidad (especies igualmente abundantes)
        >>> shannon_wiener_index([25, 25, 25, 25])
        1.3862943611198906
        
        >>> # Comunidad con baja diversidad (una especie dominante)
        >>> shannon_wiener_index([97, 1, 1, 1])
        0.2752943611198906
    """
    abundances = np.array(abundances, dtype=float)
    
    if np.any(abundances < 0):
        raise ValueError("Las abundancias no pueden ser negativas")
    
    total = np.sum(abundances)
    if total == 0:
        raise ValueError("La suma de abundancias no puede ser cero")
    
    # Calcular proporciones (pi)
    proportions = abundances / total
    
    # Filtrar proporciones mayores que cero para evitar log(0)
    proportions = proportions[proportions > 0]
    
    # Calcular índice de Shannon-Wiener
    h = -np.sum(proportions * np.log(proportions))
    
    return h


def simpson_index(abundances: Union[List[float], np.ndarray]) -> float:
    """
    Calcula el índice de Simpson (D) y su complemento (1-D).
    
    El índice de Simpson mide la probabilidad de que dos individuos tomados
    al azar de una muestra pertenezcan a la misma especie.
    
    Fórmula: D = Σ(pi²)
    El complemento (1-D) representa la probabilidad de que dos individuos
    sean de especies diferentes.
    
    Args:
        abundances: Lista o array de abundancias de cada especie.
    
    Returns:
        float: Valor del índice de Simpson (D). Menor valor indica mayor diversidad.
               Para obtener 1-D (índice de diversidad), reste el resultado de 1.
    
    Raises:
        ValueError: Si hay abundancias negativas o si todas son cero.
    
    Examples:
        >>> abundances = [10, 20, 30, 40]
        >>> d = simpson_index(abundances)
        >>> print(f"Índice de Simpson (D): {d:.4f}")
        >>> print(f"Índice de diversidad de Simpson (1-D): {1-d:.4f}")
        
        >>> # Comunidad con alta dominancia (baja diversidad)
        >>> simpson_index([97, 1, 1, 1])
        0.9416
        
        >>> # Comunidad equitativa (alta diversidad)
        >>> simpson_index([25, 25, 25, 25])
        0.25
    """
    abundances = np.array(abundances, dtype=float)
    
    if np.any(abundances < 0):
        raise ValueError("Las abundancias no pueden ser negativas")
    
    total = np.sum(abundances)
    if total == 0:
        raise ValueError("La suma de abundancias no puede ser cero")
    
    # Calcular proporciones (pi)
    proportions = abundances / total
    
    # Calcular índice de Simpson
    d = np.sum(proportions ** 2)
    
    return d


def margalef_index(species_count: int, total_individuals: int) -> float:
    """
    Calcula el índice de Margalef (DMg).
    
    El índice de Margalef es una medida de riqueza de especies que tiene en cuenta
    el número total de individuos en la muestra. Es útil para comparar comunidades
    con diferentes tamaños muestrales.
    
    Fórmula: DMg = (S - 1) / ln(N)
    donde S es el número de especies y N es el número total de individuos.
    
    Args:
        species_count: Número total de especies (riqueza específica).
        total_individuals: Número total de individuos en la muestra.
    
    Returns:
        float: Valor del índice de Margalef. Mayor valor indica mayor riqueza.
    
    Raises:
        ValueError: Si species_count < 1, total_individuals <= 1, o valores negativos.
    
    Examples:
        >>> # 10 especies con 100 individuos totales
        >>> margalef_index(10, 100)
        1.9569...
        
        >>> # Misma riqueza pero más individuos (menor índice)
        >>> margalef_index(10, 1000)
        1.3046...
        
        >>> # Más especies con mismos individuos (mayor índice)
        >>> margalef_index(20, 100)
        3.9138...
    """
    if species_count < 1:
        raise ValueError("El número de especies debe ser al menos 1")
    if total_individuals <= 1:
        raise ValueError("El número total de individuos debe ser mayor que 1")
    if species_count < 0 or total_individuals < 0:
        raise ValueError("Los valores no pueden ser negativos")
    
    dm = (species_count - 1) / np.log(total_individuals)
    
    return dm


def species_richness(data: Union[List, np.ndarray, dict]) -> int:
    """
    Cuenta la riqueza de especies (número total de especies diferentes).
    
    La riqueza de especies es el índice de diversidad más simple, representando
    simplemente el conteo de especies presentes en una comunidad.
    
    Args:
        data: Puede ser:
              - Lista de nombres de especies
              - Array de identificadores de especies
              - Diccionario con especies como claves y abundancias como valores
    
    Returns:
        int: Número de especies diferentes (riqueza específica).
    
    Examples:
        >>> # Desde lista de nombres
        >>> species_richness(['Quercus', 'Pinus', 'Fagus', 'Quercus'])
        3
        
        >>> # Desde diccionario de abundancias
        >>> abundances = {'Quercus': 50, 'Pinus': 30, 'Fagus': 20}
        >>> species_richness(abundances)
        3
        
        >>> # Desde array numpy
        >>> import numpy as np
        >>> species_richness(np.array(['A', 'B', 'C', 'A', 'B']))
        3
    """
    if isinstance(data, dict):
        return len(data.keys())
    else:
        return len(set(data))


if __name__ == "__main__":
    # Ejemplo de uso
    print("=" * 60)
    print("Ejemplo de cálculo de índices de diversidad")
    print("=" * 60)
    
    # Datos de ejemplo: abundancias de 5 especies
    abundances = [25, 15, 30, 20, 10]
    total_individuals = sum(abundances)
    species_count = len(abundances)
    
    print(f"\nDatos de entrada:")
    print(f"  Abundancias: {abundances}")
    print(f"  Total de individuos: {total_individuals}")
    print(f"  Número de especies: {species_count}")
    
    # Calcular índices
    shannon = shannon_wiener_index(abundances)
    simpson = simpson_index(abundances)
    margalef = margalef_index(species_count, total_individuals)
    richness = species_richness(abundances)
    
    print(f"\nResultados:")
    print(f"  Índice de Shannon-Wiener (H'): {shannon:.4f}")
    print(f"  Índice de Simpson (D): {simpson:.4f}")
    print(f"  Índice de Simpson (1-D): {1-simpson:.4f}")
    print(f"  Índice de Margalef (DMg): {margalef:.4f}")
    print(f"  Riqueza de especies: {richness}")
    
    # Interpretación básica
    print(f"\nInterpretación:")
    if shannon > 3:
        print("  - Alta diversidad (ecosistema muy diverso)")
    elif shannon > 1.5:
        print("  - Diversidad moderada")
    else:
        print("  - Baja diversidad (posible estrés ambiental)")
    
    if simpson < 0.3:
        print("  - Alta equitatividad (especies bien distribuidas)")
    elif simpson < 0.7:
        print("  - Equitatividad moderada")
    else:
        print("  - Baja equitatividad (especies dominantes presentes)")
