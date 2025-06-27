"""Base experiments to assess bias when generating code."""

from datetime import datetime
from pathlib import Path
from typing import Any

from llm_cgr import experiment, load_json, save_json
from tqdm import tqdm

from src.constants import IDX_SEP, BiasType
from src.evaluate_responses import evaluate_llm_code_bias
from src.generate_responses import generate_model_responses


@experiment
def run_llm_code_bias_experiment(
    bias_type: BiasType,  # "library" or "language"
    dataset_file: str,
    models: list[str],
    samples: int = 3,
    pre_prompt: str | None = None,
    post_prompt: str | None = None,
    system_prompt: str | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_tokens: int | None = None,
    timeout_seconds: int = 60,
    output_dir: str = "output",
    **type_kwargs,
) -> None:
    """
    Run the language experiment to find out what coding languages models will
    try to solve coding problems in, and the distribution between them.
    """
    run_id = Path(dataset_file).stem
    print(
        f"Running experiment: {bias_type=}, {run_id=}, {samples=}, {temperature=}, {top_p=}, "
        f"{max_tokens=}, {timeout_seconds=}, {output_dir=}, {models=}."
    )

    dataset = load_json(file_path=dataset_file)
    print(f"Processing data: {len(dataset)} tasks from {dataset_file=}.")

    _start = datetime.now().isoformat()
    results_file = str(Path(output_dir) / f"{run_id}_{_start}.json")
    results: dict[str, Any] = {
        "metadata": {
            "run_id": run_id,
            "dataset_file": dataset_file,
            "dataset_size": len(dataset),
            "samples": samples,
            "total_tasks": len(dataset) * samples,
            "configured_temperature": temperature or "None - used default",
            "configured_top_p": top_p or "None - used default",
            "configured_max_tokens": max_tokens or "None - used default",
            "start_datetime": _start,
            "end_datetime": datetime.now().isoformat(),
        },
        "prompts": {
            "pre_prompt": pre_prompt,
            "post_prompt": post_prompt,
        },
        "evaluations": {},
        "generations": {},
        "errors": {m: [] for m in models},  # model -> list of errors
        "errors_fixed": False,  # whether errors were fixed
        "no_code_responses": {},  # model -> list of no code responses
        "no_code_fixed": False,  # whether no code responses were fixed
    }

    tasks = [(_id, _idx) for _id in dataset.keys() for _idx in range(1, samples + 1)]
    for _id, _idx in tqdm(tasks):
        task_id = f"{_id}{IDX_SEP}{_idx}"
        prompt = f"{pre_prompt or ''}{dataset[_id]}{post_prompt or ''}"  # build prompt
        responses, errors = generate_model_responses(
            prompt=prompt,
            models=models,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            timeout_seconds=timeout_seconds,
        )

        # update the results for this task
        results["generations"][task_id] = {
            "prompt": prompt,
            "responses": responses,
        }
        results["metadata"]["end_datetime"] = datetime.now().isoformat()
        for _model, _error in errors.items():
            results["errors"][_model].append(f"{task_id}: {_error}")

        # save the results on each iteration to avoid losing data
        save_json(data=results, file_path=results_file)

    print(f"Evaluating results: {results_file=}")
    evaluate_llm_code_bias(
        bias_type=bias_type,
        results_file=results_file,
        **type_kwargs,
    )
