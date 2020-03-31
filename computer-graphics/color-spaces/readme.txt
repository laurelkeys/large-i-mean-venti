usage: convert.py [-h] [--whitepoint {50,65}] from to color color color

Color space converter for sRGB, CMY, HSV, XYZ and CIELAB.
Assumes the following ranges:
  [0, 255] for sRGB; 
  [0.0, 100.0] for CMY; 
  [0.0, 360.0) for HSV hue;
  [0.0, 1.0] for HSV saturation and value;
  [0.0, 100.0] for XYZ.
The three `color` arguments define the tristimulus values (i.e. the color components).

positional arguments:
  from                  Initial color space
  to                    Destination color space
  color                 Tristimulus values (i.e. color components)

optional arguments:
  -h, --help            show this help message and exit
  --whitepoint {50,65}, -D {50,65}
                        Reference whitepoint of illuminant series D