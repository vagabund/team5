def load_played_vars(path="variants.txt"):
    with open(path, "r", encoding="utf-8") as f:
        line = f.read().strip()
    line = line.strip("()")
    numbers = line.split("-")
    return tuple(int(n) for n in numbers)

PLAYED_VARS = load_played_vars()