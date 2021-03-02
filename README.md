It's a python syntax parser based on prismjs - create a parse tree for 246 languages.

Input code:
```javascript
const Prism = require('prismjs');
const loadLanguages = require('prismjs/components/');
loadLanguages(['haml']);

// The code snippet you want to highlight, as a string
const code = `= ['hi', 'there', 'reader!'].join " "`;

// Returns a highlighted HTML string
const html = Prism.highlight(code, Prism.languages.haml, 'haml');
```

Output parse tree:
```
0 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 0}
1 {'type': 'keyword', 'content': 'const', 'alias': None, 'length': 5, 'position': 1}
2 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 6}
3 {'type': 'assign-left', 'content': 'Prism', 'alias': None, 'length': 5, 'position': 7}
4 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 12}
5 {'type': 'operator', 'content': '=', 'alias': None, 'length': 1, 'position': 13}
6 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 14}
7 {'type': 'function', 'content': 'require', 'alias': None, 'length': 7, 'position': 15}
8 {'type': 'punctuation', 'content': '(', 'alias': None, 'length': 1, 'position': 22}
9 {'type': 'string', 'content': "'prismjs'", 'alias': None, 'length': 9, 'position': 23}
10 {'type': 'punctuation', 'content': ')', 'alias': None, 'length': 1, 'position': 32}
11 {'type': 'punctuation', 'content': ';', 'alias': None, 'length': 1, 'position': 33}
12 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 34}
13 {'type': 'keyword', 'content': 'const', 'alias': None, 'length': 5, 'position': 35}
14 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 40}
15 {'type': 'assign-left', 'content': 'loadLanguages', 'alias': None, 'length': 13, 'position': 41}
16 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 54}
17 {'type': 'operator', 'content': '=', 'alias': None, 'length': 1, 'position': 55}
18 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 56}
19 {'type': 'function', 'content': 'require', 'alias': None, 'length': 7, 'position': 57}
20 {'type': 'punctuation', 'content': '(', 'alias': None, 'length': 1, 'position': 64}
21 {'type': 'string', 'content': "'prismjs/components/'", 'alias': None, 'length': 21, 'position': 65}
22 {'type': 'punctuation', 'content': ')', 'alias': None, 'length': 1, 'position': 86}
23 {'type': 'punctuation', 'content': ';', 'alias': None, 'length': 1, 'position': 87}
24 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 88}
25 {'type': 'function', 'content': 'loadLanguages', 'alias': None, 'length': 13, 'position': 89}
26 {'type': 'punctuation', 'content': '(', 'alias': None, 'length': 1, 'position': 102}
27 {'type': 'punctuation', 'content': '[', 'alias': None, 'length': 1, 'position': 103}
28 {'type': 'string', 'content': "'haml'", 'alias': None, 'length': 6, 'position': 104}
29 {'type': 'punctuation', 'content': ']', 'alias': None, 'length': 1, 'position': 110}
30 {'type': 'punctuation', 'content': ')', 'alias': None, 'length': 1, 'position': 111}
31 {'type': 'punctuation', 'content': ';', 'alias': None, 'length': 1, 'position': 112}
32 {'type': 'enter', 'content': '\n\n', 'alias': None, 'length': 2, 'position': 113}
33 {'type': 'comment', 'content': '// The code snippet you want to highlight, as a string', 'alias': None, 'length': 54, 'position': 115}
34 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 169}
35 {'type': 'keyword', 'content': 'const', 'alias': None, 'length': 5, 'position': 170}
36 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 175}
37 {'type': 'assign-left', 'content': 'code', 'alias': None, 'length': 4, 'position': 176}
38 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 180}
39 {'type': 'operator', 'content': '=', 'alias': None, 'length': 1, 'position': 181}
40 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 182}
41 {'type': 'template-string', 'content': '`= [\'hi\', \'there\', \'reader!\'].join " "`', 'alias': None, 'length': 39, 'position': 183}
42 {'type': 'punctuation', 'content': ';', 'alias': None, 'length': 1, 'position': 222}
43 {'type': 'enter', 'content': '\n\n', 'alias': None, 'length': 2, 'position': 223}
44 {'type': 'comment', 'content': '// Returns a highlighted HTML string', 'alias': None, 'length': 36, 'position': 225}
45 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 261}
46 {'type': 'keyword', 'content': 'const', 'alias': None, 'length': 5, 'position': 262}
47 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 267}
48 {'type': 'assign-left', 'content': 'html', 'alias': None, 'length': 4, 'position': 268}
49 {'type': 'assign-right', 'content': 'Prism', 'length': 5, 'position': 275, 'merged': 1}
50 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 272}
51 {'type': 'operator', 'content': '=', 'alias': None, 'length': 1, 'position': 273}
52 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 274}
53 {'type': 'punctuation', 'content': '.', 'alias': None, 'length': 1, 'position': 280}
54 {'type': 'function', 'content': 'highlight', 'alias': None, 'length': 9, 'position': 281}
55 {'type': 'punctuation', 'content': '(', 'alias': None, 'length': 1, 'position': 290}
56 {'type': 'unknown', 'content': 'code', 'alias': None, 'length': 4, 'position': 291}
57 {'type': 'punctuation', 'content': ',', 'alias': None, 'length': 1, 'position': 295}
58 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 296}
59 {'type': 'unknown', 'content': 'Prism', 'alias': None, 'length': 5, 'position': 297}
60 {'type': 'punctuation', 'content': '.', 'alias': None, 'length': 1, 'position': 302}
61 {'type': 'unknown', 'content': 'languages', 'alias': None, 'length': 9, 'position': 303}
62 {'type': 'punctuation', 'content': '.', 'alias': None, 'length': 1, 'position': 312}
63 {'type': 'unknown', 'content': 'haml', 'alias': None, 'length': 4, 'position': 313}
64 {'type': 'punctuation', 'content': ',', 'alias': None, 'length': 1, 'position': 317}
65 {'type': 'blank', 'content': ' ', 'alias': None, 'length': 1, 'position': 318}
66 {'type': 'string', 'content': "'haml'", 'alias': None, 'length': 6, 'position': 319}
67 {'type': 'punctuation', 'content': ')', 'alias': None, 'length': 1, 'position': 325}
68 {'type': 'punctuation', 'content': ';', 'alias': None, 'length': 1, 'position': 326}
69 {'type': 'enter', 'content': '\n', 'alias': None, 'length': 1, 'position': 327}
70 {'type': 'blank', 'content': '    ', 'alias': None, 'length': 4, 'position': 328}
```
It can support all 246 languages in PrismJS. Easy to convert PrismJS language component settings from javascript to python. Here, 4 languages have been converted: Javscript, Python, Bash and Clike.
