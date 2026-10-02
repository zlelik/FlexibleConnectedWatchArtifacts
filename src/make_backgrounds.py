#!/usr/bin/env python3
"""Generate the day and night watch face backgrounds, one pair per screen resolution.

Every pixel is written as a palette index, so the file never contains a colour that is not in the
palette: no anti-aliasing, no gradients, nothing to dither. The encoder below writes the PNG itself
rather than going through an imaging library, which keeps three things under control:

  * the palette is exactly the colours asked for, in a known order
  * the bit depth is the smallest PNG allows for that number of colours, 1, 2 or 4 bits per pixel
  * every row filter is tried against three deflate strategies and the smallest result is written

Colours come from the Garmin 64 colour device palette, every channel being 0x00, 0x55, 0xAA or 0xFF,
which is what a 64 colour Memory-In-Pixel watch shows without converting anything. They were checked
against all_garmin_64colors_watch_colors.html.

Every image is a full rectangle with no transparency. A round watch shows the inscribed circle of its
framebuffer and never displays the corners, so there is nothing to mask off.
"""

import zlib, struct, math, os

#--------------------------------------------------------------------------------------------------
# Colours
#--------------------------------------------------------------------------------------------------

YELLOW     = (0xFF, 0xAA, 0x00)     # Garmin COLOR_YELLOW, the sun and the moon
DK_BLUE    = (0x00, 0x00, 0xAA)     # night sky
DEEP_WATER = (0x00, 0x00, 0x55)     # night lake, darker than the night sky
LT_BLUE    = (0x00, 0xAA, 0xFF)     # Garmin COLOR_BLUE, day sky
DAY_WATER  = (0x00, 0x55, 0xAA)     # day lake, lighter than the night lake
BLACK      = (0x00, 0x00, 0x00)     # night mountain
BROWN      = (0xAA, 0x55, 0x00)     # day mountain
WHITE      = (0xFF, 0xFF, 0xFF)     # the pale state of a two colour Instinct display

#A picture is built out of four logical codes and each variant says which colour every code takes.
#The picture fills the frame whatever the shape of the screen: a round watch shows the inscribed
#circle and never displays the corners of the bitmap, so masking them would buy nothing and cost a
#fifth palette entry, which is the difference between two and four bits per pixel.
SKY, WATER, MOUNTAIN, DISC = 0, 1, 2, 3

NIGHT = {SKY: DK_BLUE, WATER: DEEP_WATER, MOUNTAIN: BLACK, DISC: YELLOW}
DAY   = {SKY: LT_BLUE, WATER: DAY_WATER,  MOUNTAIN: BROWN, DISC: YELLOW}

#An Instinct display has two colours, so sky and water share one and the mountain and the disc share
#the other. At night the pale colour is left for the peak and the moon, which reads as moonlight on
#the mountain; by day the sky is pale and everything in front of it is dark.
MONO_NIGHT = {SKY: BLACK, WATER: BLACK, MOUNTAIN: WHITE, DISC: WHITE}
MONO_DAY   = {SKY: WHITE, WATER: WHITE, MOUNTAIN: BLACK, DISC: BLACK}

#--------------------------------------------------------------------------------------------------
# Composition, in fractions of the image so every resolution gets the same picture
#--------------------------------------------------------------------------------------------------

HORIZON = 0.70                      # the lake and sky border, 30% up from the bottom of the image

#One big mountain on the right, with two small ones on the left for depth. The big one's left flank
#breaks at 0.48 so the slope steepens towards the summit rather than running as one straight line,
#and its right flank falls away quickly into the frame. The two on the left reach 13% and 20% of the
#big one's height above the water, and the ridge returns to the waterline between the groups so they
#read as separate mountains rather than as one range.
RIDGE = [(0.00, 0.705), (0.080, 0.638), (0.135, 0.692), (0.195, 0.605), (0.26, 0.705),
         (0.48, 0.52), (0.72, 0.22), (0.88, 0.50), (1.00, 0.705)]

#The moon and the sun are on the left, in clear sky well away from the summit.
DISC_X, DISC_Y = 0.27, 0.235

MOON_R       = 0.085                # the moon is a plain crescent, so it can be the larger disc
LIT_FRACTION = 0.25                 # of the moon's disc, which makes a waxing crescent

SUN_R     = 0.062                   # the filled inner circle of the sun
SUN_BEAM  = 0.124                   # how far the beams reach from the centre, twice the inner circle
SUN_BEAMS = 8                       # beams at every 45 degrees, the way a child draws one
BEAM_HALF = 0.009                   # half the thickness of a beam

REFLECTION = [(0.035, 0.90), (0.080, 0.60), (0.130, 0.35)]   # offset below the horizon, width as a fraction of the disc


def ridge_height(x, w, h):
    """The y of the mountain silhouette at column x, in pixels."""
    fx = x / float(w - 1)
    for i in range(len(RIDGE) - 1):
        x0, y0 = RIDGE[i]
        x1, y1 = RIDGE[i + 1]
        if x0 <= fx <= x1:
            t = (fx - x0) / (x1 - x0)
            return (y0 + t * (y1 - y0)) * h
    return HORIZON * h


def moon_pixel(dx, dy, r):
    """True where a waxing crescent is lit.

    The terminator of a crescent projects to an ellipse whose horizontal semi axis is r*|2k-1|. The
    lit part is then what lies right of the centre line and outside that ellipse, which is exactly k
    of the area of the disc.
    """
    if dx * dx + dy * dy > r * r:
        return False
    term = r * abs(2.0 * LIT_FRACTION - 1.0)
    return dx >= 0 and (term == 0 or (dx * dx) / (term * term) + (dy * dy) / (r * r) >= 1.0)


def sun_pixel(dx, dy, r, beam, half):
    """True inside the filled circle, and along any beam leaving it."""
    d2 = dx * dx + dy * dy
    if d2 <= r * r:
        return True
    if d2 > beam * beam:
        return False
    for i in range(SUN_BEAMS):
        a = 2.0 * math.pi * i / SUN_BEAMS
        along = dx * math.cos(a) + dy * math.sin(a)
        across = abs(dx * math.sin(a) - dy * math.cos(a))
        if along > 0 and across <= half:
            return True
    return False


def build(w, h, night):
    """One image as a list of rows of the logical codes above, not of palette indices."""
    horizon = int(round(HORIZON * h))
    cx, cy = DISC_X * w, DISC_Y * h
    moon_r = MOON_R * w
    sun_r, sun_beam, beam_half = SUN_R * w, SUN_BEAM * w, max(1.0, BEAM_HALF * w)
    reach = moon_r if night else sun_beam

    rows = []
    for y in range(h):
        row = bytearray(w)
        for x in range(w):
            #the disc, drawn before anything else so it is never cut by the sky
            dx, dy = x - cx, y - cy
            if abs(dx) <= reach and abs(dy) <= reach:
                if moon_pixel(dx, dy, moon_r) if night else sun_pixel(dx, dy, sun_r, sun_beam, beam_half):
                    row[x] = DISC
                    continue

            if y >= horizon:
                #the lake, with the disc reflected straight below it
                row[x] = WATER
                for offset, width in REFLECTION:
                    ry = horizon + offset * h
                    if abs(y - ry) <= max(0.5, 0.006 * h) and abs(dx) <= width * (moon_r if night else sun_r):
                        row[x] = DISC
                        break
                continue

            row[x] = MOUNTAIN if y >= ridge_height(x, w, h) else SKY
        rows.append(row)
    return rows


#--------------------------------------------------------------------------------------------------
# PNG encoding
#--------------------------------------------------------------------------------------------------

def chunk(tag, data):
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)


def pack_row(row, depth):
    """Pack palette indices into a PNG scanline at 1, 2, 4 or 8 bits per pixel."""
    if depth == 8:
        return bytes(row)
    per = 8 // depth
    out = bytearray((len(row) + per - 1) // per)
    for i, v in enumerate(row):
        out[i // per] |= (v & ((1 << depth) - 1)) << (8 - depth * (i % per + 1))
    return bytes(out)


def filtered(lines, bpp_bytes, kind):
    """Apply one PNG row filter to every scanline. 0 none, 1 sub, 2 up, 3 average, 4 paeth."""
    out = bytearray()
    prev = bytes(len(lines[0]))
    for line in lines:
        out.append(kind)
        if kind == 0:
            out += line
        elif kind == 1:
            out += bytes((line[i] - (line[i - bpp_bytes] if i >= bpp_bytes else 0)) & 0xFF for i in range(len(line)))
        elif kind == 2:
            out += bytes((line[i] - prev[i]) & 0xFF for i in range(len(line)))
        elif kind == 3:
            out += bytes((line[i] - (((line[i - bpp_bytes] if i >= bpp_bytes else 0) + prev[i]) >> 1)) & 0xFF for i in range(len(line)))
        else:
            res = bytearray()
            for i in range(len(line)):
                a = line[i - bpp_bytes] if i >= bpp_bytes else 0
                b = prev[i]
                c = prev[i - bpp_bytes] if i >= bpp_bytes else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                res.append((line[i] - pred) & 0xFF)
            out += res
        prev = line
    return bytes(out)


def write_png(path, rows, scheme):
    """Write an indexed PNG, trying every row filter and keeping the smallest deflate result.

    The palette has one entry per distinct colour the scheme uses: two for an Instinct screen, which
    fit in one bit per pixel, and four otherwise, which fit in two.
    """
    order = []
    for code in (SKY, WATER, MOUNTAIN, DISC):
        if scheme[code] not in order:
            order.append(scheme[code])

    index = {}
    plte = b''
    for colour in order:
        index_of = len(plte) // 3
        plte += bytes(colour)
        for code in (SKY, WATER, MOUNTAIN, DISC):
            if scheme[code] == colour:
                index[code] = index_of

    colours = len(plte) // 3
    depth = 1 if colours <= 2 else (2 if colours <= 4 else 4)
    w, h = len(rows[0]), len(rows)

    lines = [pack_row(bytearray(index[v] for v in row), depth) for row in rows]
    best = None
    for kind in (0, 1, 2, 3, 4):
        raw = filtered(lines, 1, kind)
        for strategy in (zlib.Z_DEFAULT_STRATEGY, zlib.Z_FILTERED, zlib.Z_RLE):
            co = zlib.compressobj(9, zlib.DEFLATED, 15, 9, strategy)
            data = co.compress(raw) + co.flush()
            if best is None or len(data) < len(best):
                best = data

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, depth, 3, 0, 0, 0))
    png += chunk(b'PLTE', plte)
    png += chunk(b'IDAT', best)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png), depth, colours


#--------------------------------------------------------------------------------------------------

OUT = os.path.dirname(os.path.abspath(__file__))

#resolution, screen shape, and whether the display has only two colours. The shape is recorded
#because it says which watches a row is for, not because it changes the picture: every image fills
#its frame and a round watch cuts it to the circle itself.
TARGETS = [
    (240, 240, 'round',        False),
    (260, 260, 'round',        False),
    (280, 280, 'round',        False),
    (360, 360, 'round',        False),
    (390, 390, 'round',        False),
    (416, 416, 'round',        False),
    (448, 486, 'rectangle',    False),
    (454, 454, 'round',        False),
    (466, 466, 'round',        False),
    (166, 166, 'semi-octagon', True),
    (176, 176, 'semi-octagon', True),
]

if __name__ == '__main__':
    print(f"{'file':28} {'bytes':>7} {'bits/px':>8} {'colours':>8}  shape")
    total = 0
    for w, h, shape, mono in TARGETS:
        for night in (True, False):
            name = ('NightBG' if night else 'DayBG') + f'_{w}x{h}.png'
            scheme = (MONO_NIGHT if night else MONO_DAY) if mono else (NIGHT if night else DAY)
            rows = build(w, h, night)
            size, depth, colours = write_png(os.path.join(OUT, name), rows, scheme)
            total += size
            print(f"{name:28} {size:7} {depth:8} {colours:8}  {shape}")
    print(f"{'':28} {total:7} bytes in total")
