from dataclasses import dataclass

@dataclass
class VectorDato:
    # Indice del vector de datos
    indice: int
    # Indica los valores que son cualitativos
    valor_cualitativo: str
    # Indica los valores que son cuantitativos
    valores_cuantitativos: list