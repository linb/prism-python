import re
from PrismParser.Prism import *

specialEscape = {
    "pattern": r"\\[\\(){}[\]^$+*?|.]",
    "alias": 'escape'
}
escape = r"\\(?:x[\da-fA-F]{2}|u[\da-fA-F]{4}|u\{[\da-fA-F]+\}|c[a-zA-Z]|0[0-7]{0,2}|[123][0-7]{2}|.)"
charClass = {
    "pattern": r"\.|\\[wsd]|\\p{[^{}]+}",
    "flag": re.I,
    "alias": 'class-name'
}
charClassWithoutDot = {
    "pattern": r"\\[wsd]|\\p{[^{}]+}",
    "flag": re.I,
    "alias": 'class-name'
}

rangeChar = '(?:[^\\\\-]|' + escape + ')'
_range = rangeChar + '-' + rangeChar

# the name of a capturing group
groupName = {
    "pattern": r"(<|')[^<>']+(?=[>']$)",
    "lookbehind": True,
    "alias": 'variable'
}

Prism.LanguagesPatterns["regex"] = {
    'charset': {
        "pattern": r"((?:^|[^\\])(?:\\\\)*)\[(?:[^\\\]]|\\[\s\S])*\]",
        "lookbehind": True,
        "inside": {
            'charset-negation': {
                "pattern": r"(^\[)\^",
                "lookbehind": True,
                "alias": 'operator'
            },
            'charset-punctuation': {
                "pattern": r"^\[|\]$",
                "alias": 'punctuation'
            },
            'range': {
                "pattern": _range,
                "inside": {
                    'escape': escape,
                    'range-punctuation': {
                        "pattern": r"-",
                        "alias": 'operator'
                    }
                }
            },
            'special-escape': specialEscape,
            'charclass': charClassWithoutDot,
            'escape': escape
        }
    },
    'special-escape': specialEscape,
    'charclass': charClass,
    'backreference': [
        {
            # a backreference which is not an octal escape
            "pattern": r"\\(?![123][0-7]{2})[1-9]",
            "alias": 'keyword'
        },
        {
            "pattern": r"\\k<[^<>']+>",
            "alias": 'keyword',
            "inside": {
                'group-name': groupName
            }
        }
    ],
    'anchor': {
        "pattern": r"[$^]|\\[ABbGZz]",
        "alias": 'function'
    },
    'escape': escape,
    'group': [
        {
            # https://docs.oracle.com/javase/10/docs/api/java/util/regex/Pattern.html
            # https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference?view=netframework-4.7.2#grouping-constructs

            # (), (?<name>), (?'name'), (?>), (?:), (?=), (?!), (?<=), (?<!), (?is-m), (?i-m:)
            "pattern": r"\((?:\?(?:<[^<>']+>|'[^<>']+'|[>:]|<?[=!]|[idmnsuxU]+(?:-[idmnsuxU]+)?:?))?",
            "alias": 'punctuation',
            "inside": {
                'group-name': groupName
            }
        },
        {
            "pattern": r"\)",
            "alias": 'punctuation'
        }
    ],
    'quantifier': {
        "pattern": r"(?:[+*?]|\{\d+(?:,\d*)?\})[?+]?",
        "alias": 'number'
    },
    'alternation': {
        "pattern": r"\|",
        "alias": 'keyword'
    }
}

__all__ = []
