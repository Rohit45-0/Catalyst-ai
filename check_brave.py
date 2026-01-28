import sys
try:
    import brave
    with open("brave_check.txt", "w") as f:
        f.write("INSTALLED")
except ImportError:
    with open("brave_check.txt", "w") as f:
        f.write("MISSING")
