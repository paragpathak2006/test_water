import os
from pathlib import Path
import numpy as np
import unittest

import trimesh

from src.Fluid_region_extraction_algo.baseline.test import (
    test_convexhull_difference_algo as baseline_algo_test,
)
from src.Fluid_region_extraction_algo.Variant.kdtree.test import (
    test_convexhull_difference_algo as kdtree_algo_test,
)
from src.Fluid_region_extraction_algo.Variant.hashing.test import (
    test_convexhull_difference_algo as hash_algo_test,
)

from src.Performance.perfLog import PerfLog, TargetAlgo

from tests.io_path import OUT_DIR as benchmark_OUT_DIR

from src.Fluid_region_extraction_algo.baseline.io_path import (
    OUT_DIR as baseline_OUT_DIR,
)
from src.Fluid_region_extraction_algo.Variant.kdtree.io_path import (
    OUT_DIR as kdtree_OUT_DIR,
)
from src.Fluid_region_extraction_algo.Variant.hashing.io_path import (
    OUT_DIR as hash_OUT_DIR,
)


class Run_Unit_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        print("\nSetting up fluid volume extraction algorithm test...\n")

        cls.times = ["0.1", "0.1"]
        cls.maxTimeAllowed = 1  # time limit of 1 seconds

        cls.benchmark_files_list()
        cls.pre_cleanup_output_dir()

        print("─────୨ৎ────୨ৎ────୨ৎ────୨ৎ────\n\n")

    @classmethod
    def benchmark_files_list(cls):
        cls.files = [p.name for p in Path(benchmark_OUT_DIR).iterdir() if p.is_file()]
        print("Files to be tested : ", cls.files)

    @classmethod
    def pre_cleanup_output_dir(cls):
        print("\nPre-cleaning up the output directory...\n")
        for file in cls.files:
            if file.startswith("0."):
                continue

            baseline_file = baseline_OUT_DIR / file
            if os.path.exists(baseline_file):
                os.remove(baseline_file)

            hash_file = hash_OUT_DIR / file
            if os.path.exists(hash_file):
                os.remove(hash_file)

            kdtree_file = kdtree_OUT_DIR / file
            if os.path.exists(kdtree_file):
                os.remove(kdtree_file)

        print("Pre-cleanup done.\n\n")

    def test_C1_correctness_baseline(self):
        print("\n\n C1️⃣ testing baseline convex hull difference algorithm...")

        if baseline_algo_test() is None:
            self.fail(
                "❌ Baseline convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, baseline_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_P1_performance_baseline(self):
        print(
            "\n\n P1️⃣  testing performance of baseline convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[TargetAlgo.BASELINE.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[TargetAlgo.BASELINE.MESH_INTERSECTION_DIFFERENCE(0)]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_C2_correctness_kdtree(self):
        print("\n\n C2️⃣   Testing kdtree convex hull difference algorithm...")

        if kdtree_algo_test() is None:
            self.fail(
                "❌ KDtree convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, kdtree_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_P2_performance_kdtree(self):
        print(
            "\n\n P2️⃣   testing performance of kdtree convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[TargetAlgo.KDTREE.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[TargetAlgo.KDTREE.MESH_INTERSECTION_DIFFERENCE(0)]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_C3_correctness_hash_intersection(self):
        print("\n\n C3️⃣  Testing hash intersection algorithm...")

        if hash_algo_test() is None:
            self.fail("❌ Hash intersection algorithm failed. Aborting test.")

        self.files_compare(benchmark_OUT_DIR, hash_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_P3_performance_hash_intersection(self):
        print("\n\n  P3️⃣   testing performance of hash intersection algorithm...\n")

        total_time = (
            PerfLog._events[TargetAlgo.HASH_INTERSECTION.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[
                TargetAlgo.HASH_INTERSECTION.MESH_INTERSECTION_DIFFERENCE(0)
            ]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    # Final report after all tests are done
    def test_report_all(self):
        print(
            "\n 4️⃣ All tests completed... \n 📝 ✅✅ Final performance report ✅✅\n"
        )
        PerfLog.report()

    # Helper function to compare files in two directories
    def files_compare(self, DIR1, DIR2):

        files = [p.name for p in Path(DIR1).iterdir() if p.is_file()]

        for file in files:
            print("📁 Comparing file : ", file)

            baseline_mesh = trimesh.load(DIR1 / file)
            benchmark_mesh = trimesh.load(DIR2 / file)

            self.assertTrue(
                np.array_equal(baseline_mesh.faces, benchmark_mesh.faces),
                f"❌ Face arrays are not equal for file {file}",
            )
            self.assertTrue(
                np.allclose(baseline_mesh.vertices, benchmark_mesh.vertices),
                f"❌ Vertex arrays are not close for file {file}",
            )


if __name__ == "__main__":
    unittest.main()
