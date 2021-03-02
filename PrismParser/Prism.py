import copy
import re
import time

"""
Usage:
    token_array = Prism.parse(code, lang_key, return_all, assign_mode)

Return:
    A token list, like
    [
        {
            'type': 'assign-left', 
            # order number of the tokens
            'no': 2, 
            # the start position in the code
            'position': 12, #
            # the length of the token content
            'length': 17, 
            'cotent': 'SHORT_DESCRIPTION',
            'alias': 'variable'
        }, ...
    ]
    
Parameters:
    [text]: string, code to be parsed
    [language]: string, language key
    [return_all]: boolean, to determine whether return all parsed tree, or just assignment expressions
    [assign_mode]: boolean, to determine whether return assign_right info or not
"""

RE_TYPE = re.compile('').__class__


def current_milli_time():
    return round(time.time() * 1000)


class Token:
    def __init__(self, token_type, content, alias=None, matched_str=None, position=None):
        self.type = token_type
        self.content = content
        self.alias = alias
        self.length = len(matched_str)
        self.position = position

    def __len__(self):
        return self.length

    @staticmethod
    def _text(content):
        if isinstance(content, list):
            s = ""
            for item in content:
                s += Token._text(item["content"])
            return s
        else:
            return content

    def toDict(self, assign_mode=False):
        return {
            "type": self.type,
            "content": Token._text(self.content) if assign_mode else self.content,
            "alias": self.alias,
            "length": self.length,
            "position": self.position
        }

    def __str__(self):
        return str(self.toDict())


class Node:
    def __init__(self, value=None, prev_sibling=None, next_sibling=None):
        self.value = value
        self.prev = prev_sibling
        self.next = next_sibling


class LinkedList:
    def __init__(self):
        head = Node()
        tail = Node(None, head, None)
        head.next = tail
        self.head = head
        self.tail = tail
        self.length = 0


class Prism:
    LanguagesPatterns = {}
    TokensOutputAdapter = {}
    AssignRightTokens = {}
    Plugins = {}

    class Util:
        uniqueId = 0

        @classmethod
        def getObjectId(cls, obj):
            if not ("__id" in obj):
                obj["__id"] = str(cls.uniqueId)
                cls.uniqueId += 1
            return obj["__id"]

    class Languages:
        # Traverse a language definition with Depth First Search
        @classmethod
        def DFS(cls, o, callback, key=None, visited=None):
            if visited is None:
                visited = {}
            keys = o.keys()
            getObjectId = Prism.Util.getObjectId
            for i in keys:
                callback(o, i, o[i], key or i)

                value: dict = o[i]
                obj_id = getObjectId(value)

                if visited.get(obj_id) is not None:
                    if isinstance(value, dict):
                        visited[obj_id] = True
                        cls.DFS(value, callback, None, visited)
                    elif isinstance(value, list):
                        visited[obj_id] = True
                        cls.DFS(value, callback, i, visited)

        @classmethod
        def insertBefore(cls, inside, before, insert, root=None):
            root = Prism.LanguagesPatterns if root is None else root
            grammar = root[inside]
            ret = {}
            keys = grammar.keys()
            for token in keys:
                if token is before:
                    for newToken in insert.keys():
                        ret[newToken] = insert[newToken]

                # Do not insert token which also occur in insert. See #1525
                if token not in insert:
                    ret[token] = grammar[token]

            old = root[inside]
            root[inside] = ret

            # type fo compatible
            def callback(obj, key, value, _type):
                if value is old and key is not inside:
                    obj[key] = ret

            cls.DFS(Prism.LanguagesPatterns, callback)

            return ret

        @staticmethod
        def extend(lang_id, ext_def):
            lang = copy.deepcopy(Prism.LanguagesPatterns[lang_id])
            lang.update(ext_def)
            return lang

    class Hooks:
        all = {}

        @classmethod
        def add(cls, name, callback):
            hooks = cls.all
            hooks[name] = [] if hooks[name] is None else hooks[name]
            hooks[name].push(callback)

        @classmethod
        def run(cls, name, env):
            callbacks = cls.all.get(name)

            if callbacks is None or len(callbacks) == 0:
                return
            for callback in callbacks:
                callback(env)

    @classmethod
    def _dft_rst_adapter(cls, env, language,assign_mode, return_all):
        right_allowed = Prism.AssignRightTokens.get(language)
        # default AssignRightTokens
        if right_allowed is None:
            right_allowed = {"operator": 1, "variable": 1, "unknown": 1, "regex": 1, "number": 1, "string": 1}

        def collect_assign_right(left_mark, temp_right):
            if temp_right is not None and len(temp_right) > 0:
                while len(temp_right) > 0 and \
                        (
                                temp_right[0]["type"] == "blank" or
                                (
                                        temp_right[0]["type"] == "operator"
                                        and (
                                                (temp_right[0]["content"][0]["content"] if isinstance(
                                                    temp_right[0]["content"], list) else temp_right[0][
                                                    "content"]) == "="
                                        )
                                )
                        ):
                    temp_right.pop(0)

                while len(temp_right) > 0 and \
                        (temp_right[len(temp_right) - 1]["type"] == "blank"):
                    temp_right.pop()

                if len(temp_right) > 0:
                    length = 0
                    content = ""
                    for t in temp_right:
                        t["merged"]=True
                        if isinstance(t["content"], list):
                            for i in t["content"]:
                                length += t["length"]
                                content += i["content"]
                        else:
                            length += t["length"]
                            content += t["content"]
                    left_mark["right"] = {
                        'type':'assign-right',
                        'content': content,
                        'length': length,
                        'position': temp_right[0]["position"],
                        'merged': len(temp_right)
                    }

        tokens = env["tokens"]

        if assign_mode:
            left_mark = None
            temp_right = None
            for token in tokens:
                collecting = left_mark is not None and temp_right is not None
                if token["type"] == "blank":
                    if collecting:
                        temp_right.append(token)
                    continue
                elif right_allowed.get(token["type"]) is not None:
                    if collecting:
                        temp_right.append(token)
                    continue
                else:
                    if collecting:
                        collect_assign_right(left_mark, temp_right)
                    left_mark = None
                    temp_right = None

                    if token["type"] == "assign-left":
                        left_mark = token
                        temp_right = []

            if left_mark is not None and temp_right is not None:
                collect_assign_right(left_mark, temp_right)

            adjusted = []
            for token in tokens:
                if token.get("merged") is None:
                    adjusted.append(token)
                    if token.get("right") is not None:
                        adjusted.append(token['right'])
                        del token['right']
            tokens = adjusted

        if not return_all:
            tokens = list(filter(lambda x: x["type"] == "assign-left" or x["type"] == "assign-right", tokens))

        return tokens

    @classmethod
    def parse(cls, text, language, return_all=True, assign_mode=True):
        """
        core parse function
        :param text: string, code to be parsed
        :param language: string, language key
        :param return_all: boolean, to determine whether return all parsed tree, or just assignment expressions
        :param assign_mode: boolean, to determine whether return assign_right info or not
        :return: token array
        """

        grammar = Prism.LanguagesPatterns.get(language)
        rst_filter = Prism.TokensOutputAdapter.get(language)
        if rst_filter is None:
            rst_filter = cls._dft_rst_adapter
        if grammar is None:
            return None

        start_time = current_milli_time()
        env = {
            "code": text,
            "grammar": grammar,
            "language": language
        }
        Prism.Hooks.run('before-tokenize', env)
        env["tokens"] = Prism.tokenize(text, grammar, 0, assign_mode)
        Prism.Hooks.run('after-tokenize', env)
        Prism.Hooks.run('complete', env)

        print(current_milli_time() - start_time, "ms")

        return rst_filter(env, language, assign_mode, return_all)

    @classmethod
    def tokenize(cls, text, grammar, start_pos=0, assign_mode=False):
        rest = grammar.get("rest")
        if rest is not None:
            for token in rest.keys():
                grammar[token] = rest.get(token)
            del grammar["rest"]

        tokenList = LinkedList()
        cls.addAfter(tokenList, tokenList.head, text)

        cls.matchGrammar(text, tokenList, grammar, tokenList.head, 0, None)

        return cls.toArray(tokenList, start_pos, assign_mode)

    @classmethod
    def addAfter(cls, lst, node, value):
        # assumes that node != list.tail && len(values) >= 0
        _next = node.next

        newNode = Node(value, node, _next)
        node.next = newNode
        _next.prev = newNode
        lst.length += 1

        return newNode

    @classmethod
    def removeRange(cls, lst, node, count):
        _next = node.next
        i = 0
        for i in range(0, count):
            if _next is not lst.tail:
                _next = _next.next
        node.next = _next
        _next.prev = node
        lst.length -= i

    @classmethod
    def toArray(cls, lst, start_pos=0, assign_mode=False):
        array = []
        node = lst.head.next
        _blank = re.compile(r"\S")
        while node is not lst.tail:
            array.append(node.value)
            node = node.next
        arr_len = len(array)
        for i in range(0, arr_len):
            if isinstance(array[i], str):
                array[i] = Token(
                    "unknown" if re.match(_blank, array[i]) is not None else "blank",
                    array[i],
                    None,
                    array[i],
                    (array[i - 1].position + array[i - 1].length) if isinstance(array[i - 1], Token)
                    else (
                        (array[i + 1].position + array[i + 1].length) if arr_len > i + 1 and isinstance(array[i + 1], Token)
                        else start_pos
                    )
                )
        return list(map(lambda x: x.toDict(assign_mode), array))

    @classmethod
    def matchPattern(cls, pattern, pos, text, lookbehind):
        index = -1
        match_str = None
        if text is not None:
            match = pattern.search(text, pos)
            if match is not None:
                index = match.regs[0][0]
                match_str = match[0]
                if lookbehind and len(match.regs) > 1:
                    # change the match to remove the text matched by the PrismParser lookbehind group
                    lookbehindLength = match.regs[1][1] - match.regs[1][0]
                    index += lookbehindLength
                    match_str = match_str[lookbehindLength:]

        return match_str, index

    @classmethod
    def matchGrammar(cls, text, token_list, grammar, start_node, start_pos, rematch=None):
        tail = token_list.tail
        items = grammar.items()
        for key, patterns in items:
            if not isinstance(patterns, list):
                grammar[key] = patterns = [patterns]

            for j, patternObj in enumerate(patterns):
                if rematch is not None and rematch.get("cause") == key + ',' + str(j):
                    return

                if not isinstance(patternObj, dict):
                    patterns[j] = patternObj = {
                        "pattern": patternObj
                    }

                inside = patternObj.get("inside")

                lookbehind = patternObj.get("lookbehind")
                lookbehind = False if lookbehind is None else lookbehind

                greedy = patternObj.get("greedy")
                greedy = False if greedy is None else greedy

                alias = patternObj.get("alias")

                __compiled__ = patternObj.get("__compiled__")

                if __compiled__ is None:
                    patternObj["__compiled__"] = True
                    if isinstance(patternObj.get("pattern"), str):
                        flag = 0 if patternObj.get("flag") is None else patternObj.get("flag")
                        patternObj["pattern"] = re.compile(patternObj.get("pattern"), flag)

                # get regex pattern
                pattern = patternObj.get("pattern")

                # if cant get pattern
                if not isinstance(pattern, RE_TYPE):
                    print("*** Not a valid pattern", grammar, key, j, patternObj)
                    continue

                currentNode = start_node
                pos = start_pos
                while currentNode is not tail:
                    if currentNode is start_node:
                        pass
                    else:
                        pos += len(currentNode.value)

                    currentNode = currentNode.next

                    if rematch is not None and pos >= rematch.get("reach"):
                        break

                    if token_list.length > len(text):
                        # Something went terribly wrong, ABORT, ABORT!
                        return

                    if isinstance(currentNode.value, Token):
                        continue

                    value = currentNode.value

                    removeCount = 1  # this is the to parameter of removeBetween

                    if greedy:
                        match_str, match_index = cls.matchPattern(pattern, pos, text, lookbehind)
                        if match_str is None:
                            break

                        pos_from = match_index
                        pos_to = match_index + len(match_str)
                        p = pos

                        # find the node that contains the match
                        p += len(currentNode.value)
                        while pos_from >= p:
                            currentNode = currentNode.next
                            p += len(currentNode.value)

                        # adjust pos (and p)
                        p -= len(currentNode.value)
                        pos = p

                        # the current node is a Token, then the match starts inside another Token, which is invalid
                        if isinstance(currentNode.value, Token):
                            continue

                        # find the last node which is affected by this match
                        k = currentNode
                        while k is not tail and (p < pos_to or isinstance(k.value, str)):
                            removeCount += 1
                            p += len(k.value)
                            k = k.next

                        removeCount -= 1

                        # replace with the new match
                        value = text[pos:p]
                        match_index -= pos
                    else:
                        match_str, match_index = cls.matchPattern(pattern, 0, value, lookbehind)
                        if match_str is None:
                            continue

                    pos_from = match_index

                    before = value[:pos_from]
                    after = value[pos_from + len(match_str):]

                    reach = pos + len(value)

                    if rematch is not None and reach > rematch.get("reach"):
                        rematch["reach"] = reach

                    removeFrom = currentNode.prev

                    if before:
                        removeFrom = cls.addAfter(token_list, removeFrom, before)
                        pos += len(before)

                    cls.removeRange(token_list, removeFrom, removeCount)

                    wrapped = Token(key, cls.tokenize(match_str, inside, pos) if inside else match_str,
                                    alias, match_str, pos)
                    currentNode = cls.addAfter(token_list, removeFrom, wrapped)

                    if after:
                        cls.addAfter(token_list, currentNode, after)

                    if removeCount > 1:
                        # at least one Token object was removed, so we have to do some rematching
                        # this can only happen if the current pattern is greedy

                        nestedRematch = {
                            "cause": key + ',' + str(j),
                            "reach": reach
                        }
                        cls.matchGrammar(text, token_list, grammar, currentNode.prev, pos, nestedRematch)

                        # the reach might have been extended because of the rematching
                        if rematch is not None and nestedRematch.get("reach") > rematch.get("reach"):
                            rematch["reach"] = nestedRematch.get("reach")


# compatible with old version
Prism.util = Prism.Util
Prism.languages = Prism.Languages
Prism.plugins = Prism.Plugins
Prism.hooks = Prism.Hooks
Prism.Token = Token

__all__ = ["Prism"]
