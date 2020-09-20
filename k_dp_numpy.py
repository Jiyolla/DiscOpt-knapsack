#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy


def solve(item_count, capacity, items):

    # DP implementation with vectorized computation by numpy
    table = numpy.zeros((item_count + 1, capacity + 1), dtype=numpy.int32)

    for i in range(1, item_count + 1):
        item = items[i - 1]
        threshold = min(item.weight, capacity + 1)
        table[i][0:threshold] = table[i - 1][0:threshold]
        j = numpy.arange(capacity + 1 - threshold) + threshold
        j_m_iw = j - item.weight
        v_take = item.value + table[i - 1][j_m_iw]
        table[i][threshold:capacity + 1] = numpy.maximum(
            v_take, table[i - 1][threshold:capacity + 1]
        )

    value = table[item_count][capacity]
    taken = numpy.zeros(item_count, dtype=numpy.int32)
    remaining_capacity = capacity
    for i in range(item_count, 0, -1):
        if table[i][remaining_capacity] != table[i - 1][remaining_capacity]:
            taken[i - 1] = 1
            remaining_capacity -= items[i - 1].weight
        else:
            taken[i - 1] = 0

    return value, taken
