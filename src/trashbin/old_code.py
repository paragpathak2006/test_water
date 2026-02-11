import numpy as np
from vhacdx import compute_vhacd
# ----------------------------
# Simple concave shape (L-block)
# ----------------------------
vertices1 = np.array([
    [0,0,0], [2,0,0], [2,1,0], [1,1,0], [1,2,0], [0,2,0],   # bottom L
    [0,0,1], [2,0,1], [2,1,1], [1,1,1], [1,2,1], [0,2,1]
], dtype=np.float64)

faces1 = np.array([
    [0,1,2],[0,2,3],[0,3,5],[3,4,5],        # bottom
    [6,7,8],[6,8,9],[6,9,11],[9,10,11],     # top
    [0,1,7],[0,7,6],
    [1,2,8],[1,8,7],
    [2,3,9],[2,9,8],
    [3,4,10],[3,10,9],
    [4,5,11],[4,11,10],
    [5,0,6],[5,6,11]
], dtype=np.uint32)

# ----------------------------
# Convex decomposition options
# ----------------------------
part1s = compute_vhacd(vertices1, 
                       faces1, 
                       maxConvexHulls=4, 
                       resolution=10000)

print("Convex parts:", len(part1s))