import trimesh
from Convexhull_operations.self_difference import convex_hull_difference
from Mesh_operations.intersection import mesh_faces_intersection
from Mesh_operations.difference import mesh_faces_difference
from io_path import OUT_DIR
from trimesh import Trimesh

def baseline_convexhull_difference(solid_volume : Trimesh):

    fluid_volumes =  convex_hull_difference(solid_volume)

    print("\nNumber of fluid volumes : ", len(fluid_volumes))
    for i, fluid_volume in enumerate(fluid_volumes):
        fluid_volume.export(OUT_DIR / f"1. fluid-volume-{i}.stl")

    fluid_walls = []
    all_fluid_inlets_outlets = []

    print("\nExtracting fluid walls and inlet-outlet boundaries...")
    for i, fluid_volume in enumerate(fluid_volumes):

        print("\nProcessing fluid volume#", i," ...")
        print("\nExtracting fluid wall...\n")
        fluid_wall = mesh_faces_intersection( solid_volume, fluid_volume)
        fluid_wall.export(OUT_DIR / f"2. fluid_wall-{i}.stl")
        fluid_walls.append(fluid_wall)

        print("\nExtracting fluid inlet and outlet boundaries...\n")
        diff = mesh_faces_difference(fluid_volume, fluid_wall)
        diff.export(OUT_DIR / f"3. fluid_wall_difference-{i}.stl")

        print("\nSplitting fluid inlet and outlet boundaries...")
        fluid_inlets_outlets = diff.split(only_watertight=False)
        all_fluid_inlets_outlets.append(fluid_inlets_outlets)

        print("For volume#", i, " : Number of fluid inlet and outlet boundaries : ", len(fluid_inlets_outlets))
        for ii, fluid_inlet_outlet in enumerate(fluid_inlets_outlets):
            fluid_inlet_outlet.export(OUT_DIR / f"4. fluid-inlet-outlet-{i}-{ii}.stl")

    return {"fluid_volumes": fluid_volumes, "fluid_walls": fluid_walls, "all_fluid_inlets_outlets": all_fluid_inlets_outlets}
    
# # Load the original mesh
# solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")
# baseline_convexhull_difference_method(solid_volume)

