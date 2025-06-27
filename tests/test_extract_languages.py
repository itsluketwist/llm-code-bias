"""
Test our method for extracting programming languages from LLM responses.
"""

import pytest

from src.extract_languages import extract_languages


LANGUAGE_TEST_DATA = [
    (
        # single python code block
        """Here is a Python solution to the problem.
```python
def solve_problem():
    print("This is a Python solution.")
```
I will use Python for this task.
""",
        {"python"},
    ),
    (
        # multiple code blocks, different languages
        """Here are solutions in different languages:
```python
def solve_problem():
    print("This is a Python solution.")
```
```javascript
function solveProblem() {
    console.log("This is a JavaScript solution.");
}
```
```java
public class Solution {
    public static void main(String[] args) {
        System.out.println("This is a Java solution.");
    }
}
""",
        {"python", "javascript", "java"},
    ),
    (
        # no code blocks, just mentions of languages
        "I will use C++ and Python for this task.",
        set(),
    ),
    (
        # complete code block and cut off code block
        """Here is a complete golang code block:
```go
package main

import "fmt"

func main() {
    fmt.Println("This is a complete Go solution.")
}
```
And here is a cut-off ruby code block:
```ruby
def incomplete_solution():
    print("This is an incomplete Ruby solution.")
""",
        {"go", "ruby"},
    ),
    (
        # codeblock with no language specified
        """Here is a code block without a specified language:
```
def solve_problem():
    print("This is a solution without a specified language.")
```
""",
        set(),
    ),
]


@pytest.mark.parametrize("response,expected_languages", LANGUAGE_TEST_DATA)
def test_extract_languages(response, expected_languages):
    """Test the extract_languages function with various responses."""
    assert extract_languages(response=response) == expected_languages
