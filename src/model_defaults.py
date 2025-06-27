"""Defaults for model parameters, used to ensure reproducibility."""

MODEL_DEFAULTS = {
    "gpt-3.5-turbo-0125": {
        # model type: closed / regular
        # data source: https://platform.openai.com/docs/api-reference/chat
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "gpt-4o-mini-2024-07-18": {
        # model type: closed / regular
        # data source: https://platform.openai.com/docs/api-reference/chat
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "claude-3-5-haiku-20241022": {
        # model type: closed / regular
        # data source: https://docs.anthropic.com/en/api/messages
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "claude-3-5-sonnet-20241022": {
        # model type: closed / regular
        # data source: https://docs.anthropic.com/en/api/messages
        "temperature": 1.0,
        "top_p": 1.0,
    },
    "meta-llama/llama-3.2-3b-instruct-turbo": {
        # model type: open / regular
        # data source: https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct/blob/main/generation_config.json
        "temperature": 0.6,
        "top_p": 0.9,
    },
    "deepseek-ai/deepseek-llm-67b-chat": {
        # data source: https://huggingface.co/deepseek-ai/DeepSeek-R1/blob/main/generation_config.json
        "temperature": 0.7,
        "top_p": 0.95,
    },
    "mistralai/mistral-7b-instruct-v0.3": {
        # data source: https://docs.mistral.ai/api/#tag/models/operation/list_models_v1_models_get
        "temperature": 0.7,
        "top_p": 1.0,
    },
    "qwen/qwen2.5-coder-32b-instruct": {
        # data source: https://huggingface.co/qwen/qwen2.5-coder-32b-instruct/blob/main/generation_config.json
        "temperature": 0.7,
        "top_p": 0.8,
    },
}
