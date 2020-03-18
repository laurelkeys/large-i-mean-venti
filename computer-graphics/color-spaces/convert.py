import os
import argparse


COLOR_SPACE_ALIASES = [
    # sRGB
    "rgb",    # r, g, b  ∈ [0, 255]

    # HSV
    "hsv",    # h        ∈ [0.0, 360.0)
              # s, v     ∈ [0.0, 1.0]

    # CMY
    "cmy",    # c, m, y  ∈ [0.0, 100.0]

    # XYZ
    "xyz",    # x, y, z  ∈ [0.0, 100.0]

    # CIELAB
    "cielab"  # L        ∈ [0.0, 100.0]
              # a, b     ∈ [-100.0, 100.0]
]


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

# References:
#   https://www.mathworks.com/help/images/ref/whitepoint.html
#   http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html


###############################################################################
###############################################################################


def __linear_RGB_to_sRGB(linear_RGB):
    return [
        12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        for v in linear_RGB
    ]


def __sRGB_to_linear_RGB(sRGB):
    return [
        V / 12.92 if V <= 0.04045 else ((V + 0.055) / 1.055) ** 2.4
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

min_HSV = [  0, 0, 0]
max_HSV = [360, 1, 1]

def __HSV_to_sRGB(color):
    h, s, v = color

    chroma = v * s
    h /= 60 # [0, 360] -> [0, 6]
    x = chroma * (1 - abs((h % 2) - 1))
    m = v - chroma

    return [
        255 * (_ + m)
        for _ in (
                 [chroma, x, 0] if 0 <= h <= 1
            else [x, chroma, 0] if 1 < h <= 2
            else [0, chroma, x] if 2 < h <= 3
            else [0, x, chroma] if 3 < h <= 4
            else [x, 0, chroma] if 4 < h <= 5
            else [chroma, 0, x] if 5 < h <= 6
            else [0, 0, 0]
        )
    ]

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
    return [h, s, v]

##
## CMY
##

min_CMY = [  0,   0,   0]
max_CMY = [100, 100, 100]

def __CMY_to_sRGB(color):
    c, m, y = [component / 100 for component in color]
    return [255 * (1 - _) for _ in [c, m, y]]

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
        r, g, b = __linear_RGB_to_sRGB(__mat_mul(__XYZ_to_sRGB1_under_D50, [x, y, z]))
    else: # __d65 (default)
        r, g, b = __linear_RGB_to_sRGB(__mat_mul(__XYZ_to_sRGB1_under_D65, [x, y, z]))

    return [255 * min(max(0, _), 1) for _ in [r, g, b]]

def __sRGB_to_XYZ(color, max_XYZ=__d65):
    assert max_XYZ in [__d50, __d65], f"invalid whitepoint [{', '.join(max_XYZ)}]"

    r, g, b = __sRGB_to_linear_RGB([component / 255 for component in color])
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

__epsilon = 216 / 24389 # 0.008856
__kappa = 24389 / 27 # 903.3
# __kappa * __epsilon == 8

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


def __convert(color, init, dest, max_XYZ):
    if init == dest:
        return color

    if init == "hsv":
        color = __HSV_to_sRGB(color)
    elif init == "cmy":
        color = __CMY_to_sRGB(color)
    elif init == "xyz":
        if dest == "cielab":
            return __XYZ_to_CIELAB(color, max_XYZ)
        color = __XYZ_to_sRGB(color, max_XYZ)
    elif init == "cielab":
        if dest == "xyz":
            return __CIELAB_to_XYZ(color, max_XYZ)
        color = __XYZ_to_sRGB(__CIELAB_to_XYZ(color, max_XYZ), max_XYZ)
    else: # sRGB
        pass

    if dest == "hsv":
        return __sRGB_to_HSV(color)
    elif dest == "cmy":
        return __sRGB_to_CMY(color)
    elif dest == "xyz":
        return __sRGB_to_XYZ(color, max_XYZ)
    elif dest == "cielab":
        return __XYZ_to_CIELAB(__sRGB_to_XYZ(color, max_XYZ), max_XYZ)
    else: # sRGB
        return [int(component) for component in color]


###############################################################################
###############################################################################


def validate(color, color_space, max_XYZ):
    if color_space == "rgb":
        assert all(
            int(component) == component for component in color
        ), f"rgb color components must be integers {color}"
        assert all(
            0 <= component <= 255 for component in color
        ), "rgb color components must be in the range [0, 255]"

    elif color_space == "hsv":
        h, s, v = color
        assert 0.0 <= h < 360.0, "hue component must be in the range [0.0, 360.0)"
        assert 0.0 <= s <= 1.0, "saturation component must be in the range [0.0, 1.0]"
        assert 0.0 <= v <= 1.0, "value component must be in the range [0.0, 1.0]"

    elif color_space == "cmy":
        assert all(
            0.0 <= component <= 100.0 for component in color
        ), "cmy color components must be in the range [0.0, 100.0]"

    elif color_space == "xyz":
        x, y, z = color
        assert (
            0 <= x <= max_XYZ[0]
        ), f"x component must be in the range [0.0, {max_XYZ[0]:.1f}]"
        assert (
            0 <= y <= max_XYZ[1]
        ), f"y component must be in the range [0.0, {max_XYZ[1]:.1f}]"
        assert (
            0 <= z <= max_XYZ[2]
        ), f"z component must be in the range [0.0, {max_XYZ[2]:.1f}]"

    elif color_space == "cielab":
        L, a, b = color
        assert 0.0 <= L <= 100.0, f"L component must be in the range [0.0, 100.0"
        assert -100.0 <= a <= 100.0, f"a component must be in the range [-100.0, 100.0]"
        assert -100.0 <= b <= 100.0, f"b component must be in the range [-100.0, 100.0]"

    else:
        assert False, f"invalid color space '{color_space}'"


def main(args):
    from_color = [float(component) for component in args.color]
    validate(from_color, args.from_space, max_XYZ=__d50)

    to_color = __convert(
        from_color, init=args.from_space, dest=args.to_space, max_XYZ=__d50
    )
    validate(to_color, args.to_space, max_XYZ=__d50)

    def color2str(color, color_space, pts=1):
        if color_space == "rgb":
            return ", ".join([f"{_:.0f}" for _ in from_color])
        return ", ".join([f"{_:.{pts}f}" for _ in from_color])

    print(
        f"{args.from_space.upper()}({color2str(from_color, args.from_space)})",
        "to",
        f"{args.to_space.upper()}({color2str(to_color, args.to_space)})",
    )


###############################################################################
###############################################################################


def get_parser():
    parser = argparse.ArgumentParser(description="Color space converter.")
    parser.add_argument("from_space", type=str, metavar="from", choices=COLOR_SPACE_ALIASES)
    parser.add_argument("to_space", type=str, metavar="to", choices=COLOR_SPACE_ALIASES)
    parser.add_argument("color", nargs=3, type=float, action="store")
    parser.add_argument("--verbose", "-v", action="store_true", help="Increase verbosity")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = get_parser().parse_args()

    main(args)
