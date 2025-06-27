"""Dataset processing utilities for filtering and sampling the datasets."""

import random


def process_dataset(
    tasks: list[str],
    bias_terms: set[str] | None = None,
    prompt_template: str | None = None,
    sample_limit: int | None = None,  # sampling the dataset gives a good representation
    random_seed: int | None = None,  # for sampling reproducibility
) -> dict[str, str]:
    """
    Filter out tasks with mentions of the given terms.
    Sample tasks, and apply a prompt template if provided.
    """
    print(f"Processing {len(tasks)} tasks.")
    # filter out bias terms if given
    if bias_terms is not None:
        # only consider bias terms longer than 2 characters
        bias_terms = {bt.lower() for bt in bias_terms if len(bt) > 2}

        # filter out tasks with mention of bias terms
        tasks = [
            _task
            for _task in tasks
            if not any(_term in _task.lower() for _term in bias_terms)
        ]
        print(f"Have {len(tasks)} remaining after removing tasks with bias.")

    # randomly sample if limit given
    if sample_limit is not None and len(tasks) > sample_limit:
        random.seed(random_seed)
        tasks = random.sample(tasks, sample_limit)
        print(f"Have {len(tasks)} remaining after sampling tasks.")

    # apply prompt template if given
    if prompt_template is not None:
        tasks = [prompt_template.format(task=_task) for _task in tasks]

    digits = len(str(len(tasks)))
    return {str(_i + 1).zfill(digits): _t for _i, _t in enumerate(tasks)}
