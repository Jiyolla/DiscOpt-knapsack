#!/usr/bin/python
# -*- coding: utf-8 -*-

import cProfile
import timeit
from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])
Oracle_cache = namedtuple("Oracle_cache", ["n", "k"])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # DP implementation

    value = 0
    taken = [0] * len(items)

    table = [[0 for x in range(capacity + 1)] for x in range(item_count + 1)]

    start = timeit.default_timer()
    for i in range(1, item_count + 1):
        for j in range(0, capacity + 1):
            item = items[i - 1]
            if item.weight > j:
                table[i][j] = table[i - 1][j]
                continue
            # Value when taking the item
            v_take = item.value + table[i - 1][j - item.weight]
            table[i][j] = max(v_take, table[i - 1][j])
    end = timeit.default_timer()

    print(end - start)

    value = table[item_count][capacity]

    c_track = capacity
    for i in range(item_count, 0, -1):
        if table[i][c_track] != table[i - 1][c_track]:
            taken[i - 1] = 1
            c_track -= items[i - 1].weight
        else:
            taken[i - 1] = 0

    # prepare the solution in the specified output format
    output_data = str(value) + " " + str(1) + "\n"
    output_data += " ".join(map(str, taken))
    return output_data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        # cProfile.run('print(solve_it(input_data))')
        print(timeit.timeit('print(solve_it(input_data))', number=10, globals=globals()))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
        )
