"""Code to generate responses from LLMs."""

from llm_cgr import get_llm, timeout

from src.model_defaults import MODEL_DEFAULTS


def generate_model_responses(
    prompt: str,
    models: list[str],
    system_prompt: str | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_tokens: int | None = None,
    timeout_seconds: int = 60,
) -> tuple[dict, dict]:
    """
    Generate responses for the given models and tasks.

    Returns a tuple containing the dictionary of model generations for each prompt,
    and the list of errors hit when generating responses.
    """
    responses: dict[str, str | None] = {}  # model -> response
    errors: dict[str, str] = {}  # model -> error

    for model in models:
        # configure model parameters
        _temperature = temperature or MODEL_DEFAULTS.get(model, {}).get("temperature")
        _top_p = top_p or MODEL_DEFAULTS.get(model, {}).get("top_p")
        _max_tokens = max_tokens or MODEL_DEFAULTS.get(model, {}).get("max_tokens")

        try:
            # do each query in a new session
            llm = get_llm(
                model=model,
                system=system_prompt,
                temperature=_temperature,
                top_p=_top_p,
                max_tokens=_max_tokens,
            )
            with timeout(seconds=timeout_seconds):
                [_response] = llm.generate(user=prompt)
                responses[model] = _response

        except Exception as e:
            # handle any errors
            responses[model] = None
            errors[model] = f"{type(e).__name__}: {str(e)}"

    return responses, errors
