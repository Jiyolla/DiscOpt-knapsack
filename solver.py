#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import cProfile
import configparser
import importlib
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


def solve_it(input_data, profile=False):
    # Parse the input
    lines = input_data.split("\n")
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # Load kernel
    with open('setting.ini') as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        kernel = config['Default Kernel']['name']
        solver = importlib.import_module(kernel)

        # Compute with kernel
        if profile:
            print(f'Running with kernel={kernel}\n')
            prof = cProfile.Profile()
            value, taken = prof.runcall(solver.solve, item_count, capacity, items)
            prof.print_stats(1)
            print(f'value = {value}\ntaken = {taken}')
            num_run = [1, 3, 5, 10]
            for i in num_run:
                avg = (
                    timeit.timeit(
                        'solver.solve(item_count, capacity, items)', number=i, globals=locals()
                    )
                    / i
                )
                print(f'Average of {i} run(s): {avg}')
        else:
            value, taken = solver.solve(item_count, capacity, items)

    # prepare the solution in the specified output format
    output_data = f'{value} 1\n'
    output_data += " ".join(map(str, taken))
    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solve knapsack problems')
    parser.add_argument('data_file_name', metavar='Data_File_Path', type=str, # nargs='+',
                        help='data file path')
    parser.add_argument('-k', dest='kernel', action='store',
                        help='Set default kernel')
    parser.add_argument('-p', dest='profile', action='store_true',
                        help='Show profiling stats')

    args = parser.parse_args()
    # set kernel if specified
    if args.kernel:
        set_kernel(args.kernel.replace('.py', ''))
    with open(args.data_file_name, "r") as input_data_file:
        print(solve_it(input_data_file.read(), args.profile))
