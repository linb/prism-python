from PrismParser import Prism


def test_parse(code, lang, return_all=True, assign_mode=True, log=False):
    arr = Prism.parse(code, lang, return_all, assign_mode)
    if log:
        for i, token in enumerate(arr):
            print(i, token)


if __name__ == '__main__':
    code = """
const Prism = require('prismjs');
const loadLanguages = require('prismjs/components/');
loadLanguages(['haml']);

// The code snippet you want to highlight, as a string
const code = `= ['hi', 'there', 'reader!'].join " "`;

// Returns a highlighted HTML string
const html = Prism.highlight(code, Prism.languages.haml, 'haml');
    """

    print("start")

    # test_parse(code, lang, return_all=True, assign_mode=True, log=False):

    # test_parse(code, "clike")
    print("-----return assignment with string/number right part----------")
    test_parse(code, "javascript", False, True, True)
    print("-----return assignment without right part----------")
    test_parse(code, "javascript", False, False, True)
    print("-----return all token with assignment----------")
    test_parse(code, "javascript", True, True, True)
    print("-----return all token without assignment----------")
    test_parse(code, "javascript", True, False, True)

    print("end")
