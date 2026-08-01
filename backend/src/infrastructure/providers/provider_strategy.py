import logging
from typing import List, Sequence
from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.shared.models import TravelSearchRequest

logger = logging.getLogger(__name__)


class ProviderStrategy:
    """
    Estratégia de execução para múltiplos providers de viagem.
    Responsável por orquestrar as chamadas de busca entre os providers registrados.
    """

    def __init__(self, provider_names: Sequence[str] | None = None):
        """
        Se nenhum provider for especificado, utiliza 'amadeus' por padrão (ou os ativos).
        """
        self.provider_names = list(provider_names) if provider_names else ["amadeus"]

    def _get_providers(self) -> List[TravelProvider]:
        """Instancia os providers solicitados via ProviderFactory."""
        providers: List[TravelProvider] = []
        for name in self.provider_names:
            try:
                providers.append(ProviderFactory.create(name))
            except Exception as e:
                logger.error(f"Erro ao instanciar provider '{name}': {e}")
        return providers

    async def search(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str | None = None,
        adults: int = 1,
    ) -> List[TravelOffer]:
        """
        Executa a busca de ofertas em todos os providers configurados de forma sequencial.
        Coleta e unifica os resultados, isolando falhas individuais.
        """
        offers: List[TravelOffer] = []
        providers = self._get_providers()
        request = TravelSearchRequest(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
        )

        for provider in providers:
            try:
                results: TravelResult = await provider.search(request)
                offers.extend(results.offers)
            except Exception as e:
                logger.error(f"Falha na busca do provider '{provider}': {e}")

        return offers