import textwrap
import sys
import argparse


PRE_TEMPLATE = textwrap.dedent("""
(Absolute distance mode)
G90
(Program coordiantes are mm)
G21
(XY plane select)
G17
(Set feedrate)
F{feedrate}

(Move to lower left corner)
G0 Z1
G0 X{minx} Y{miny}
""")

ONEPASS_TEMPLATE = textwrap.dedent("""
(pass {pass_index}, cutting at {depth} deep)
G1 Z{depth}
G1 X{minx} Y{maxy}
G1 X{maxx} Y{maxy}
G1 X{maxx} Y{miny}
G0 Z1
(Move to lower left corner)
G0 X{minx} Y{miny}
""")

END_TEMPLATE = textwrap.dedent("""
(Move mill to safe height)
G0 Z10
(End of program)
M2
""")


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('cutter', type=float)
    parser.add_argument('feedrate', type=int)
    parser.add_argument('xsize', type=float)
    parser.add_argument('ysize', type=float)
    parser.add_argument('depth', type=float)
    parser.add_argument('maxcutdepth', type=float)
    return parser.parse_args()


def roundednum(num):
    return "{0:.2f}".format(num)


def roundeddict(d):
    return dict((k, roundednum(v)) for (k, v) in d.iteritems())


def main():
    params = get_params()

    halfx = params.xsize / 2.0
    halfcutter = params.cutter / 2.0
    minx = - halfx + halfcutter
    miny = 0.0

    maxx = halfx - halfcutter
    maxy = params.ysize

    pre_params = roundeddict({
        'feedrate': params.feedrate,
        'minx': minx,
        'miny': miny
    })

    sys.stdout.write(PRE_TEMPLATE.format(**pre_params))

    actual_depth = -params.maxcutdepth
    pass_index = 1

    while True:
        onepass_params = roundeddict({
            'depth': actual_depth,
            'minx': minx,
            'maxx': maxx,
            'miny': miny,
            'maxy': maxy
        })
        sys.stdout.write(ONEPASS_TEMPLATE.format(
            pass_index=pass_index,
            **onepass_params
        ))
        if actual_depth <= -params.depth:
            break
        actual_depth -= params.maxcutdepth

    sys.stdout.write(END_TEMPLATE)


if __name__ == "__main__":
    main()
