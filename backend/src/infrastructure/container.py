from pathlib import Path

from src.application.ports import (
    AIAssistant,
    DecisionRepository,
    SearchRepository,
)
from src.application.travel.analyze_price_history import (
    AnalyzePriceHistoryUseCase,
)
from src.application.travel.compare_search_snapshots import (
    CompareSearchSnapshotsUseCase,
)
from src.application.travel.export_search_snapshot import (
    ExportSearchSnapshotUseCase,
)
from src.application.travel.explain_decision import ExplainDecisionUseCase
from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)
from src.application.travel.get_decision_history import GetDecisionHistoryUseCase
from src.application.travel.recommend_travel_offers import (
    RecommendTravelOffersUseCase,
)
from src.application.travel.search_orchestrator import SearchOrchestrator
from src.application.travel.save_decision_snapshot import SaveDecisionSnapshotUseCase
from src.core.config import Settings, get_settings
from src.core.readiness import ReadinessService
from src.domain.services.decision_engine import DecisionEngine
from src.domain.services import AIPromptBuilder
from src.domain.services.price_intelligence_engine import (
    PriceIntelligenceEngine,
)
from src.domain.services.recommendation_engine import RecommendationEngine
from src.domain.travel.provider import TravelProvider
from src.infrastructure.ai import TemplateAIAssistant
from src.infrastructure.http.client import HttpClient
from src.infrastructure.persistence import (
    DuckDBDecisionRepository,
    DuckDBSearchRepository,
)
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.infrastructure.providers.provider_strategy import ProviderStrategy


class Container:

    def __init__(self, settings: Settings | None = None):

        self.settings = settings or get_settings()
        self.http_client = HttpClient()

    def get_travel_provider(
        self,
        provider_name: str,
    ) -> TravelProvider:

        return ProviderFactory.create(
            provider_name=provider_name,
            client=self.http_client,
        )

    def get_search_orchestrator(self) -> SearchOrchestrator:
        strategy = ProviderStrategy(
            provider_names=[self.settings.travel_provider],
        )
        engine = DecisionEngine()
        return SearchOrchestrator(
            provider_strategy=strategy,
            decision_engine=engine,
            search_repository=self.get_search_repository(),
        )

    def get_search_repository(self) -> SearchRepository | None:
        if not self.settings.search_persistence_enabled:
            return None

        return DuckDBSearchRepository(
            self.settings.search_database_path,
        )

    def get_readiness_service(self) -> ReadinessService:
        return ReadinessService(
            settings=self.settings,
            http_client=self.http_client,
        )

    def get_ai_assistant(self) -> AIAssistant | None:
        if not self.settings.ai_assistant_enabled:
            return None
        if self.settings.ai_assistant_provider == "template":
            return TemplateAIAssistant()
        raise ValueError(
            "Unsupported AI assistant provider: "
            f"{self.settings.ai_assistant_provider}"
        )

    def get_explain_decision_use_case(
        self,
    ) -> ExplainDecisionUseCase | None:
        assistant = self.get_ai_assistant()
        if assistant is None:
            return None
        return ExplainDecisionUseCase(
            assistant=assistant,
            prompt_builder=AIPromptBuilder(),
        )

    def get_decision_repository(self) -> DecisionRepository | None:
        if not self.settings.decision_persistence_enabled:
            return None
        return DuckDBDecisionRepository(self.settings.decision_database_path)

    def get_save_decision_snapshot_use_case(
        self,
    ) -> SaveDecisionSnapshotUseCase | None:
        repository = self.get_decision_repository()
        return SaveDecisionSnapshotUseCase(repository) if repository else None

    def get_decision_history_use_case(
        self,
    ) -> GetDecisionHistoryUseCase | None:
        repository = self.get_decision_repository()
        return GetDecisionHistoryUseCase(repository) if repository else None

    def get_search_history_use_case(
        self,
    ) -> GetSearchHistoryUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return GetSearchHistoryUseCase(repository)

    def get_search_snapshot_use_case(
        self,
    ) -> GetSearchSnapshotUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return GetSearchSnapshotUseCase(repository)

    def get_compare_search_snapshots_use_case(
        self,
    ) -> CompareSearchSnapshotsUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return CompareSearchSnapshotsUseCase(repository)

    def get_export_search_snapshot_use_case(
        self,
    ) -> ExportSearchSnapshotUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None

        database_path = Path(self.settings.search_database_path)
        return ExportSearchSnapshotUseCase(
            repository=repository,
            export_directory=database_path.parent / "exports",
        )

    def get_recommendation_engine(self) -> RecommendationEngine:
        return RecommendationEngine()

    def get_recommend_travel_offers_use_case(
        self,
    ) -> RecommendTravelOffersUseCase:
        return RecommendTravelOffersUseCase(
            self.get_recommendation_engine()
        )

    def get_price_intelligence_engine(self) -> PriceIntelligenceEngine:
        return PriceIntelligenceEngine()

    def get_analyze_price_history_use_case(
        self,
    ) -> AnalyzePriceHistoryUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return AnalyzePriceHistoryUseCase(
            repository=repository,
            engine=self.get_price_intelligence_engine(),
        )

    async def close(self):

        await self.http_client.close()
