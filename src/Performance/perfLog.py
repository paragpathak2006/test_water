from locale import format_string
import time


class Variant:

    def BASELINE(s : str):
        return "Baseline " + s
    def KDTREE(s : str):
        return "KDtree " + s
    def HASH_INTERSECTION(s : str):
        return "Hash " + s


class Algo:

    CONVEX_HULL_DIFFERENCE = "1️⃣. CHD"

    def MESH_INTERSECTION_DIFFERENCE(i):
        return f"2️⃣. Mesh (∩,Δ) : {i}"

    def SPLIT(i):
        return f"3️⃣. Split : {i}"

    PROXIMITY_CONSTRUCT = "    Proximity Build"
    TREE_CONSTRUCT = "    KDTree Build"
    HASH_CONSTRUCT = "    Hash Build"


class PerfLog:
    _events = {}
    _start = time.perf_counter()

    @staticmethod
    def start(name: str):
        PerfLog._events[name] = time.perf_counter()

    @staticmethod
    def line(i):
        PerfLog._events[f"-----------------------{i}"] = "-------------------"

    @staticmethod
    def log(name: str, func: callable, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        PerfLog._events[name] = time.perf_counter() - start_time
        return result

    @staticmethod
    def stop(name: str):
        PerfLog._events[name] = time.perf_counter() - PerfLog._events[name]

    @staticmethod
    def report():
        print(" Event Times ")
        # Print header
        row_format = "{:<35} | {:<30} "
        print(row_format.format("Method Name ", "Time (ms)"))
        print("-" * 60) # Separator
        for name, times in PerfLog._events.items():
            if isinstance(times, list):
                total_time = sum(times)
                avg_time = total_time / len(times)
                print(row_format.format(f" 📍 {name:20} ",f" Δt = ⏰ {times} , avg = {avg_time * 1e3:8.4f}ms (over {len(times)} runs)"))
            else:
                if isinstance(name, str) and name.startswith("-----------------------"):
                    print("-" * 60) # Separator
                else:
                    print(row_format.format(f" 📍 {name:20} ",f" Δt = ⏰ {times * 1e3:8.4f}ms"))
