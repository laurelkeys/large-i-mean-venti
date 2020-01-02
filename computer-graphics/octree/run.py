import os
import argparse
from time import time
from subprocess import run

EXEC_NAME = "octree"

def build_cmd(args):
    cmd = ["g++", "main.cc", "-o", EXEC_NAME]
    if args.debug:
        cmd.append("-g")
    if args.warnings:
        cmd.append("-Wall")
    if args.max_speed:
        cmd.append("-O2")
        if args.min_size:
            print("\nWarning: -O is ignored if -O2 is used as well\n")
    elif args.min_size:
        cmd.append("-O")
    return cmd

def main():
    args, unknown_args = get_parser().parse_known_args()
    start_time = time()

    if not args.clean:
        run(build_cmd(args) + unknown_args) # build
        run([f"./{EXEC_NAME}"]) # run
    else:
        try:
            os.remove(f"{EXEC_NAME}.exe") # clean
        except OSError:
            pass

    print(f"Δt = {(time() - start_time):.2f}s")


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Remove .exe instead of building and running")
    parser.add_argument("--debug", "-g", action="store_true", help="Use -g on g++ call")
    parser.add_argument("--warnings", "-Wall", action="store_true", help="Use -Wall on g++ call")
    parser.add_argument("--min_size", "-O", action="store_true", help="Use -O on g++ call (minimize size)")
    parser.add_argument("--max_speed", "-O2", action="store_true", help="Use -O2 on g++ call (maximize speed)")
    return parser

if __name__ == "__main__":
    main()