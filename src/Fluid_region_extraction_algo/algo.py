from trimesh import Trimesh
from src.Performance.perfLog import PerfLog
from src.Geometry.Processing.pre import preprocess
from src.Geometry.Processing.post import postprocess
from src.Geometry.Processing.export import export_fluid_volumes_and_boundaries_all

from src.Fluid_region_extraction_algo.selector import (
    convexhull_difference_selector,
    mesh_intersection_difference_selector,
    proximity_selector,
    split_selector,
    tree_or_table_selector,
)


class Fluid_region_extraction_algo:

    @classmethod
    def fluid_extraction_algo(cls, solid: Trimesh, variant):

        if preprocess(solid) is None:
            return None

        fluids = convexhull_difference_selector(variant, solid)
        if fluids is None:
            print(cls.convex_hull_difference_failed_msg)
            return None

        print("\n✅ Number of fluid volumes : ", len(fluids))

        # compute proximity query for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
        prox_solid = proximity_selector(variant, solid)
        tree_or_table = tree_or_table_selector(variant, solid)

        for i, fluid in enumerate(fluids):
            print("\nExtracting fluid walls and inlet-outlet boundaries...")
            print("\nProcessing fluid volume#", i, " ...")
            print("\nVolume = ", fluid.volume)
            print("surface area = ", fluid.area)

            # extract fluid wall and inlet-outlet boundaries using intersection-difference method
            wall, IOs_combined = mesh_intersection_difference_selector(
                variant, i, fluid, solid, prox_solid, tree_or_table
            )

            IOs = split_selector(variant, i, IOs_combined)
            print(cls.number_of_fluid_volumes_msg(i, IOs))

            if len(IOs) >= 2:
                # Validation check for output fluid volume mesh
                if postprocess(fluid) is None:
                    return None

                print(cls.fluid_volume_path_validation_success_msg)
                # capturing the list of inlet-outlet boundary meshes
                cls.add_to_collection(fluid, wall, IOs_combined, IOs)

        PerfLog.line()

        if len(cls.embedded_volumes) == 0:
            print(cls.no_embedded_fluid_volume_msg)
            return None

        export_fluid_volumes_and_boundaries_all(cls, variant)
        return cls.embedded_volumes, cls.fluid_walls, cls.fluid_inlets_outlets_all

    @classmethod
    def add_to_collection(cls, fluid, wall, IOs_combined, IOs):
        # capturing the fluid volume mesh that form a valid path with atleast 2 open boundaries (i.e. inlet and outlet)
        cls.embedded_volumes.append(fluid)
        cls.fluid_walls.append(wall)  # capturing the fluid wall mesh
        cls.fluid_inlets_outlets_all_combined.append(IOs_combined)
        cls.fluid_inlets_outlets_all.append(IOs)
        # capturing the list of inlet-outlet boundary meshes

    @classmethod
    def number_of_fluid_volumes_msg(cls, i, ios):
        return (
            f"For volume#{i} : Number of fluid inlet and outlet boundaries : {len(ios)}"
        )

    convex_hull_difference_failed_msg = "❌ Convex hull difference algorithm failed or Solid is already convex.No fluid volumes extracted."
    fluid_volume_path_validation_success_msg = "\n✅ Multiple fluid inlets-outlets detected. Fluid volume represents a valid embedded path."
    no_embedded_fluid_volume_msg = "\n❌ No valid embedded fluid volumes with atleast 2 open boundaries (i.e. inlet and outlet) detected.❌"

    # result list to store combined inlet-outlet boundary meshes for each fluid volume
    embedded_volumes = []
    fluid_walls = []  # result list to store fluid wall meshes
    fluid_inlets_outlets_all_combined = []
    fluid_inlets_outlets_all = []

    @classmethod
    def cleanup(cls):
        cls.embedded_volumes = []
        cls.fluid_walls = []  # result list to store fluid wall meshes
        cls.fluid_inlets_outlets_all_combined = []
        cls.fluid_inlets_outlets_all = []
