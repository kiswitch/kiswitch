#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

from math import sqrt

from KiSwitch.deps_path import deps_path

with deps_path():
    from KicadModTree.Vector import Vector2D


def norm_vector(v):
    source_v = Vector2D(v)
    radius, angle = source_v.to_polar()
    return source_v / radius if radius != 0 else Vector2D(0, 0)

    return new_polyline


def offset_poly(poly: list, offset: float, origin: Vector2D = Vector2D(0, 0), outer_ccw=True):
    new_poly = []
    outer_ccw = 1 if outer_ccw else -1
    closed = poly[0] == poly[-1]

    if closed:
        poly.pop()

    num_points = len(poly)

    for curr in range(num_points):
        curr_point = Vector2D(poly[curr]) - origin
        prev_point = Vector2D(poly[(curr + num_points - 1) % num_points]) - origin
        next_point = Vector2D(poly[(curr + 1) % num_points]) - origin

        vn = next_point - curr_point
        vnn = norm_vector(vn)
        nnn = Vector2D([vnn.y, -vnn.x])

        vp = curr_point - prev_point
        vpn = norm_vector(vp)
        npn = Vector2D([vpn.y * outer_ccw, -vpn.x * outer_ccw])

        bis = (nnn + npn) * outer_ccw
        bisn = norm_vector(bis)

        bislen = offset / sqrt(1 + nnn.x * npn.x + nnn.y * npn.y)

        new_point = (curr_point + (bisn * bislen)) + origin

        new_poly.append(new_point.round_to(0.001))

    if closed:
        new_poly.append(new_poly[0])

    return new_poly
