#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def solve(item_count, capacity, items):
    # DP implementation
    value = 0
    taken = np.zeros(item_count, dtype=np.int32)
    table = [[0 for x in range(capacity + 1)] for x in range(item_count + 1)]

    for i in range(1, item_count + 1):
        item = items[i - 1]
        threshold = min(item.weight, capacity + 1)
        for j in range(0, threshold):
            table[i][j] = table[i - 1][j]
        for j in range(threshold, capacity + 1):
            # Value when taking the item
            v_take = item.value + table[i - 1][j - item.weight]
            table[i][j] = max(v_take, table[i - 1][j])

    value = table[item_count][capacity]

    c_track = capacity
    for i in range(item_count, 0, -1):
        if table[i][c_track] != table[i - 1][c_track]:
            taken[i - 1] = 1
            c_track -= items[i - 1].weight
        else:
            taken[i - 1] = 0

    return value, taken
