"""Sesión 1 — Prueba diagnóstica (45 min). Implemente cada función y ejecute:

    uv run pytest diagnostico -q

Mide: tipado, colecciones, comprensiones, funciones de orden superior, generadores,
manejo de errores, dataclasses y context managers. No requiere librerías externas.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass


# 1. Comprensiones -----------------------------------------------------------
def palabras_por_longitud(texto: str) -> dict[int, list[str]]:
    """Agrupa palabras únicas (minúsculas, sin puntuación) por longitud, ordenadas."""

    clean_text = ""
    for char in texto.lower():
        if char not in ".,;:¡!¿?()[]{}\"'-_":
            clean_text += char
        else:
            clean_text += " "

    raw_words = clean_text.split()

    unique_words = []
    for word in raw_words:
        if word not in unique_words:
            unique_words.append(word)

    unique_words.sort()

    result = {}
    for word in unique_words:
        length = len(word)
        if length not in result:
            result[length] = []
        result[length].append(word)

    return result


# 2. Colecciones -------------------------------------------------------------
def top_n(frecuencias: Iterable[str], n: int) -> list[tuple[str, int]]:
    """Los n elementos más frecuentes; empate → orden alfabético."""

    counts = {}
    for item in frecuencias:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    items_list = []
    for item, count in counts.items():
        items_list.append((item, count))

    def by_word(element):
        return element[0]  # Devuelve la palabra (posición 0)

    def by_frequency(element):
        return element[1]  # Devuelve la cantidad (posición 1)

    items_list.sort(key=by_word)

    items_list.sort(key=by_frequency, reverse=True)

    return items_list[:n]


# 3. Funciones de orden superior / closures ----------------------------------
def reintentar(veces: int) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Decorador: reintenta la función hasta `veces` si lanza excepción; luego la propaga."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(veces):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if attempt == veces - 1:
                        raise error

        return wrapper

    return decorator


# 4. Generadores -------------------------------------------------------------
def en_lotes[T](items: Iterable[T], tamano: int) -> Iterator[list[T]]:
    """Entrega listas de `tamano` elementos (la última puede ser menor). Perezoso."""
    batch = []

    for item in items:
        batch.append(item)

        if len(batch) == tamano:
            yield batch

            batch = []

    if len(batch) > 0:
        yield batch


# 5. Dataclasses + propiedades -----------------------------------------------
@dataclass
class Factura:
    subtotal: float
    iva: float = 0.19

    @property
    def total(self) -> float:
        raise NotImplementedError

    def __post_init__(self) -> None:
        """Debe lanzar ValueError si subtotal < 0 o iva fuera de [0, 1]."""
        raise NotImplementedError


# 6. Context managers --------------------------------------------------------
class Cronometro:
    """with Cronometro() as c: ...  → c.segundos tiene la duración del bloque."""

    def __enter__(self) -> Cronometro:
        raise NotImplementedError

    def __exit__(self, *exc: object) -> None:
        raise NotImplementedError
