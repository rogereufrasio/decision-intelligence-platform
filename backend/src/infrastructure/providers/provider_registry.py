from typing import Callable, Dict, List
from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient


class ProviderNotFoundError(Exception):
    """Lançado quando um provider solicitado não está registrado."""
    pass


class ProviderRegistry:
    """
    Catálogo centralizado para registro e criação de providers de viagem.
    Armazena factories (callables) para permitir a criação configurada de cada provider.
    """

    _registry: Dict[str, Callable[[HttpClient | None], TravelProvider]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        factory_fn: Callable[[HttpClient | None], TravelProvider],
    ) -> None:
        """Registra a função construtora de um provider sob um identificador (case-insensitive)."""
        normalized_name = name.lower().strip()
        cls._registry[normalized_name] = factory_fn

    @classmethod
    def get_factory(
        cls, name: str
    ) -> Callable[[HttpClient | None], TravelProvider]:
        """Retorna a função construtora do provider correspondente ao nome informado."""
        normalized_name = name.lower().strip()
        if normalized_name not in cls._registry:
            raise ProviderNotFoundError(
                f"Provider '{name}' não está registrado no ProviderRegistry."
            )
        return cls._registry[normalized_name]

    @classmethod
    def list_available(cls) -> List[str]:
        """Retorna a lista de nomes de todos os providers atualmente registrados."""
        return list(cls._registry.keys())

    @classmethod
    def unregister_all(cls) -> None:
        """Limpa todos os registros. Útil para isolamento em testes."""
        cls._registry.clear()