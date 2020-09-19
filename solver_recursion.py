#!/usr/bin/python
# -*- coding: utf-8 -*-


import timeit
import cProfile
from collections import namedtuple
import copy

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

    # A "Top-down" dynamic programming with caching
    # The main bottleneck should be tracking the decision varaibles
    # Currently the decision variables are being forked every time we call sub
    # which is obviously inefficient.

    value = 0
    taken = [0] * len(items)
    caches = {}

    start = timeit.default_timer()
    def oracle(n, k):
        if n < 1:
            emptylist = []
            return 0, emptylist

        if Oracle_cache(n, k) in caches:
            return caches[Oracle_cache(n, k)]

        item = items[n - 1]
        if item.weight > k:
            res = oracle(n - 1, k)
            res[1].append(0)
            caches[Oracle_cache(n, k)] = copy.deepcopy(res)
            return res
        else:
            v_ntake, t_ntake = oracle(n - 1, k)
            v_take, t_take = oracle(n - 1, k - item.weight)
            v_take += item.value
            if v_take > v_ntake:
                t_take.append(1)
                caches[Oracle_cache(n, k)] = copy.deepcopy((v_take, t_take))
                return v_take, t_take
            else:
                t_ntake.append(0)
                caches[Oracle_cache(n, k)] = copy.deepcopy((v_ntake, t_ntake))
                return v_ntake, t_ntake

    value, taken = oracle(item_count, capacity)
    end = timeit.default_timer()
    print(end - start)

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
