import time


class Variant:

    def BASELINE(s: str):
        return "Baseline " + s

    def KDTREE(s: str):
        return "KDtree " + s

    def HASH_INTERSECTION(s: str):
        return "Hash " + s


class Algo:

    CONVEX_HULL_DIFFERENCE = "⬜ CHD"

    def MESH_INTERSECTION_DIFFERENCE(i):
        return f"⬜ Mesh (∩,Δ) : {i}"

    def SPLIT(i):
        return f"⬜ Split : {i}"

    PROXIMITY_CONSTRUCT = "🔨 Proximity Build"
    TREE_CONSTRUCT = "🔨 KDTree Build"
    HASH_CONSTRUCT = "🔨 Hash Build"


class PerfLog:
    _events = {}
    _start = time.perf_counter()
    _line_count = 0

    @staticmethod
    def start(name: str):
        PerfLog._events[name] = time.perf_counter()

    @staticmethod
    def line():
        PerfLog._events[f"-----------------------{PerfLog._line_count}"] = (
            "-------------------"
        )
        PerfLog._line_count += 1

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
        row_format = "{:<30} | {:<30} "
        print(row_format.format("⬜ Method Name ", "ΔT"))
        print("-" * 60)  # Separator
        for name, times in PerfLog._events.items():
            if isinstance(times, list):
                total_time = sum(times)
                avg_time = total_time / len(times)
                print(
                    row_format.format(
                        f" 📍 {name:20} ",
                        f" Δt = ⏰ {times} , avg = {avg_time * 1e3:8.4f}ms (over {len(times)} runs)",
                    )
                )
            else:
                if isinstance(name, str) and name.startswith("-----------------------"):
                    print("-" * 60)  # Separator
                else:
                    print(row_format.format(f" 📍 {name} ", f"⏰ {times_msg(times)}"))


def times_msg(times):
    if times > 1e-3:
        return f"{times * 1e3:8.0f} ms"
    elif times > 1e-4:
        return f"{times * 1e3:8.1f} ms"
    else:
        return f"{times * 1e6:8.1f} μs"
