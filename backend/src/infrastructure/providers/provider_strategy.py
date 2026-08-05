import logging
from collections.abc import Sequence

from src.domain.models import Offer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.infrastructure.http.client import HttpClient
from src.shared.models import TravelSearchRequest

logger = logging.getLogger(__name__)


class ProviderStrategy:
    """
    Estratégia de execução para múltiplos providers.
    """

    def __init__(
        self,
        provider_names: Sequence[str] | None = None,
        client: HttpClient | None = None,
    ):
        if provider_names:
            self.provider_names = list(provider_names)
        else:
            self.provider_names = ["mock"]
        self.client = client

    def _get_providers(self) -> list[TravelProvider]:
        providers: list[TravelProvider] = []

        for name in self.provider_names:
            try:
                providers.append(ProviderFactory.create(name, self.client))
            except Exception as exc:
                logger.error(
                    "Erro ao instanciar provider '%s': %s",
                    name,
                    exc,
                )

        return providers

    async def search(self, request: TravelSearchRequest) -> TravelResult:
        providers = self._get_providers()

        offers: list[Offer] = []
        warnings: list[str] = []

        last_result: TravelResult | None = None

        for provider in providers:
            try:
                result = await provider.search(request)
                last_result = result

                if result.status != "success":
                    warnings.append(
                        f"Provider {provider.__class__.__name__} returned "
                        f"status '{result.status}': {result.message}"
                    )

                offers.extend(result.offers)

            except Exception as exc:
                logger.error(
                    "Falha na busca do provider '%s': %s",
                    provider,
                    exc,
                )
                warnings.append(
                    f"Provider {provider.__class__.__name__} failed: {exc}"
                )

        # Apenas um provider: preserva exatamente a resposta dele.
        if len(providers) == 1 and last_result is not None:
            return TravelResult(
                provider=self.provider_names[0],
                status=last_result.status,
                message=last_result.message,
                offers=offers,
                warnings=warnings,
            )

        # Múltiplos providers
        if not offers and warnings:
            logger.error("Search failed for all providers")
            status = "error"
            message = "; ".join(warnings)
        elif warnings:
            logger.warning(
                "Search completed with warnings: %s",
                "; ".join(warnings),
            )
            status = "success"
            message = "Offers retrieved with warnings"
        else:
            status = "success"
            message = "Offers retrieved successfully"

        return TravelResult(
            provider="aggregated",
            status=status,
            message=message,
            offers=offers,
            warnings=warnings,
        )
