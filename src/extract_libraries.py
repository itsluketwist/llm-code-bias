"""Methods for extracting libraries from Python code blocks in LLM responses."""

import re

from src.constants import PYTHON_STDLIB
from src.extract_languages import extract_code_blocks


# regex to extract imports from python code: `from module import thing`
FROM_MODULE_IMPORT_REGEX = re.compile(
    pattern=r"^\s*from\s+(\w[\w.]+)\s+import\s*\(?\s*(.*)$",
)


# regex to extract imports from python code: `import module`
IMPORT_MODULE_REGEX = re.compile(
    pattern=r"^\s*import\s+(.*)$",
)


def extract_python_imports_from_line(
    line: str,
) -> set[str]:
    """
    Extract any imported modules in a line of python code.

    Returns the set of imported python modules found in the line.
    """
    line = line.split("#")[0]  # ignore comments

    # find `from module import thing` imports
    if match := FROM_MODULE_IMPORT_REGEX.search(string=line):
        _import = match.group(1)

        if "." in _import:
            _import, _, _ = _import.partition(".")

        return {_import}

    # find `import module` imports
    if match := IMPORT_MODULE_REGEX.search(string=line):
        imports = set()
        matches = [m.strip() for m in match.group(1).split(",")]

        for _import in matches:
            if _import.startswith("."):
                continue  # skip local imports

            if " as " in _import:
                _import, _, _ = _import.partition(" as ")

            if "." in _import:
                _import, _, _ = _import.partition(".")

            imports.add(_import)

        return imports

    return set()


def extract_python_libraries(
    response: str,
    include_stdlib: bool = False,
) -> set[str]:
    """
    Extract any imported python modules within the code blocks of a markdown response.

    Returns the set of imported python modules found in the response.
    """
    imports = set()
    for language, code in extract_code_blocks(response=response):
        if not language or language != "python":
            # ignore anything that is not explicitly python
            continue

        for line in code.split("\n"):
            # extract imports per line
            imports.update(extract_python_imports_from_line(line=line.strip()))

    if include_stdlib:
        return imports
    else:
        return imports - set(PYTHON_STDLIB)
