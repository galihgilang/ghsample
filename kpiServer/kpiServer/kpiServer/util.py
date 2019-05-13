import sys

def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)