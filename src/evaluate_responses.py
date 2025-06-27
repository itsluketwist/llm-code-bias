from collections import defaultdict

from llm_cgr import load_json, save_json

from src.constants import IDX_SEP, BiasType
from src.extract_languages import extract_code_blocks, extract_languages
from src.extract_libraries import extract_python_libraries


def evaluate_llm_code_bias(
    bias_type: BiasType,
    results_file: str,
    **kwargs,
) -> None:
    """
    Evaluate the results for responses.
    """

    results_data = load_json(file_path=results_file)

    if bias_type == BiasType.LANGUAGE:
        extraction_function = extract_languages
    elif bias_type == BiasType.LIBRARY:
        extraction_function = extract_python_libraries
    else:
        raise ValueError(f"Unknown {bias_type=}. Must be one of {BiasType.options()}.")

    tech_per_task: defaultdict[str, defaultdict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )  # model -> task -> technology set
    counts_per_response: defaultdict[str, defaultdict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )  # model -> technology -> count
    no_code_responses: defaultdict[str, list[str]] = defaultdict(list)

    generations = results_data["generations"]
    for task_id, task_data in generations.items():
        task_name, _, _ = task_id.partition(IDX_SEP)

        for model, response in task_data["responses"].items():
            if not response:
                # skip empty responses
                continue

            # check for code in response, skip and record if no code found
            _code_blocks = extract_code_blocks(response=response)
            if not _code_blocks:
                no_code_responses[model].append(f"{task_id}: {response}")
                continue

            # extract technology from the response
            _technologies = extraction_function(
                response=response,
                **kwargs,  # pass any additional kwargs to the extraction function
            )

            # save the technology used in the *response*
            for _tech in _technologies:
                counts_per_response[model][_tech] += 1

            # save the technology used in the *task*
            tech_per_task[model][task_name].update(_technologies)

    # count the technologies used per task
    counts_per_task: defaultdict[str, defaultdict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )  # model -> technology -> count
    for model, _tasks in tech_per_task.items():
        for _, _technologies in _tasks.items():
            for _tech in _technologies:
                counts_per_task[model][_tech] += 1

    # prepare the evaluation data
    models = list(tech_per_task.keys())
    evaluations = {
        _model: {
            "task_counts": dict(
                sorted(
                    counts_per_task[_model].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ),
            "response_counts": dict(
                sorted(
                    counts_per_response[_model].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ),
        }
        for _model in models
    }

    # update the results and save to file
    results_data["evaluations"] = evaluations
    results_data["no_code_responses"] = dict(no_code_responses)
    results_data["no_code_fixed"] = True if not no_code_responses else False
    save_json(data=results_data, file_path=results_file)
