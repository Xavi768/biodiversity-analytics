"""
Módulo para la evaluación de servicios ecosistémicos.

Este módulo proporciona herramientas para clasificar y evaluar servicios
ecosistémicos según el marco del Millennium Ecosystem Assessment (MEA).
"""

from enum import Enum
from typing import Dict, List, Optional, Union
import pandas as pd


class ServiceCategory(Enum):
    """Categorías de servicios ecosistémicos según el Millennium Ecosystem Assessment."""
    PROVISIONING = "Aprovisionamiento"
    REGULATING = "Regulación"
    CULTURAL = "Culturales"
    SUPPORTING = "Soporte"


class EcosystemServicesEvaluator:
    """
    Clase para evaluar y clasificar servicios ecosistémicos.
    
    El Millennium Ecosystem Assessment (2005) clasifica los servicios
    ecosistémicos en cuatro categorías principales que contribuyen al
    bienestar humano.
    
    Attributes:
        services (Dict): Diccionario de servicios registrados.
        evaluations (List): Lista de evaluaciones realizadas.
    """
    
    # Definición de servicios por categoría según MEA
    SERVICE_DEFINITIONS = {
        ServiceCategory.PROVISIONING: {
            "alimentos": "Producción de alimentos (cultivos, ganado, pesca)",
            "agua_dulce": "Provisión de agua dulce",
            "madera": "Producción de madera y fibra",
            "combustible": "Producción de combustible (leña, biomasa)",
            "recursos_geneticos": "Recursos genéticos y bioquímicos",
            "medicinas": "Recursos medicinales y farmacéuticos",
            "ornamentales": "Recursos ornamentales"
        },
        ServiceCategory.REGULATING: {
            "calidad_aire": "Regulación de la calidad del aire",
            "clima": "Regulación del clima (secuestro de carbono)",
            "agua": "Regulación hídrica (control de inundaciones)",
            "erosion": "Control de la erosión del suelo",
            "polinizacion": "Polinización de cultivos",
            "plagas": "Control biológico de plagas y enfermedades",
            "purificacion": "Purificación del agua y tratamiento de residuos"
        },
        ServiceCategory.CULTURAL: {
            "recreacion": "Recreación y ecoturismo",
            "estetico": "Valores estéticos y paisajísticos",
            "espiritual": "Valores espirituales y religiosos",
            "educativo": "Educación e investigación",
            "identidad": "Sentido de lugar e identidad cultural",
            "inspiracion": "Inspiración artística y cultural"
        },
        ServiceCategory.SUPPORTING: {
            "produccion_primaria": "Producción primaria (fotosíntesis)",
            "ciclo_nutrientes": "Ciclo de nutrientes (N, P, K)",
            "formacion_suelo": "Formación y retención de suelo",
            "ciclo_agua": "Ciclo hidrológico",
            "habitat": "Provisión de hábitat para especies",
            "biodiversidad": "Mantenimiento de la diversidad genética"
        }
    }
    
    def __init__(self):
        """Inicializa el evaluador de servicios ecosistémicos."""
        self.services: Dict[str, Dict] = {}
        self.evaluations: List[Dict] = []
    
    def get_categories(self) -> List[str]:
        """
        Obtiene las categorías de servicios ecosistémicos disponibles.
        
        Returns:
            List[str]: Lista de nombres de categorías.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> categories = evaluator.get_categories()
            >>> len(categories)
            4
        """
        return [cat.value for cat in ServiceCategory]
    
    def get_services_by_category(self, category_name: str) -> Dict[str, str]:
        """
        Obtiene los servicios disponibles para una categoría específica.
        
        Args:
            category_name: Nombre de la categoría (en español).
        
        Returns:
            Dict[str, str]: Diccionario de servicios y sus descripciones.
        
        Raises:
            ValueError: Si la categoría no existe.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> services = evaluator.get_services_by_category("Aprovisionamiento")
            >>> "alimentos" in services
            True
        """
        category = self._get_category_enum(category_name)
        return self.SERVICE_DEFINITIONS[category]
    
    def _get_category_enum(self, category_name: str) -> ServiceCategory:
        """Convierte nombre de categoría a enum."""
        for cat in ServiceCategory:
            if cat.value == category_name or cat.name.lower() == category_name.lower():
                return cat
        raise ValueError(
            f"Categoría '{category_name}' no válida. "
            f"Opciones: {[c.value for c in ServiceCategory]}"
        )
    
    def register_service(
        self,
        service_name: str,
        category: str,
        description: Optional[str] = None,
        quantitative_value: Optional[float] = None,
        unit: Optional[str] = None,
        qualitative_score: Optional[int] = None
    ) -> None:
        """
        Registra un servicio ecosistémico para evaluación.
        
        Args:
            service_name: Nombre del servicio.
            category: Categoría del servicio (Aprovisionamiento, Regulación, etc.).
            description: Descripción opcional del servicio.
            quantitative_value: Valor cuantitativo medido (opcional).
            unit: Unidad de medida del valor cuantitativo.
            qualitative_score: Puntuación cualitativa (1-5) donde:
                              1 = Muy bajo, 2 = Bajo, 3 = Moderado,
                              4 = Alto, 5 = Muy alto
        
        Raises:
            ValueError: Si la categoría es inválida o la puntuación está fuera de rango.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> evaluator.register_service(
            ...     "Secuestro de carbono",
            ...     "Regulación",
            ...     quantitative_value=150.5,
            ...     unit="ton CO2/ha/año",
            ...     qualitative_score=4
            ... )
        """
        category_enum = self._get_category_enum(category)
        
        if qualitative_score is not None and not (1 <= qualitative_score <= 5):
            raise ValueError("La puntuación cualitativa debe estar entre 1 y 5")
        
        self.services[service_name] = {
            "category": category_enum.value,
            "description": description or "",
            "quantitative_value": quantitative_value,
            "unit": unit or "",
            "qualitative_score": qualitative_score
        }
    
    def evaluate_service(
        self,
        service_name: str,
        quantitative_value: Optional[float] = None,
        qualitative_score: Optional[int] = None
    ) -> Dict:
        """
        Evalúa un servicio registrado actualizando sus valores.
        
        Args:
            service_name: Nombre del servicio a evaluar.
            quantitative_value: Nuevo valor cuantitativo (opcional).
            qualitative_score: Nueva puntuación cualitativa (opcional).
        
        Returns:
            Dict: Resultado de la evaluación con todos los datos del servicio.
        
        Raises:
            KeyError: Si el servicio no está registrado.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> evaluator.register_service("Polinización", "Regulación")
            >>> result = evaluator.evaluate_service("Polinización", qualitative_score=5)
            >>> result['qualitative_score']
            5
        """
        if service_name not in self.services:
            raise KeyError(f"El servicio '{service_name}' no está registrado")
        
        service = self.services[service_name]
        
        if quantitative_value is not None:
            service["quantitative_value"] = quantitative_value
        if qualitative_score is not None:
            if not (1 <= qualitative_score <= 5):
                raise ValueError("La puntuación cualitativa debe estar entre 1 y 5")
            service["qualitative_score"] = qualitative_score
        
        evaluation_result = {
            "service_name": service_name,
            **service,
            "evaluation_status": "completed"
        }
        
        self.evaluations.append(evaluation_result)
        
        return evaluation_result
    
    def qualitative_quantitative_assessment(
        self,
        service_name: str
    ) -> Dict[str, Union[str, float, int]]:
        """
        Realiza una evaluación cualitativa-cuantitativa integrada de un servicio.
        
        Combina medidas cuantitativas (valores numéricos) con evaluaciones
        cualitativas (puntuaciones expertas) para proporcionar una valoración
        comprehensiva del servicio ecosistémico.
        
        Args:
            service_name: Nombre del servicio a evaluar.
        
        Returns:
            Dict: Diccionario con:
                  - service_name: Nombre del servicio
                  - category: Categoría del servicio
                  - quantitative_assessment: Valor cuantitativo o "No disponible"
                  - qualitative_assessment: Descripción textual de la puntuación
                  - integrated_score: Puntuación integrada (0-100)
                  - assessment_summary: Resumen textual de la evaluación
        
        Raises:
            KeyError: Si el servicio no está registrado.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> evaluator.register_service(
            ...     "Producción de madera",
            ...     "Aprovisionamiento",
            ...     quantitative_value=50.0,
            ...     unit="m³/ha",
            ...     qualitative_score=4
            ... )
            >>> result = evaluator.qualitative_quantitative_assessment("Producción de madera")
            >>> result['integrated_score'] > 0
            True
        """
        if service_name not in self.services:
            raise KeyError(f"El servicio '{service_name}' no está registrado")
        
        service = self.services[service_name]
        
        # Evaluación cualitativa textual
        qualitative_labels = {
            1: "Muy bajo",
            2: "Bajo",
            3: "Moderado",
            4: "Alto",
            5: "Muy alto"
        }
        
        qual_score = service.get("qualitative_score")
        qual_assessment = qualitative_labels.get(qual_score, "No evaluado")
        
        # Evaluación cuantitativa
        quant_value = service.get("quantitative_value")
        quant_assessment = f"{quant_value} {service.get('unit', '')}" if quant_value else "No disponible"
        
        # Cálculo de puntuación integrada (0-100)
        integrated_score = self._calculate_integrated_score(service)
        
        # Generar resumen
        summary_parts = [
            f"Servicio: {service_name}",
            f"Categoría: {service['category']}",
            f"Valor cuantitativo: {quant_assessment}",
            f"Evaluación cualitativa: {qual_assessment}",
            f"Puntuación integrada: {integrated_score}/100"
        ]
        
        return {
            "service_name": service_name,
            "category": service["category"],
            "quantitative_assessment": quant_assessment,
            "qualitative_assessment": qual_assessment,
            "integrated_score": integrated_score,
            "assessment_summary": " | ".join(summary_parts)
        }
    
    def _calculate_integrated_score(self, service: Dict) -> float:
        """Calcula puntuación integrada basada en valores cuali-cuantitativos."""
        score = 0.0
        components = 0
        
        # Componente cualitativo (peso 60%)
        if service.get("qualitative_score"):
            qual_component = (service["qualitative_score"] / 5) * 60
            score += qual_component
            components += 1
        
        # Componente cuantitativo (peso 40%)
        # Normalizamos usando percentiles simples
        if service.get("quantitative_value"):
            quant_value = service["quantitative_value"]
            # Normalización simple (se podría mejorar con datos de referencia)
            if quant_value > 0:
                # Asumimos un máximo teórico de 1000 para normalización
                normalized = min(quant_value / 1000, 1.0)
                quant_component = normalized * 40
                score += quant_component
                components += 1
        
        return round(score, 2)
    
    def get_all_services_summary(self) -> pd.DataFrame:
        """
        Obtiene un resumen de todos los servicios registrados como DataFrame.
        
        Returns:
            pd.DataFrame: Tabla con todos los servicios y sus atributos.
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> evaluator.register_service("Madera", "Aprovisionamiento", qualitative_score=3)
            >>> df = evaluator.get_all_services_summary()
            >>> len(df)
            1
        """
        if not self.services:
            return pd.DataFrame()
        
        data = []
        for name, attrs in self.services.items():
            row = {"service_name": name, **attrs}
            data.append(row)
        
        return pd.DataFrame(data)
    
    def compare_categories(self) -> Dict[str, Dict]:
        """
        Compara las diferentes categorías de servicios registradas.
        
        Returns:
            Dict[str, Dict]: Estadísticas por categoría incluyendo:
                            - count: Número de servicios
                            - avg_qualitative_score: Puntuación cualitativa promedio
                            - total_quantitative: Suma de valores cuantitativos
        
        Examples:
            >>> evaluator = EcosystemServicesEvaluator()
            >>> evaluator.register_service("Madera", "Aprovisionamiento", qualitative_score=4)
            >>> evaluator.register_service("Carbono", "Regulación", qualitative_score=5)
            >>> comparison = evaluator.compare_categories()
            >>> "Aprovisionamiento" in comparison
            True
        """
        category_stats = {}
        
        for cat in ServiceCategory:
            cat_services = [
                s for s in self.services.values()
                if s["category"] == cat.value
            ]
            
            if cat_services:
                count = len(cat_services)
                qual_scores = [
                    s["qualitative_score"] for s in cat_services
                    if s.get("qualitative_score")
                ]
                quant_values = [
                    s["quantitative_value"] for s in cat_services
                    if s.get("quantitative_value")
                ]
                
                category_stats[cat.value] = {
                    "count": count,
                    "avg_qualitative_score": (
                        sum(qual_scores) / len(qual_scores) if qual_scores else None
                    ),
                    "total_quantitative": sum(quant_values) if quant_values else None
                }
        
        return category_stats


if __name__ == "__main__":
    # Ejemplo de uso
    print("=" * 60)
    print("Evaluador de Servicios Ecosistémicos")
    print("=" * 60)
    
    evaluator = EcosystemServicesEvaluator()
    
    # Mostrar categorías
    print("\nCategorías de servicios ecosistémicos:")
    for cat in evaluator.get_categories():
        print(f"  - {cat}")
    
    # Registrar servicios de ejemplo
    print("\nRegistrando servicios de ejemplo...")
    
    evaluator.register_service(
        "Producción de madera",
        "Aprovisionamiento",
        description="Extracción sostenible de madera del bosque",
        quantitative_value=45.5,
        unit="m³/ha/año",
        qualitative_score=4
    )
    
    evaluator.register_service(
        "Secuestro de carbono",
        "Regulación",
        description="Captura y almacenamiento de CO2 atmosférico",
        quantitative_value=180.0,
        unit="ton CO2/ha",
        qualitative_score=5
    )
    
    evaluator.register_service(
        "Ecoturismo",
        "Cultural",
        description="Actividades recreativas en la naturaleza",
        quantitative_value=500,
        unit="visitantes/año",
        qualitative_score=3
    )
    
    evaluator.register_service(
        "Ciclo de nutrientes",
        "Soporte",
        description="Reciclaje de N, P, K en el ecosistema",
        qualitative_score=4
    )
    
    # Mostrar resumen
    print("\nResumen de servicios registrados:")
    df = evaluator.get_all_services_summary()
    print(df.to_string(index=False))
    
    # Evaluación cualitativa-cuantitativa
    print("\n" + "=" * 60)
    print("Evaluación integrada de servicios:")
    print("=" * 60)
    
    for service_name in evaluator.services.keys():
        result = evaluator.qualitative_quantitative_assessment(service_name)
        print(f"\n{result['assessment_summary']}")
    
    # Comparación de categorías
    print("\n" + "=" * 60)
    print("Comparación por categorías:")
    print("=" * 60)
    
    comparison = evaluator.compare_categories()
    for category, stats in comparison.items():
        print(f"\n{category}:")
        print(f"  Servicios: {stats['count']}")
        if stats['avg_qualitative_score']:
            print(f"  Puntuación promedio: {stats['avg_qualitative_score']:.2f}")
