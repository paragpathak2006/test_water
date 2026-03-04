import sys

sys.path.append("build")

import numpy as np
import cgal_module
import trimesh
from io_path import BASE_DIR


def split_by_count(arr, counts):
    # arr = np.array([10, 20, 30, 40, 50, 60, 70])
    # counts = np.array([2, 3, 2])

    # Compute split indices (cumulative sum, excluding last)
    indices = np.cumsum(counts)[:-1]

    result = np.split(arr, indices)

    return result


# PYBIND11_MODULE(cgal_module, m) {
#     test(m);

#     get_cgal_version(m);
#     print_cgal_version(m);

#     self_difference(m);
#     self_difference_and_split(m);
#     self_difference_split_intersection_difference(m);
# }

# Load the original mesh
mesh = trimesh.load(BASE_DIR / "0. solid-volume.stl")

# pts = [(0,0), (1,0), (0,1), (0.2,0.2)]
print("Test 1 : ", cgal_module.test())
print("Test 2 : CGAL version : ", cgal_module.get_cgal_version())
print("Test 3 : cout CGAL version : ")
cgal_module.print_cgal_version()

# To ensure contiguous memory
vertices = np.ascontiguousarray(mesh.vertices, dtype=np.float64)
faces = np.ascontiguousarray(mesh.faces, dtype=np.int32)

# print("cgal_module.convex_hull")
# [v,n,nv,nf] = cgal_module.convex_hull(vertices, faces)

print("cgal_module.self_difference_split_intersection_difference")
[v, n, nv, nf] = cgal_module.self_difference_split_intersection_difference(
    vertices, faces
)

print("cgal_module.self_difference_split_intersection_difference python output")
print(
    "vertices\n",
    "vlen=",
    len(v),
    "\nfaces\n",
    "nlen=",
    len(n),
    "\n nv = ",
    nv,
    "\n nf = ",
    nf,
)


print("sum(nv)=", sum(nv))
print("sum(nf)=", sum(nf))

v = split_by_count(v, nv)
f = split_by_count(n, nf)

for i, (x, y) in enumerate(zip(v, f)):
    # if len(x) == 0 or len(y) == 0:
    #     continue
    # print(i, x, y)
    mesh = trimesh.Trimesh(x, y)
    mesh.export(str(i) + ".obj")
