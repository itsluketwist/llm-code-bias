"""
Test our method for extracting programming languages from LLM responses.
"""

import pytest

from src.extract_libraries import extract_python_libraries


LIBRARY_TEST_DATA = [
    (
        # python response with libraries
        """Here is a Python solution to the problem.
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
def solve_problem():
    print("This is a Python solution.")
```
I will use Python for this task.
""",
        False,
        {"numpy", "pandas", "matplotlib"},
    ),
    (
        # multiple python code blocks, different libraries
        """Here are solutions in different languages:
```python
import numpy as np
def solve_problem():
    print("This is a Python solution.")
```
```javascript
import express from 'express';
function solveProblem() {
    console.log("This is a JavaScript solution.");
}
```
```python
import requests
def fetch_data():
    print("Fetching data in Python.")
```
""",
        False,
        {"numpy", "requests"},
    ),
    (
        # python code, return stdlibs too
        """Here is a Python solution to the problem.
```python
import os, sys
import numpy as np
def solve_problem():
    print("This is a Python solution.")
```""",
        True,
        {"os", "sys", "numpy"},
    ),
    (
        # valid python code blocks, but no libraries
        """Here is a Python solution to the problem.
```python
def solve_problem():
    print("This is a Python solution.")
```""",
        False,
        set(),
    ),
    (
        # valid python code block, but not specified as python
        """Here is a code block without a specified language:
```
import numpy as np
import re
def solve_problem():
    print("This is a Python solution.")
```""",
        False,
        set(),
    ),
]


@pytest.mark.parametrize(
    "response,include_stdlib,expected_libraries", LIBRARY_TEST_DATA
)
def test_extract_python_libraries(response, include_stdlib, expected_libraries):
    """Test the extract_python_libraries function with various responses."""
    assert (
        extract_python_libraries(
            response=response,
            include_stdlib=include_stdlib,
        )
        == expected_libraries
    )
