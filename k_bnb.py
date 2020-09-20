#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy as cp
import numpy as np


def solve(item_count, capacity, items):

    # A Branch and Bound solution
    # with DFS branching
    # implemented by recursion

    taken = np.zeros(item_count, dtype=np.int32)
    best_value = 0
    best_taken = None

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
                best_taken = cp.deepcopy(taken)
                return v_take
            else:
                taken[i] = 0
                best_value = v_ntake
                best_taken = cp.deepcopy(taken)
                return v_ntake
        return best_value

    opt_est = np.sum(items, axis=0)[1]
    value = bnb(taken, 0, capacity, 0, opt_est)

    return value, best_taken
