from copy import deepcopy

from fastapi.testclient import TestClient

from src.api.dependencies.travel import get_explain_decision_use_case
from src.application.travel.explain_decision import ExplainDecisionUseCase
from src.domain.models import AIContext, AIExplanation
from src.domain.services import AIPromptBuilder
from src.infrastructure.ai import TemplateAIAssistant
from src.main import app

client = TestClient(app)


def enabled_use_case() -> ExplainDecisionUseCase:
    return ExplainDecisionUseCase(TemplateAIAssistant(), AIPromptBuilder())


def valid_payload() -> dict[str, object]:
    return {
        "context": {
            "decision_explanation": {
                "summary": "Selected the best eligible offer.",
                "reasons": ["Lowest price"],
                "warnings": ["One option was rejected"],
                "rejected_count": 1,
                "profile": "balanced",
            }
        },
        "correlation_id": "correlation-42",
    }


def test_returns_template_explanation_and_preserves_fields() -> None:
    app.dependency_overrides[get_explain_decision_use_case] = enabled_use_case
    try:
        response = client.post("/api/v1/ai-explanations", json=valid_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Selected the best eligible offer.",
        "reasons": ["Lowest price"],
        "warnings": ["One option was rejected"],
        "confidence": "1",
        "provider": "local",
        "model": "template",
        "correlation_id": "correlation-42",
    }


def test_returns_503_when_assistant_is_disabled() -> None:
    app.dependency_overrides[get_explain_decision_use_case] = lambda: None
    try:
        response = client.post("/api/v1/ai-explanations", json=valid_payload())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 503


def test_returns_422_for_invalid_payload() -> None:
    app.dependency_overrides[get_explain_decision_use_case] = enabled_use_case
    try:
        response = client.post(
            "/api/v1/ai-explanations",
            json={"context": {"price_intelligence": {"snapshot_count": -1}}},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422


class FailingAssistant:
    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation:
        raise RuntimeError("sensitive internal failure")


def test_unexpected_adapter_error_returns_controlled_500() -> None:
    use_case = ExplainDecisionUseCase(FailingAssistant(), AIPromptBuilder())
    app.dependency_overrides[get_explain_decision_use_case] = lambda: use_case
    try:
        response = client.post("/api/v1/ai-explanations", json=valid_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert "sensitive internal failure" not in response.text
    assert response.json()["detail"]["code"] == "ai_assistant_error"


def test_request_input_is_not_modified() -> None:
    payload = valid_payload()
    original = deepcopy(payload)
    app.dependency_overrides[get_explain_decision_use_case] = enabled_use_case
    try:
        response = client.post("/api/v1/ai-explanations", json=payload)
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert payload == original
