from trimesh import Trimesh

# The volume of the mesh using the trimesh volume property.
def baseline_volume_calculate(mesh : Trimesh):
    return mesh.volume