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

    n = random.choice(table)
    try:
        index = names.index(n)
    except:
        index = 0
    return _select(names, tables, output, index)


def _get_weight(item):
    _, table = item
    return len(table)
