from math import dist
import random
import time

# Points are tuples ( data Point = Point Double Double )
# A list of points is a list of tuples

# cool things to test
# combinations from itertools
# generating list and then getting the minimun
# slices vs indexes

def generate_points(n):
    return [(random.uniform(-2 * n, 2 * n), random.uniform(-2 * n, 2 * n)) for _ in range(n)]


def measure_time(f, input):
    start = time.perf_counter()
    result = f(input)
    end = time.perf_counter()
    return end - start, result


def closest_pair_brute_force(points):
    closest_pair = (points[0], points[1])
    min_dist = float('inf')

    for i in range(len(points)):
        for k in range(i + 1, len(points)):
            distance = dist(points[i], points[k])
            if distance < min_dist:
                min_dist = distance
                closest_pair = (points[i], points[k])

    return closest_pair


def closest_pair_divide_and_conquer(points):
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return closest_pair_rec(px, py)


def closest_pair_rec(px, py):
    n = len(px)
    if n <= 3:
        return closest_pair_brute_force(px)
    mid = n // 2
    qx = px[:mid]
    rx = px[mid:]

    midpoint = px[mid][0]

    qy = [p for p in py if p[0] <= midpoint]
    ry = [p for p in py if p[0] > midpoint]

    (q0, q1) = closest_pair_rec(qx, qy)
    (r0, r1) = closest_pair_rec(rx, ry)

    delta = min(dist(q0, q1), dist(r0, r1))

    best_pair = (q0,q1) if dist(q0,q1) <= dist(r0, r1) else (r0, r1)

    s = [p for p in py if abs(p[0] - midpoint) < delta]

    for i in range(len(s)):
        for j in range(i + 1, min(i + 16, len(s))):
            d = dist(s[i], s[j])
            if d < delta:
                delta = d
                best_pair = (s[i], s[j])

    return best_pair


