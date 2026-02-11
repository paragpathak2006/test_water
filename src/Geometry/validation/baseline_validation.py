from trimesh import Trimesh

def baseline_validation_check(mesh : Trimesh):

    print("Is mesh watertight:", mesh.is_watertight)
    print("Volume of mesh:", mesh.volume)

    return mesh.is_watertight and mesh.volume > 0