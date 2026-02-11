from trimesh import Trimesh

def baseline_heal(mesh : Trimesh):
    mesh.process(validate=True)
    mesh.remove_unreferenced_vertices()
    mesh.fill_holes()

    if mesh.volume > 0 : 
        mesh.fix_normals()


    print("Is mesh watertight:", mesh.is_watertight)
    print("Volume of mesh:", mesh.volume)

