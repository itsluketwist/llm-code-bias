"""Methods for extracting programming languages from markdown formatted text."""

import re


# regex to extract code blocks from markdown text
CODE_BLOCK_REGEX = re.compile(
    pattern=r"\`\`\`(\w*)\n(.*?)(?:\`\`\`|$)",
    flags=re.DOTALL,
)


def extract_code_blocks(
    response: str,
) -> list[tuple[str | None, str]]:
    """
    Extract the code blocks from the markdown formatted text.

    Returns (language, code) tuples for each code block found.
    """
    matches = CODE_BLOCK_REGEX.findall(string=response)
    code_blocks = [
        (language if language else None, code.strip()) for language, code in matches
    ]
    return code_blocks


def extract_languages(response: str) -> set[str]:
    """
    Extract the programming languages mentioned in the response.

    Returns the set of programming languages.
    """
    code_blocks = extract_code_blocks(response)
    languages = {language.lower() for language, _ in code_blocks if language}
    return languages
