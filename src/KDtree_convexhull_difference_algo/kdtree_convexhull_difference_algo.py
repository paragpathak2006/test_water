from trimesh import Trimesh
from .Convexhull_operations.self_difference import convex_hull_difference
from .Mesh_operations.intersection_difference import mesh_faces_intersection_difference
from .io_path import OUT_DIR
from ..Performance.perfLog import PerfLog
from ..Geometry.validation.baseline_validation import baseline_validation_check
from ..Geometry.healing.baseline_healing import baseline_heal


def kdtree_convexhull_difference(solid_volume: Trimesh):

    if not baseline_validation_check(solid_volume):
        print("❌Input solid volume mesh is not valid. Attempting to heal geometry.❌")
        baseline_heal(solid_volume)
        if not baseline_validation_check(solid_volume):
            print(
                "❌Input solid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm.❌"
            )
            return None
        else:
            print(
                "✅Input solid volume mesh has been successfully healed to a valid mesh. Proceeding with convex hull difference algorithm.✅"
            )

    print("\nRunning kdtree convex hull difference algorithm...\n")
    PerfLog.start("KDtree Convex hull difference")
    fluid_volumes = convex_hull_difference(solid_volume)
    PerfLog.stop("KDtree Convex hull difference")

    print("\nNumber of fluid volumes : ", len(fluid_volumes))
    for i, fluid_volume in enumerate(fluid_volumes):
        fluid_volume.export(OUT_DIR / f"1. fluid-volume-{i}.stl")

    fluid_walls = []
    all_fluid_inlets_outlets = []
    max_volume_index = max(
        range(len(fluid_volumes)), key=lambda i: fluid_volumes[i].volume
    )
    i = max_volume_index

    print(
        "\nLargest fluid volume is volume#",
        max_volume_index,
        " with volume = ",
        fluid_volumes[max_volume_index].volume,
    )
    print("\nExtracting fluid walls and inlet-outlet boundaries...")

    print("\nProcessing fluid volume#", i, " ...")
    print("\nvolume = ", fluid_volumes[i].volume)
    print("surface area = ", fluid_volumes[i].area)

    print("\nExtracting fluid wall and inlet-outlet boundaries...\n")

    # extract fluid wall and inlet-outlet boundaries using intersection-difference method
    PerfLog.start("KDtree mesh faces (∩,Δ) - vol#" + str(i))
    fluid_boundary = mesh_faces_intersection_difference(fluid_volumes[i], solid_volume)
    PerfLog.stop("KDtree mesh faces (∩,Δ) - vol#" + str(i))

    fluid_wall = fluid_boundary["intersection"]
    fluid_inlets_outlets = fluid_boundary["difference"].split(only_watertight=False)

    fluid_walls.append(fluid_wall)
    all_fluid_inlets_outlets.append(fluid_inlets_outlets)

    # export each inlet-outlet boundary separately
    fluid_boundary["difference"].export(
        OUT_DIR / f"3. fluid_inlets-outlets-combined-{i}.stl"
    )
    fluid_wall.export(OUT_DIR / f"2. fluid_wall-{i}.stl")
    print(
        "For volume#",
        i,
        " : Number of fluid inlet and outlet boundaries : ",
        len(fluid_inlets_outlets),
    )
    for ii, fluid_inlet_outlet in enumerate(fluid_inlets_outlets):
        fluid_inlet_outlet.export(OUT_DIR / f"4. fluid-inlet-outlet-{i}-{ii}.stl")

    # Validation check for output fluid volume mesh
    if not baseline_validation_check(fluid_volumes[i]):
        print(
            "❌ Output fluid volume mesh is not valid. Attempting to heal geometry.❌"
        )
        baseline_heal(fluid_volumes[i])
        if not baseline_validation_check(fluid_volumes[i]):
            print(
                "❌ Output fluid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm.❌"
            )
            return None
        else:
            print(
                "✅ Output fluid volume mesh has been successfully healed to a valid mesh. Proceeding with convex hull difference algorithm.✅"
            )
    else:
        print(
            "✅ Output fluid volume mesh is valid and represents a fluid volume. No healing needed."
        )

    return {
        "fluid_volumes": fluid_volumes,
        "fluid_walls": fluid_walls,
        "all_fluid_inlets_outlets": all_fluid_inlets_outlets,
    }

    # # Load the original mesh
    # solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")
    # baseline_convexhull_difference_method(solid_volume)

    # fluid_wall = mesh_faces_intersection( solid_volume, fluid_volume)
    # fluid_wall.export(OUT_DIR / f"2. fluid_wall-{i}.stl")
    # fluid_walls.append(fluid_wall)

    # print("\nExtracting fluid inlet and outlet boundaries...\n")
    # diff = mesh_faces_difference(fluid_volume, fluid_wall)
    # diff.export(OUT_DIR / f"3. fluid_wall_difference-{i}.stl")
