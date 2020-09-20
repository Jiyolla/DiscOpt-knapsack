#!/usr/bin/python
# -*- coding: utf-8 -*-

import cProfile
import configparser
import importlib
import numpy
import timeit
from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])


def set_kernel(kernel):
    config = configparser.ConfigParser()
    with open('setting.ini', 'r') as f:
        config.read_file(f)
        kernels = config['Supported Kernels']
        if kernel not in kernels:
            kernels[kernel] = str(len(kernels))
        config['Default Kernel'] = {'name': kernel,
                                    'code': kernels[kernel]}
        with open('setting.ini', 'w') as configfile:
            config.write(configfile)


def solve_it(input_data):
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

    config = configparser.ConfigParser()
    solver = None
    value = 0
    taken = numpy.zeros(item_count, dtype=numpy.int32)
    with open('setting.ini') as f:
        config.read_file(f)
        kernel = config['Default Kernel']['name']
        compute = importlib.import_module(kernel)
        prof = cProfile.Profile()
        value, taken = prof.runcall(compute.solve, item_count, capacity, items)
        prof.print_stats(1)
        num_run = [1, 3, 5, 10]
        for i in num_run:
            avg = (
                timeit.timeit(
                    'compute.solve(item_count, capacity, items)', number=i, globals=locals()
                )
                / i
            )
            print(f'Average of {i} run(s): {avg}')


    # prepare the solution in the specified output format
    output_data = f'{value} 1\n'
    output_data += " ".join(map(str, taken))
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
