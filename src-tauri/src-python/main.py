
import sys

_tauri_plugin_functions = ["greet_python"]

def greet_python(name):
    return f"Hello {name} from Python! (Version: {sys.version})"
