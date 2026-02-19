import numpy as np
import trimesh
import os
from pathlib import Path


# Helper function to get list of files in a directory
def get_files_list(DIR):
    print(f"\nGetting list of files in directory : {DIR}")
    files = [p.name for p in Path(DIR).iterdir() if p.is_file()]

    print("files found : ")
    for i, file in enumerate(files):
        print(f"📁 {i}: {file}")

    return files


# Helper function to compare files in two directories
def files_compare(tester, DIR1, DIR2):

    files = get_files_list(DIR1)

    for file in files:
        print("📁 Comparing file : ", file)

        mesh1 = trimesh.load(DIR1 / file)
        mesh2 = trimesh.load(DIR2 / file)

        tester.assertTrue(
            np.array_equal(mesh1.faces, mesh2.faces),
            f"❌ Face arrays are not equal for file {file}",
        )
        tester.assertTrue(
            np.allclose(mesh1.vertices, mesh2.vertices),
            f"❌ Vertex arrays are not close for file {file}",
        )


# Helper function to pre-cleanup output directories before running tests to avoid confusion with old files from previous runs
def pre_cleanup_outputs(DIRs):
    for DIR in DIRs:
        pre_cleanup_output(DIR)


def pre_cleanup_output(DIR):
    print(f"\n Pre-cleaning up output directory : {DIR} ...\n")
    files = get_files_list(DIR)
    for name in files:
        if name.startswith("0."):
            continue

        file = DIR / name
        if os.path.exists(file):
            print(f"🧹 Removing file 📂 {name} 🗑️")
            os.remove(file)
