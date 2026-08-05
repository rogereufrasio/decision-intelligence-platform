from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from src.api.dependencies.travel import get_explain_decision_use_case
from src.api.schemas.ai_explanation_schema import (
    AIExplanationRequest,
    AIExplanationResponse,
)
from src.application.travel.explain_decision import ExplainDecisionUseCase

router = APIRouter(prefix="/ai-explanations", tags=["AI Explanations"])


@router.post("", response_model=AIExplanationResponse)
async def explain_decision(
    payload: dict[str, object],
    use_case: ExplainDecisionUseCase | None = Depends(
        get_explain_decision_use_case
    ),
) -> AIExplanationResponse:
    try:
        request = AIExplanationRequest.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_ai_explanation_payload",
                "message": "The AI explanation payload is invalid.",
            },
        ) from exc

    if use_case is None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "ai_assistant_disabled",
                "message": "AI-assisted explanations are disabled.",
            },
        )

    try:
        explanation = await use_case.execute(request.context)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ai_assistant_error",
                "message": "The assisted explanation could not be generated.",
            },
        ) from exc

    return AIExplanationResponse.from_domain(
        explanation,
        request.correlation_id,
    )
