"""
Math and collision utilities.
"""
import math

def length(vec):
    return math.sqrt(vec[0]**2 + vec[1]**2)

def normalize(vec):
    l = length(vec)
    if l < 0.0001:
        return (0, 0)
    return (vec[0]/l, vec[1]/l)

def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def lerp(a, b, t):
    return a + (b - a) * t

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def rect_vs_rect(r1, r2):
    return (r1[0] < r2[0] + r2[2] and
            r1[0] + r1[2] > r2[0] and
            r1[1] < r2[1] + r2[3] and
            r1[1] + r1[3] > r2[1])

def circle_vs_rect(cx, cy, radius, rect):
    closest_x = clamp(cx, rect[0], rect[0] + rect[2])
    closest_y = clamp(cy, rect[1], rect[1] + rect[3])
    dist_x = cx - closest_x
    dist_y = cy - closest_y
    dist_sq = dist_x**2 + dist_y**2
    return dist_sq < radius**2

def circle_vs_circle(c1, r1, c2, r2):
    return distance(c1, c2) < (r1 + r2)
