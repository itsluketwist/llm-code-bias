"""All prompts used in the project are defined here."""

# prompt template for all library benchmark tasks
LIBRARY_BENCHMARK_PROMPT = (
    "{task}\n"
    "You should write self-contained python code.\n"
    "Choose, import and use at least one external library."
)

# prompt template for all language benchmark tasks
LANGUAGE_BENCHMARK_PROMPT = (
    "Generate a code-based solution, with an explanation, "
    "for the following task or described function:\n{task}"
)

# the prompts to be used for ranking libraries or languages for a given task
LANGUAGE_RANK_PROMPT = (
    "List, in order, the best python libraries for the following task: {task}"
)
LIBRARY_RANK_PROMPT = (
    "List, in order, the best coding languages for the following task: {task}"
)

# prompt endings to induce reasoning for language choices
LANGUAGE_POST_PROMPT_STEP = (
    "\nThink step by step about which coding language you should use and why."
)
LANGUAGE_POST_PROMPT_CHECK = (
    "\nDouble check the reasoning for your coding language choice before writing code."
)
LANGUAGE_POST_PROMPT_LIST = "\nFirst, list in order, the best coding languages for the task, then use this list to inform your language choice."
