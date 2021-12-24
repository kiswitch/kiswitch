def sign(a: float) -> int:
    return (a > 0) - (a < 0)


def offset_polyline(polyline, offset: float):

    new_polyline = []

    for i in polyline:
        new_polyline.append([i[0] + (offset * sign(i[0])),
                            i[1] + (offset * sign(i[1]))])

    return new_polyline
