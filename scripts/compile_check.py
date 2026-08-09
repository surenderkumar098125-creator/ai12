import compileall
import sys

if __name__ == '__main__':
    ok = compileall.compile_dir('.', force=True)
    if not ok:
        sys.exit(1)
