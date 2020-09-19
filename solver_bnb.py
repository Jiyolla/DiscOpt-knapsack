#!/usr/bin/python
# -*- coding: utf-8 -*-


from collections import namedtuple
import copy as cp
import numpy as np

Item = namedtuple("Item", ["index", "value", "weight"])


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

    # A Branch and Bound solution
    # with DFS branching
    # implemented by recursion

    taken = np.zeros(item_count, dtype=np.int32)
    best_value = 0
    best_taken = np.zeros(item_count, dtype=np.int32)

    def bnb(taken, i, remaining_capacity, value, opt_est):
        nonlocal best_value
        nonlocal best_taken
        if best_value > opt_est:
            return 0
        if i >= item_count:
            return value
        item = items[i]
        if item.weight <= remaining_capacity:
            taken[i] = 1
            v_take = bnb(
                taken,
                i + 1,
                remaining_capacity - item.weight,
                value + item.value,
                opt_est,
            )
        else:
            v_take = 0
        taken[i] = 0
        v_ntake = bnb(taken, i + 1, remaining_capacity,
                      value, opt_est - item.value)
        if best_value < v_take or best_value < v_ntake:
            if v_take > v_ntake:
                taken[i] = 1
                best_value = v_take
                best_taken = cp.copy(taken)
                return v_take
            else:
                taken[i] = 0
                best_value = v_ntake
                best_taken = cp.copy(taken)
                return v_ntake
        return best_value

    opt_est = np.sum(items, axis=0)[1]
    value = bnb(taken, 0, capacity, 0, opt_est)

    # prepare the solution in the specified output format
    output_data = str(value) + " " + str(1) + "\n"
    output_data += " ".join(map(str, best_taken))
    return output_data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
        )
