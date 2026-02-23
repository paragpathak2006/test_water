import functools
import json


class Logger:
    root = {}
    stack = [root]

    @staticmethod
    def enter(name):
        node = {}
        Logger.stack[-1].setdefault(name, []).append(node)
        Logger.stack.append(node)

    @staticmethod
    def exit():
        if len(Logger.stack) > 1:
            Logger.stack.pop()

    @staticmethod
    def log(key, value):
        Logger.stack[-1][key] = value

    @staticmethod
    def log_val(value):
        key = " logs"
        if Logger.stack[-1].get(key) is None:
            Logger.stack[-1][key] = [value]

        Logger.stack[-1][key].append(value)

    @staticmethod
    def to_dict():
        return Logger.root

    @staticmethod
    def to_json():
        with open("logs.json", "w") as f:
            json.dump(Logger.root, f, indent=2)


def log_tree(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        Logger.enter(func.__name__)
        Logger.log("input", str(args) + str(kwargs))
        result = func(*args, **kwargs)
        Logger.log("output", str(result))
        Logger.exit()
        return result

    return wrapper
