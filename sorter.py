import random

# this is `working`
# DO NOT TOUCH !


def improvedOrder(now, before):
    data = []
    for x in now:
        cantbewith = set()
        for table in before:
            for i in range(0, len(table)):
                if x == table[i]:
                    index = i + 1
                    if i + 1 == len(table):
                        index = 0

                    if table[index] in now:
                        cantbewith.add(table[index])
        data.append((x, cantbewith))

    notdata = []
    for y in data:
        x, z = y
        table = []
        for i in now:
            if (not i in z) and i != x:
                table.append(i)
        if table == []:
            w = now.copy()
            w.remove(x)
            table = w
        notdata.append((x, table))

    notdata.sort(key=_get_weight)

    names, tables = zip(*notdata)
    return _select(list(names), list(tables), [], 0)


def _select(names, tables, output, id):
    name = names[id]
    table = tables[id]
    output.append(name)
    tables.pop(id)
    names.pop(id)
    if len(names) == 0:
        return output
    elif len(names) == 1:
        output.append(names[0])
        return output

    while len(table) > 0:
        n = random.choice(table)
        try:
            index = names.index(n)
        except:
            table.remove(n)
            continue
        else:
            return _select(names, tables, output, index)
    return _select(names, tables, output, 0)


def _get_weight(item):
    _, table = item
    return len(table)


if __name__ == "__main__":
    before = [
        ["a", "e", "f", "d", "c"],
        ["e", "b", "d", "a", "c"],
        ["f", "c", "b", "a", "e"],
        ["e", "b", "d"],
    ]
    now = ["a", "b", "c", "d"]
    print(improvedOrder(now, before))
