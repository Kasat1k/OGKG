import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import ConvexHull, Delaunay

def max_histogram_area(heights):
    stack = []
    max_area = 0
    max_rect = (0, 0, 0)  
    index = 0

    while index < len(heights):
        if not stack or heights[index] >= heights[stack[-1]]:
            stack.append(index)
            index += 1
        else:
            while stack and heights[index] < heights[stack[-1]]:
                top_of_stack = stack.pop()
                area = (heights[top_of_stack] *
                        ((index - stack[-1] - 1) if stack else index))
                if area > max_area:
                    max_area = area
                    max_rect = (heights[top_of_stack], stack[-1] + 1 if stack else 0, index - (stack[-1] + 1 if stack else 0))

    while stack:
        top_of_stack = stack.pop()
        area = (heights[top_of_stack] *
                ((index - stack[-1] - 1) if stack else index))
        if area > max_area:
            max_area = area
            max_rect = (heights[top_of_stack], stack[-1] + 1 if stack else 0, index - (stack[-1] + 1 if stack else 0))

    return max_area, max_rect

def max_rectangle_area(matrix):
    if matrix.size == 0:
        return 0, None
    
    max_area = 0
    final_rect = None
    row_count = matrix.shape[0]
    column_count = matrix.shape[1]
    heights = [0] * column_count

    for row in range(row_count):
        for index in range(column_count):
            if matrix[row, index] == 1:
                heights[index] += 1
            else:
                heights[index] = 0

        current_area, (h, start_col, width) = max_histogram_area(heights)
        if current_area > max_area:
            max_area = current_area
            final_rect = (row - h + 1, start_col, row, start_col + width - 1)

    return max_area, final_rect

def visualize_matrix(matrix, rectangle, initial_hull_points, changed_zeros):
    fig, ax = plt.subplots()

    if rectangle:
        r = patches.Rectangle((rectangle[1], rectangle[0]), rectangle[3] - rectangle[1] + 1, rectangle[2] - rectangle[0] + 1, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(r)

    hull = ConvexHull(initial_hull_points)
    for simplex in hull.simplices:
        ax.plot(initial_hull_points[simplex, 1], initial_hull_points[simplex, 0], 'g-')

    unchanged_zeros = [point for point in np.argwhere(matrix == 0) if tuple(point) not in changed_zeros]
    unchanged_zeros = np.array(unchanged_zeros)
    ax.scatter(unchanged_zeros[:, 1], unchanged_zeros[:, 0], color='blue', s=10)

    plt.show()

np.random.seed()  
m = 100
n = 100
k = 50
matrix = np.random.choice([0, 1], size=(m, n), p=[k / (m*n), 1 - k / (m*n)])
print("Binary Matrix:")

initial_points = np.argwhere(matrix == 0)
initial_hull = ConvexHull(initial_points)
hull_path = Delaunay(initial_points)

changed_zeros = set()
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] == 1 and not hull_path.find_simplex((i, j)) >= 0:
            matrix[i, j] = 0
            changed_zeros.add((i, j))

largest_area, largest_rect = max_rectangle_area(matrix)

print("Largest rectangle area of 1s:", largest_area)

visualize_matrix(matrix, largest_rect, initial_points, changed_zeros)
