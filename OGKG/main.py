import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def generate_random_points():
    N = np.random.randint(10, 101) 
    return np.random.rand(N, 2) * 100

def plot_points_and_hull(points, hull):
    plt.figure(figsize=(8, 6))
    plt.plot(points[:, 0], points[:, 1], 'o', label='Points')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
    plt.legend()

def check_if_inside(points, rect):
    x_min, y_min, x_max, y_max = rect
    inside = np.any((points[:, 0] > x_min) & (points[:, 0] < x_max) & (points[:, 1] > y_min) & (points[:, 1] < y_max))
    return not inside

def find_largest_rectangle(points):
    max_area = 0
    best_rect = None
    num_points = len(points)
    
    for i in range(num_points):
        for j in range(i + 1, num_points):
            x_min, y_min = np.minimum(points[i], points[j])
            x_max, y_max = np.maximum(points[i], points[j])
            rect = (x_min, y_min, x_max, y_max)
            area = (x_max - x_min) * (y_max - y_min)
            if area > max_area and check_if_inside(points, rect):
                max_area = area
                best_rect = rect
                
    return best_rect, max_area

def plot_rectangle(rect):
    if rect:
        x_min, y_min, x_max, y_max = rect
        plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], 'r-', label='Max Area Rectangle')
        plt.legend()

points = generate_random_points()
hull = ConvexHull(points)
plot_points_and_hull(points, hull)

rect, area = find_largest_rectangle(points)
plot_rectangle(rect)
plt.title(f'Best Rectangle Area: {area:.2f}')
plt.grid(True)
plt.show()
