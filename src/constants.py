"""Constants for use throughout the project."""

import sys
from enum import StrEnum


IDX_SEP = ">>>"


class BiasType(StrEnum):
    """Enum for different types of experiments that can be run."""

    LIBRARY = "library"
    LANGUAGE = "language"

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def options(cls) -> str:
        """Return a list of all experiment types."""
        return ", ".join([type.value for type in cls])


# list of Python standard library modules
PYTHON_STDLIB = set(getattr(sys, "stdlib_module_names", []))


# list of external libraries used in the BigCodeBench dataset (February 2025)
# https://huggingface.co/datasets/bigcode/bigcodebench
# fmt: off
BIGCODEBENCH_EXTERNAL_LIBRARIES = {
    'holidays', 'faker', 'librosa', 'natsort', 'pandas',
    'skimage', 'blake3', 'bs4', 'flask_restful', 'pytesseract',
    'geopandas', 'matplotlib', 'flask_mail', 'sendgrid', 'geopy',
    'openpyxl', 'xlwt', 'keras', 'sklearn', 'numpy',
    'flask_wtf', 'tensorflow', 'nltk', 'seaborn', 'chardet',
    'statsmodels', 'crypto', 'texttable', 'gensim', 'wordcloud',
    'django', 'flask', 'cryptography', 'pytz', 'regex',
    'sympy', 'soundfile', 'dateutil', 'docx', 'xmltodict',
    'rsa', 'prettytable', 'wordninja', 'lxml', 'wikipedia',
    'folium', 'mechanize', 'wtforms', 'python_http_client', 'pil',
    'textblob', 'pyquery', 'psutil', 'shapely', 'yaml',
    'requests', 'flask_login', 'levenshtein', 'werkzeug', 'mpl_toolkits',
    'cv2', 'scipy',
}
# fmt: on


# list of top 50 languages from the TIOBE index (February 2025)
# source: https://www.tiobe.com/tiobe-index/
# fmt: off
TIOBE_TOP_50_LANGUAGE_TERMS = {
    "python", "c++", "java", "c", "c#",
    "javascript", "golang","pascal", "visual basic",
    "fortran", "scratch", "rust", "php", "r",
    "matlab", "assembly", "cobol", "ruby", "prolog",
    "swift","classic visual basic",  "kotlin", "ada", "sas",
    "lisp", "haskell", "dart", "foxpro",
    "scala", "objective-c", "julia", "transact-sql",
    "vbscript", "pl/sql", "typescript", "gams", "solidity",
    "abap", "logo", "d", "bash", "powershell",
    "elixir", "rpg", "ml", "ladder logic", "awk",
    # common terms or language codes for the above, if different
    "cpp", "csharp", "delphi", "vb", "asm", "vbscript", "plsql",
    # skip because commonly found inside words
    # "sql", "perl", "lua",
}
# fmt: on
