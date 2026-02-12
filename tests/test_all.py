import os
from pathlib import Path
from time import time
import numpy as np
import unittest

import trimesh
from src.KDtree_convexhull_difference_algo.test_kdtree_algo import test_kdtree_convexhull_difference
from src.Baseline_convexhull_difference_algo.test_baseline_algo import test_baseline_convexhull_difference
from src.Performance.perfLog import PerfLog

from io_path import OUT_DIR as benchmark_OUT_DIR
from src.Baseline_convexhull_difference_algo.io_path import OUT_DIR as baseline_OUT_DIR
from src.KDtree_convexhull_difference_algo.io_path import OUT_DIR as kdtree_OUT_DIR


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

            kdtree_file = kdtree_OUT_DIR / file
            if os.path.exists(kdtree_file):
                os.remove(kdtree_file)

        print("Pre-cleanup done.\n\n")

    def test_baseline_convexhull_difference(self):
        print("\n\n 1️⃣ testing baseline convex hull difference algorithm...")
        
        fluid_volumes_walls_inlets_outlets = test_baseline_convexhull_difference()

        files = [p.name for p in Path(benchmark_OUT_DIR).iterdir() if p.is_file()]

        for file in files:
            print("Comparing file : ", file)

            baseline_mesh = trimesh.load(baseline_OUT_DIR / file)
            benchmark_mesh = trimesh.load(benchmark_OUT_DIR / file)

            self.assertTrue(np.array_equal(baseline_mesh.faces, benchmark_mesh.faces))
            self.assertTrue(np.allclose(baseline_mesh.vertices, benchmark_mesh.vertices))

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_performance_baseline_convex_hull_algo(self):
        print("\n\n 2️⃣  testing performance of baseline convex hull difference algorithm...\n")
        PerfLog.report()
        
        total_time = PerfLog._events["Baseline Convex hull difference"] + PerfLog._events["Baseline mesh faces (∩,Δ) - vol#0"]


        self.assertLessEqual(total_time, self.maxTimeAllowed, 
                             f"❌ Performance test failed: Time taken {total_time*1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed*1e3:.0f}ms")        

        print(f"\n✅ Performance test passed: Total time taken: {total_time*1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed*1e3:.0f}ms\n")
        
        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_kdtree_convexhull_difference(self):
        print("\n\n  3️⃣  Testing kdtree convex hull difference algorithm...")
        
        fluid_volumes_walls_inlets_outlets = test_kdtree_convexhull_difference()

        files = [p.name for p in Path(benchmark_OUT_DIR).iterdir() if p.is_file()]

        for file in files:
            print("Comparing file : ", file)

            baseline_mesh = trimesh.load(baseline_OUT_DIR / file)
            benchmark_mesh = trimesh.load(benchmark_OUT_DIR / file)

            self.assertTrue(np.array_equal(baseline_mesh.faces, benchmark_mesh.faces))
            self.assertTrue(np.allclose(baseline_mesh.vertices, benchmark_mesh.vertices))

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_performance_kdtree_convex_hull_algo(self):
        print("\n\n  4️⃣  testing performance of kdtree convex hull difference algorithm...\n")
        PerfLog.report()
        
        total_time = PerfLog._events["KDtree Convex hull difference"] + PerfLog._events["KDtree mesh faces (∩,Δ) - vol#0"]

        self.assertLessEqual(total_time, self.maxTimeAllowed, 
                             f"❌ Performance test failed: Time taken {total_time*1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed*1e3:.0f}ms")        

        print(f"\n✅ Performance test passed: Total time taken: {total_time*1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed*1e3:.0f}ms\n")
        
        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")


if __name__ == "__main__":
    unittest.main()
