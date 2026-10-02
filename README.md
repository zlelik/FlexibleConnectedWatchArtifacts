# FlexibleConnectedWatchImages

This repository hosts images for FlexibleConnectedWatch app for Garmin watches.

# Day and night background images

One pair of background images per screen resolution, for every Garmin watch released in 2023 or later. `make_backgrounds.py` produces all of them and is the only place the pictures are defined; nothing here was drawn by hand.

## The picture

One big mountain on the right and two small ones on the left, at 13% and 20% of its height above the water, with the lake and sky border at 30% of the image height from the bottom. The ridge returns to the waterline between the two groups so they read as separate mountains rather than as one range.

The night image carries a waxing crescent moon on the left with exactly 25% of the disc lit. The day image puts the sun in the same place, a filled circle with eight beams leaving its edge, and both the water and the sky are a lighter blue than at night. The moon and the sun are reflected in the water as three lines below the disc.

## Colours

Every colour is from the Garmin 64 colour device palette, where each channel is `0x00`, `0x55`, `0xAA` or `0xFF`. Each one was checked against `all_garmin_64colors_watch_colors.html`, and that file is exactly the 64 combinations of those four channel values.

| | Night | Day |
|---|---|---|
| Sky | `0x0000AA` dark blue | `0x00AAFF` light blue, Garmin `COLOR_BLUE` |
| Lake | `0x000055` deeper blue | `0x0055AA` blue |
| Mountains | `0x000000` black | `0xAA5500` brown |
| Moon and sun | `0xFFAA00` yellow, Garmin `COLOR_YELLOW` | `0xFFAA00` yellow |

Of the 53 watches these images are for, 39 have a 65,536 colour AMOLED screen, 10 have a 64 colour Memory-In-Pixel screen and 4 have a 2 colour Instinct screen. None has the 14 colour palette of `all_garmin_14colors_watch_colors.html`, which belongs to the fēnix 3 generation, so nothing here has to fit into it.

Every image is a full rectangle and none of them carries transparency. A round watch shows the inscribed circle of its framebuffer and never displays the corners, so there is nothing to mask off: the corner pixels are written and the glass ignores them. Leaving them out keeps each picture at four colours, which PNG stores at two bits per pixel rather than the four a fifth entry would need, and an opaque bitmap is also the cheapest thing a watch can draw.

An Instinct display has two colours, so the 166x166 and 176x176 images are drawn in black and white instead: at night the sky and the lake are black and the peaks and the moon are white, and by day the sky and the lake are white and the peaks and the sun are black.

## Files

`DayBG_<width>x<height>.png` and `NightBG_<width>x<height>.png`, which is the naming the `BgImageUrls` setting already uses. The resolutions are 166x166, 176x176, 240x240, 260x260, 280x280, 360x360, 390x390, 416x416, 448x486, 454x454 and 466x466. `Supported devices_v3_20261002.xlsx` in the directory above lists which watch takes which pair.

## Size

Each file is between 429 and 1,567 bytes, 22 KB for all 22. The script writes the PNG itself rather than going through an imaging library, which keeps three things under control: the palette contains exactly the colours listed above and in a known order, the bit depth is the smallest PNG allows for that number of colours, which is one bit per pixel for the two Instinct resolutions and two for every other image rather than eight, and every row filter is tried against three deflate strategies so the smallest result is the one written. Measured over all 22 files that is 14% smaller than the same images saved by Pillow with `optimize=True`, and 23% smaller than a plain 8 bit palette file.

## Regenerating

```bash
python3 make_backgrounds.py
```

Edit `TARGETS` to add a resolution, `RIDGE` to reshape the mountains, `HORIZON` to move the border between the lake and the sky, `LIT_FRACTION` to change the phase of the moon, and `SUN_BEAMS` to change how many beams the sun has.
