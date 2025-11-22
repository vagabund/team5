import sys
from pathlib import Path


def get_variants_path():
    filename = "variants.txt"
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.argv[0]).resolve()
        app_bundle = exe_path.parents[2] if exe_path.name != filename else exe_path.parent
        app_folder = app_bundle.parent
        external = app_folder / filename
        if external.exists():
            return external
        else:
            return None
    else:
       script_dir = Path(__file__).resolve().parent
       return script_dir / filename

def get_output_path():
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.argv[0]).resolve()
        app_bundle = exe_path.parents[2]
        app_folder = app_bundle.parent
        return app_folder
    else:
        return Path(__file__).resolve().parent

variants_path = get_variants_path()
output_path = get_output_path()

def load_played_vars():
    with variants_path.open("r", encoding="utf-8") as f:
        line = f.read().strip()
    line = line.strip("()")
    numbers = line.split("-")
    return tuple(int(n) for n in numbers)

PLAYED_VARS = load_played_vars()