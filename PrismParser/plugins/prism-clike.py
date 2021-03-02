import re
from PrismParser.Prism import *

Prism.LanguagesPatterns["clike"] = {
    'comment': [
        {
            "pattern": r"(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)",
            "lookbehind": True,
            "greedy": True
        },
        {
            "pattern": r"(^|[^\\:])\/\/.*",
            "lookbehind": True,
            "greedy": True
        }
    ],
    'string': {
        "pattern": r"([\"'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1",
        "greedy": True
    },
    'assign-left': r"#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[.$\w\xA0-\uFFFF])*(?=\s*[=][^=>])",
    'class-name': {
        "pattern": r"(\b(?:class|interface|extends|implements|trait|instanceof|new)\s+|\bcatch\s+\()[\w.\\]+/",
        "flag": re.I,
        "lookbehind": True,
        "inside": {
            'punctuation': "[.\\]"
        }
    },
    'keyword': r"\b(?:if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b",
    'boolean': r"\b(?:true|false)\b",
    'function': r"\w+(?=\()",
    'number': {
        "pattern": r"\b0x[\da-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?",
        "flag": re.I
    },
    'operator': r"[<>]=?|[!=]=?=?|--?|\+\+?|&&?|\|\|?|[?*/~^%]",
    'punctuation': r"[{}[\];(),.:]",
    'enter': r"[\r\n]+",
    'blank': r"[ \f\t\v]+"
}
__all__ = []

