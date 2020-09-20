#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import copy

Oracle_cache = namedtuple("Oracle_cache", ["n", "k"])


def solve(item_count, capacity, items):

    # A "Top-down" dynamic programming with caching
    # The main bottleneck should be tracking the decision varaibles
    # Currently the decision variables are being forked every time we call sub
    # which is obviously inefficient.

    value = 0
    taken = [0] * len(items)
    caches = {}

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

    return value, taken
