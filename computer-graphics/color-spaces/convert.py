import os
import argparse


###############################################################################
###############################################################################

# CIE Standard Illuminants' XYZ coordinates (normalized to Y = 100):
__d50 = [96.42, 100.00,  82.51] # D50, CCT of 5003 K (horizon light)
__d65 = [95.04, 100.00, 108.88] # D65, CCT of 6504 K (noon daylight)

# NOTE the following matrices assume:
#  - XYZ values in the range [0, 100]
#  - sRGB1 values in the range [0, 1]

# sRGB1 to XYZ matrix [M], with CIE 1931 2° whitepoint reference values:
__sRGB1_to_XYZ_under_D50 = [
    [0.4360747, 0.3850649, 0.1430804],
    [0.2225045, 0.7168786, 0.0606169],
    [0.0139322, 0.0971045, 0.7141733],
]
__sRGB1_to_XYZ_under_D65 = [
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
]

# XYZ to sRGB1 matrix [M]^-1, with CIE 1931 2° whitepoint reference values:
__XYZ_to_sRGB1_under_D50 = [
    [ 3.1338561, -1.6168667, -0.4906146],
    [-0.9787684,  1.9161415,  0.0334540],
    [ 0.0719453, -0.2289914,  1.4052427],
]
__XYZ_to_sRGB1_under_D65 = [
    [ 3.2404542, -1.5371385, -0.4985314],
    [-0.9692660,  1.8760108,  0.0415560],
    [ 0.0556434, -0.2040259,  1.0572252],
]

def __linear_RGB_to_sRGB(linear_RGB):
    return [
        12.92 * v if v <= 0.0031308
        else 1.055 * (v ** (1 / 2.4)) - 0.055
        for v in linear_RGB
    ]

def __sRGB_to_linear_RGB(sRGB):
    return [
        V / 12.92 if V <= 0.04045
        else ((V + 0.055) / 1.055) ** 2.4
        for V in sRGB
    ]

def __luminance(linear_RGB):
    r, g, b = linear_RGB
    return [0.212671 * r, 0.715160 * g, 0.072169 * b]

def __mat_mul(m3, v3):
    return [
        m3[0][0] * v3[0] + m3[0][1] * v3[1] + m3[0][2] * v3[2],
        m3[1][0] * v3[0] + m3[1][1] * v3[1] + m3[1][2] * v3[2],
        m3[2][0] * v3[0] + m3[2][1] * v3[1] + m3[2][2] * v3[2],
    ]

###############################################################################
###############################################################################

##
## sRGB
##

min_sRGB = [  0,   0,   0]
max_sRGB = [255, 255, 255]

##
## HSV
##

min_HSV = [  0,   0,   0]
max_HSV = [360, 100, 100]

def __HSV_to_sRGB(color):
    h, s, v = color
    h /= 60 # [0, 360] -> [0, 5]
    s /= 100
    v /= 100
    hi = int(h) % 6 # [0, 5] -> {0, 1, 2, 3, 4, 5}

    f = h - int(h)
    p = 255 * v * (1 - s)
    q = 255 * v * (1 - (s * f))
    t = 255 * v * (1 - (s * (1 - f)))
    v *= 255

    if hi == 0:
        return [v, t, p]
    elif hi == 1:
        return [q, v, p]
    elif hi == 2:
        return [p, v, t]
    elif hi == 3:
        return [p, q, v]
    elif hi == 4:
        return [t, p, v]
    else: # == 5
        return [v, p, q]

def __sRGB_to_HSV(color):
    r, g, b = [component / 255 for component in color]

    v = max(r, g, b)
    chroma = v - min(r, g, b)
    s = 0 if v == 0 else chroma / v
    h = (
        0 if chroma == 0
        else 60 * (    (g - b) / chroma) if v == r
        else 60 * (2 + (b - r) / chroma) if v == g
        else 60 * (4 + (r - g) / chroma) #  v == b
    )

    assert 0 <= h < 360
    return [h, 100 * s, 100 * v]

##
## CMY
##

min_CMY = [  0,   0,   0]
max_CMY = [100, 100, 100]

def __CMY_to_sRGB(color):
    c, m, y = [component / 100 for component in color]
    return [255 * (1 -  _) for _ in [c, m, y]]

def __sRGB_to_CMY(color):
    r, g, b = [component / 255 for component in color]
    return [100 * (1 - _) for _ in [r, g, b]]

##
## XYZ
##

min_XYZ = [0, 0, 0]

def __XYZ_to_sRGB(color, max_XYZ=__d65):
    assert max_XYZ in [__d50, __d65], f"invalid whitepoint [{', '.join(max_XYZ)}]"

    x, y, z = [component / white for component, white in zip(color, max_XYZ)]
    if max_XYZ == __d50:
        r, g, b = __linear_RGB_to_sRGB(
            __mat_mul(__XYZ_to_sRGB1_under_D50, [x, y, z])
        )
    else: # __d65 (default)
        r, g, b = __linear_RGB_to_sRGB(
            __mat_mul(__XYZ_to_sRGB1_under_D65, [x, y, z])
        )

    return [255 * min(max(0, _), 1) for _ in [r, g, b]]

def __sRGB_to_XYZ(color, max_XYZ=__d65):
    assert max_XYZ in [__d50, __d65], f"invalid whitepoint [{', '.join(max_XYZ)}]"

    r, g, b = __sRGB_to_linear_RGB(
        [component / 255 for component in color]
    )
    if max_XYZ == __d50:
        x, y, z = __mat_mul(__sRGB1_to_XYZ_under_D50, [r, g, b])
    else: # __d65 (default)
        x, y, z = __mat_mul(__sRGB1_to_XYZ_under_D65, [r, g, b])

    return [white * _ for _, white in zip([x, y, z], max_XYZ)]

##
## CIELAB
##

min_CIELAB = [  0, -100, -100]
max_CIELAB = [100,  100,  100]

# __kappa * __epsilon == 8
__epsilon = 216 / 24389 # 0.008856
__kappa = 24389 / 27 # 903.3

def __CIELAB_to_XYZ(color, max_XYZ=__d65):
    assert max_XYZ in [__d50, __d65], f"invalid whitepoint [{', '.join(max_XYZ)}]"

    L, a, b = color
    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    x = fx ** 3 if fx ** 3 > __epsilon else (116 * fx - 16) / __kappa
    y = ((L + 16) / 116) ** 3 if L > 8 else L / __kappa
    z = fz ** 3 if fz ** 3 > __epsilon else (116 * fz - 16) / __kappa

    return [white * _ for _, white in zip([x, y, z], max_XYZ)]

def __XYZ_to_CIELAB(color, max_XYZ=__d65):
    assert max_XYZ in [__d50, __d65], f"invalid whitepoint [{', '.join(max_XYZ)}]"

    x, y, z = [component / white for component, white in zip(color, max_XYZ)]
    fx = x ** (1 / 3) if x > __epsilon else (__kappa * x + 16) / 116
    fy = y ** (1 / 3) if y > __epsilon else (__kappa * y + 16) / 116
    fz = z ** (1 / 3) if z > __epsilon else (__kappa * z + 16) / 116

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return [L, a, b]

###############################################################################
###############################################################################

__COLOR_SPACES = ["sRGB", "HSV", "CMY", "XYZ", "CIELAB"]

def __convert(color, init, dest):
    assert init in __COLOR_SPACES, f"invalid init '{init}'"
    assert dest in __COLOR_SPACES, f"invalid dest '{dest}'"
    if init == dest:
        return color

    if init == "HSV":
        color = __HSV_to_sRGB(color)
    elif init == "CMY":
        color = __CMY_to_sRGB(color)
    elif init == "XYZ":
        color = __XYZ_to_sRGB(color)
    elif init == "CIELAB":
        color = __XYZ_to_sRGB(__CIELAB_to_XYZ(color))
    else: # sRGB
        pass

    if dest == "HSV":
        return __sRGB_to_HSV(color)
    elif dest == "CMY":
        return __sRGB_to_CMY(color)
    elif dest == "XYZ":
        return __sRGB_to_XYZ(color)
    elif dest == "CIELAB":
        return __XYZ_to_CIELAB(__sRGB_to_XYZ(color))
    else:
        assert False

###############################################################################
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
###############################################################################

COLOR_SPACE_ALIASES = [
    # sRGB
    "rgb",    # r,g,b   ∈ [0, 255]

    # HSV
    "hsv",    # h       ∈ [0.0, 360.0)
              # s,v     ∈ [0.0, 1.0]

    # CMY
    "cmy",    # c,m,y   ∈ [0.0, 100.0]

    # CMYK
    "cmyk",   # c,m,y,k ∈ [0.0, 100.0]

    # XYZ
    "xyz",    # x,y,z   ∈ [0.0, 1.0]

    # CIELAB
    "cielab"  # L*,a*,b*
]

def get_parser():
    parser = argparse.ArgumentParser(description="Color space converter.")
    parser.add_argument("from_space",
                        type=str,
                        metavar="from",
                        choices=COLOR_SPACE_ALIASES)
    parser.add_argument("to_space",
                        type=str,
                        metavar="to",
                        choices=COLOR_SPACE_ALIASES)
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

# References:
#   https://www.mathworks.com/help/images/ref/whitepoint.html
#   http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
#   http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html