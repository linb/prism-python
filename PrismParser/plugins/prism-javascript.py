import re
from PrismParser.Prism import *

__import__("PrismParser.plugins.prism-regex")

Prism.LanguagesPatterns["javascript"] = Prism.Languages.extend('clike', {
    'class-name': [
        Prism.LanguagesPatterns["clike"]['class-name'],
        {
            "pattern": r"(^|[^$\w\xA0-\uFFFF])(?!\s)[_$A-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\.(?:prototype|constructor))",
            "lookbehind": True
        }
    ],
    'keyword': [
        {
            "pattern": r"((?:^|})\s*)catch\b",
            "lookbehind": True
        },
        {
            "pattern": r"(^|[^.]|\.\.\.\s*)\b(?:as|async(?=\s*(?:function\b|\(|[$\w\xA0-\uFFFF]|$))|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally(?=\s*(?:\{|$))|for|from(?=\s*(?:['\"]|$))|function|(?:get|set)(?=\s*(?:[\[$\w\xA0-\uFFFF]|$))|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)\b",
            "lookbehind": True
        }
    ],
    # Allow for all non-ASCII characters (See http://stackoverflow.com/a/2008444)
    'function': r"#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*(?:\.\s*(?:apply|bind|call)\s*)?\()",
    'number': r"\b(?:(?:0[xX](?:[\dA-Fa-f](?:_[\dA-Fa-f])?)+|0[bB](?:[01](?:_[01])?)+|0[oO](?:[0-7](?:_[0-7])?)+)n?|(?:\d(?:_\d)?)+n|NaN|Infinity)\b|(?:\b(?:\d(?:_\d)?)+\.?(?:\d(?:_\d)?)*|\B\.(?:\d(?:_\d)?)+)(?:[Ee][+-]?(?:\d(?:_\d)?)+)?",
    'operator': r"--|\+\+|\*\*=?|=>|&&=?|\|\|=?|[!=]==|<<=?|>>>?=?|[-+*/%&|^!=<>]=?|\.{3}|\?\?=?|\?\.?|[~:]"
})

Prism.LanguagesPatterns["javascript"]['class-name'][0]["pattern"] = r"(\b(?:class|interface|extends|implements|instanceof|new)\s+)[\w.\\]+"

Prism.Languages.insertBefore('javascript', 'keyword', {
    'regex': {
        "pattern": r"((?:^|[^$\w\xA0-\uFFFF.\"'\])\s]|\b(?:return|yield))\s*)\/(?:\[(?:[^\]\\\r\n]|\\.)*]|\\.|[^/\\\[\r\n])+\/[gimyus]{0,6}(?=(?:\s|\/\*(?:[^*]|\*(?!\/))*\*\/)*(?:$|[\r\n,.;:})\]]|\/\/))",
        "lookbehind": True,
        "greedy": True,
        "inside": {
            'regex-source': {
                "pattern": r"^(\/)[\s\S]+(?=\/[a-z]*$)",
                "lookbehind": True,
                "alias": 'language-regex',
                #"inside": Prism.LanguagesPatterns["regex"]
            },
            'regex-flags': r"[a-z]+$",
            'regex-delimiter': r"^\/|\/$"
        }
    },
    # This must be declared before keyword because we use "function" inside the look-forward
    'function-variable': {
        "pattern": r"#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[.$\w\xA0-\uFFFF])*(?=\s*[=:]\s*(?:async\s*)?(?:\bfunction\b|(?:\((?:[^()]|\([^()]*\))*\)|(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)\s*=>))",
        "alias": 'function'
    },
    'parameter': [
        {
            "pattern": r"(function(?:\s+(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)?\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\))",
            "lookbehind": True,
            "inside": Prism.LanguagesPatterns["javascript"]
        },
        {
            "pattern": r"(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*=>)",
            "flag": re.I,
            "inside": Prism.LanguagesPatterns["javascript"]
        },
        {
            "pattern": r"(\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*=>)",
            "lookbehind": True,
            "inside": Prism.LanguagesPatterns["javascript"]
        },
        {
            "pattern": r"((?:\b|\s|^)(?!(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)(?![$\w\xA0-\uFFFF]))(?:(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*)\(\s*|\]\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*\{)",
            "lookbehind": True,
            "inside": Prism.LanguagesPatterns["javascript"]
        }
    ],
    'constant': r"\b[A-Z](?:[A-Z_]|\dx?)*\b"
})

Prism.Languages.insertBefore('javascript', 'string', {
    'template-string': {
        "pattern": r"`(?:\\[\s\S]|\${(?:[^{}]|{(?:[^{}]|{[^}]*})*})+}|(?!\${)[^\\`])*`",
        "greedy": True,
        "inside": {
            'template-punctuation': {
                "pattern": r"^`|`$",
                "alias": 'string'
            },
            'interpolation': {
                "pattern": r"((?:^|[^\\])(?:\\{2})*)\${(?:[^{}]|{(?:[^{}]|{[^}]*})*})+}",
                "lookbehind": True,
                "inside": {
                    'interpolation-punctuation': {
                        "pattern": r"^\${|}$",
                        "alias": 'punctuation'
                    },
                    "rest": Prism.LanguagesPatterns["javascript"]
                }
            },
            'string': r"[\s\S]+"
        }
    }
})

if Prism.LanguagesPatterns.get("markup") is not None:
    Prism.LanguagesPatterns["markup"]["tag"]["addInlined"]('script', 'javascript')

Prism.LanguagesPatterns["js"] = Prism.LanguagesPatterns["javascript"]

__all__ = []
