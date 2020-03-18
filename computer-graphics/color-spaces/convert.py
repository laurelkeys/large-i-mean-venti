import os
import argparse

# CIE Standard Illuminant D50:
__d50 = [0.9642, 1.0000, 0.8251] # CCT of 5003 K (also known as horizon light)

# sRGB to XYZ matrix [M], with D50 as the reference white:
__sRGB_to_XYZ = [
    [0.4360747, 0.3850649, 0.1430804],
    [0.2225045, 0.7168786, 0.0606169],
    [0.0139322, 0.0971045, 0.7141733],
]

# XYZ to sRGB matrix [M]^-1, with D50 as the reference white:
__XYZ_to_sRGB = [
    [ 3.1338561, -1.6168667, -0.4906146],
    [-0.9787684,  1.9161415,  0.0334540],
    [ 0.0719453, -0.2289914,  1.4052427],
]

def __mat_mul(m3, v3):
    return [
        m3[0][0] * v3[0] + m3[0][1] * v3[1] + m3[0][2] * v3[2],
        m3[1][0] * v3[0] + m3[1][1] * v3[1] + m3[1][2] * v3[2],
        m3[2][0] * v3[0] + m3[2][1] * v3[1] + m3[2][2] * v3[2],
    ]

def __linear_RGB_to_sRGB(linear_RGB):
    return [12.92 * v if v <= 0.0031308
            else 1.055 * (v ** (1 / 2.4)) - 0.055
            for v in linear_RGB]

def __sRGB_to_linear_RGB(sRGB):
    return [(1 / 12.92) * V if V <= 0.04045
            else ((V + 0.055) * (1 / 1.055)) ** 2.4
            for V in sRGB]

def __luminance(linear_RGB):
    r, g, b = linear_RGB
    return [0.212671 * r, 0.715160 * g, 0.072169 * b]

# References:
#   http://paulbourke.net/miscellaneous/colourspace/
#   https://www.mathworks.com/help/images/ref/whitepoint.html
#   http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
#   http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

COLOR_SPACES = [
    # sRGB
    "rgb",    # r,g,b ∈ [0, 255]

    # HSV
    "hsv",    # h     ∈ [0.0, 360.0)
              # s,v   ∈ [0.0, 1.0]

    # CMYK
    "cmy",    # c,m,y ∈ [0.0, 100.0]

    # CIEXYZ
    "xyz",    # x,y,z ∈ [0.0, 1.0]

    # CIELAB
    "cielab"  # L*,a*,b*
]

##
## sRGB
##

""" sRGB → HSV """
def convert_from_rgb_to_hsv(color):
    r, g, b = color

    theta_min = min(r, g, b)
    theta_max = max(r, g, b)
    delta = theta_max - theta_min
    h = 0
    v = theta_max
    s = delta / theta_max if theta_max > 0 else 0
    if delta > 0:
        if theta_max == r and theta_max != g:
            h += (g - b) / delta
        if theta_max == g and theta_max != b:
            h += (2 + (b - r) / delta)
        if theta_max == b and theta_max != r:
            h += (4 + (r - g) / delta)
        h *= 60

    return [h, s, v]

""" sRGB → CMYK """
def convert_from_rgb_to_cmy(color):
    return [100 * (255 - component) / 255 for component in color]

""" sRGB → CIEXYZ """
def convert_from_rgb_to_xyz(color):
    r, g, b = [
        V / 12.92 if V <= 0.04045
        else ((V + 0.055) / 1.055) ** 2.4
        for V in [(component / 255) for component in color]
    ]
    return __mat_mul(__sRGB_to_XYZ, [r, g, b])

""" sRGB → CIELAB """
def convert_from_rgb_to_cielab(color):
    return convert_from_xyz_to_cielab(convert_from_rgb_to_xyz(color))

##
## HSV
##

""" HSV → sRGB """
def convert_from_hsv_to_rgb(color):
    h, s, v = color

    if h < 120:
        r = (120 - h) / 60
        g = h / 60
        b = 0
    elif h < 240:
        r = 0
        g = (240 - h) / 60
        b = (h - 120) / 60
    else:
        r = (h - 240) / 60
        g = 0
        b = (360 - h) / 60

    r = (1 - s + s * min(r, 1)) * v
    g = (1 - s + s * min(g, 1)) * v
    b = (1 - s + s * min(b, 1)) * v

""" HSV → CMYK """
def convert_from_hsv_to_cmy(color):
    pass

""" HSV → CIEXYZ """
def convert_from_hsv_to_xyz(color):
    pass

""" HSV → CIELAB """
def convert_from_hsv_to_cielab(color):
    pass

##
## CMYK
##

""" CMYK → sRGB """
def convert_from_cmy_to_rgb(color):
    pass

""" CMYK → HSV """
def convert_from_cmy_to_hsv(color):
    pass

""" CMYK → CIEXYZ """
def convert_from_cmy_to_xyz(color):
    pass

""" CMYK → CIELAB """
def convert_from_cmy_to_cielab(color):
    pass

##
## CIEXYZ
##

""" CIEXYZ → sRGB """
def convert_from_xyz_to_rgb(color):
    pass

""" CIEXYZ → HSV """
def convert_from_xyz_to_hsv(color):
    pass

""" CIEXYZ → CMYK """
def convert_from_xyz_to_cmy(color):
    pass

""" CIEXYZ → CIELAB """
def convert_from_xyz_to_cielab(color):
    pass

##
## CIELAB
##

""" CIELAB → sRGB """
def convert_from_cielab_to_rgb(color):
    pass

""" CIELAB → HSV """
def convert_from_cielab_to_hsv(color):
    pass

""" CIELAB → CMYK """
def convert_from_cielab_to_cmy(color):
    pass

""" CIELAB → CIEXYZ """
def convert_from_cielab_to_xyz(color):
    pass


###############################################################################

def validate(color, from_space):
    # ref.: https://stackoverflow.com/questions/8107713/using-argparse-argumenterror-in-python
    if from_space == "rgb":
        try:
            color = map(int, color)
        except:
            raise argparse.ArgumentTypeError("rgb color components must be integers")
        assert all(0 <= component <= 255 for component in color), (
            "sRGB color components (r, g, b) must be in the range [0, 255]"
        )
    elif from_space == "hsv":
        h, s, v = color
        assert 0.0 <= h < 360.0, (
            "HSV color component h must be in the range [0.0, 360.0)"
        )
        assert 0.0 <= s <= 1.0, (
            "HSV color component s must be in the range [0.0, 1.0]"
        )
        assert 0.0 <= v <= 1.0, (
            "HSV color component v must be in the range [0.0, 1.0]"
        )
    elif from_space == "cmy":
        assert all(0.0 <= component <= 100.0 for component in color), (
            "CMYK color components (c, m, y) must be in the range [0.0, 100.0]"
        )
    elif from_space == "xyz":
        # CIEXYZ color components (x, y, z)
        pass
    else: # cielab
        # CIELAB color components (L*, a*, b*)
        pass
    return color

def convert(color, from_space, to_space):
    if from_space == to_space:
        return color

    # if from_space == "rgb":
    #     return convert_from_rgb(to_space, color)
    # elif from_space == "hsv":
    #     return convert_from_hsv(to_space, color)
    # elif from_space == "cmy":
    #     return convert_from_cmy(to_space, color)
    # elif from_space == "xyz":
    #     return convert_from_xyz(to_space, color)
    # else: # cielab
    #     return convert_from_cielab(to_space, color)

def main(args):
    from_color = validate(args.color, args.from_space)
    to_color = convert(from_color, args.from_space, args.to_space)
    print(
        f"{args.from_space.upper()}(" + ", ".join(map(str, from_color)) + ")",
        "to",
        f"{args.to_space.upper()}(" + ", ".join(map(str, to_color)) + ")"
    )

###############################################################################

def get_parser():
    parser = argparse.ArgumentParser(description="Color space converter.")
    parser.add_argument("from_space",
                        type=str,
                        metavar="from",
                        choices=COLOR_SPACES)
    parser.add_argument("to_space",
                        type=str,
                        metavar="to",
                        choices=COLOR_SPACES)
    parser.add_argument("color",
                        nargs=3,
                        type=float,
                        action="store")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Increase verbosity")
    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = get_parser().parse_args()

    main(args)