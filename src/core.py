import re
import collections


def relocate(target):
    result = {}
    content_tree = nest(target)
    for content in content_tree:
        merge(result, content)
    trans(result)
    return result


def nest(target):
    content_tree = []
    for key, value in target.items():
        stair_key = key.split('.')
        init = True
        before = {}
        for step in reversed(stair_key):
            temp = {}
            if init:
                init = False
                before[step] = value
                if len(stair_key) == 1:
                    temp = before
                continue
            temp[step] = before
            before = temp
        content_tree.append(temp)
    return content_tree


def merge(base, other):
    for k, v in other.items():
        if isinstance(v, collections.Mapping) and k in base:
            merge(base[k], v)
        else:
            base[k] = v


pattern = re.compile(r'\[\d+\]')


def trans(base):
    temp = []
    for k, v in base.items():
        if isinstance(v, collections.Mapping) and k in base:
            trans(v)
            result = pattern.match(k)
            if result:
                temp.append((k, v))
    temp.sort(key=lambda x: x[0])
    return [value for _, value in temp]
