import argparse

from convert import __convert, __d50, __d65, COLOR_SPACES


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", default=1)
    args = parser.parse_args()
    def color2str(color, color_space, pts=args.precision):
        return color_space.upper() + '(' + ", ".join(
            [f"{_:.{0 if color_space == 'rgb' else pts}f}" for _ in color]
        ) + ')'

    rgb_color = [200, 100, 20]
    print(color2str(rgb_color, "rgb"))
    
    for whitepoint, series in [(__d50, "D50"), (__d65, "D65")]:
        print(f"\nwhitepoint = [{', '.join(str(_) for _ in whitepoint)}] ({series})")
        for color_space in COLOR_SPACES[1:]:
            col = __convert(rgb_color, init="rgb", dest=color_space, max_XYZ=whitepoint)
            rgb = __convert(col, init=color_space, dest="rgb", max_XYZ=whitepoint)
            err = (sum((o - c)**2 for o, c in zip(rgb_color, rgb)))**0.5
            print("  - " + color2str(col, color_space))
            if (err > 1e-5):
                print(f"'{color_space}' to 'rgb' conversion failed:")
                print(f"  err = {err}")
                print(f"  {color2str(rgb, 'rgb')}")