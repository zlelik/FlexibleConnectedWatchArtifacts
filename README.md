# FlexibleConnectedWatchArtifacts

Files published for FlexibleConnectedWatch, a configurable watch face for Garmin watches. Everything the watch face draws is set in its settings, and this repository serves what the settings point at and two ways to help write them.

| Folder | Contents |
|---|---|
| `imgs/` | The day and night background images, one pair per screen resolution. The watch face downloads them from here |
| `src/` | `make_backgrounds.py`, which draws every image in `imgs/` |
| `tools/` | `field-config-editor.html`, the fields config editor, which is used at <https://zlelik.github.io/FlexibleConnectedWatchArtifacts/field-config-editor.html> |
| `docs/` | `fields-config-prompt.md` and `bg-rules-prompt.md`, the two prompts for a language model |

# How to use the editor and the prompts

The watch face is configured with text settings, in the Connect IQ app on the phone or in Garmin Express. **Fields config** says what each text field shows and where, and **Background image rules** says which background image is drawn when.

**The editor**, <https://zlelik.github.io/FlexibleConnectedWatchArtifacts/field-config-editor.html>, previews the value of **Fields config** on any supported watch, in a browser on a phone or a PC.

1. Choose your watch.
2. Paste your **Fields config** value into the config text field, or start from the default the page opens with.
3. Read the list under **Validation**. An error is something the watch would not draw as written; a warning is worth checking, for example two fields that overlap or a field cut off by the edge of the screen.
4. Drag a field on the preview to move it. Only its `pos` changes in the text.
5. Press **Copy config** and paste the value into the **Fields config** setting.

The preview is approximate: a browser cannot use the watch's own fonts, and the background image is not drawn.

**The prompts** let a language model write a setting from a description. On the editor page, write what you want under **Ask a language model** and press **Copy prompt**; or open `docs/fields-config-prompt.md` or `docs/bg-rules-prompt.md` and replace the text under **What I want**. Paste the whole prompt into ChatGPT, Claude or another model, and paste its answer into the setting the prompt is for, **Fields config** or **Background image rules**. Put a **Fields config** answer through the editor first, so that it is checked.

# Day and night background images

One pair of background images per screen resolution the watch face supports. `src/make_backgrounds.py` produces all of them and is the only place the pictures are defined; nothing here was drawn by hand.

## The picture

One big mountain on the right and two small ones on the left, at 13% and 20% of its height above the water, with the lake and sky border at 30% of the image height from the bottom. The ridge returns to the waterline between the two groups so they read as separate mountains rather than as one range.

The night image carries a waxing crescent moon on the left with exactly 25% of the disc lit. The day image puts the sun in the same place, a filled circle with eight beams leaving its edge, and both the water and the sky are a lighter blue than at night. The moon and the sun are reflected in the water as three lines below the disc.

## Colours

Every colour is from the Garmin 64 colour device palette, where each channel is `0x00`, `0x55`, `0xAA` or `0xFF`.

| | Night | Day |
|---|---|---|
| Sky | `0x0000AA` dark blue | `0x00AAFF` light blue, Garmin `COLOR_BLUE` |
| Lake | `0x000055` deeper blue | `0x0055AA` blue |
| Mountains | `0x000000` black | `0xAA5500` brown |
| Moon and sun | `0xFFAA00` yellow, Garmin `COLOR_YELLOW` | `0xFFAA00` yellow |

The supported watches have 65,536 colour AMOLED screens, 64 colour Memory-In-Pixel screens or, on the Instinct watches, 2 colour screens. None has the 14 colour palette of the fēnix 3 generation, so nothing here has to fit into it.

Every image is a full rectangle and none of them carries transparency. A round watch shows the inscribed circle of its framebuffer and never displays the corners, so there is nothing to mask off: the corner pixels are written and the glass ignores them. Leaving them out keeps each picture at four colours, which PNG stores at two bits per pixel rather than the four a fifth entry would need, and an opaque bitmap is also the cheapest thing a watch can draw.

An Instinct display has two colours, so the 166x166 and 176x176 images are drawn in black and white instead: at night the sky and the lake are black and the peaks and the moon are white, and by day the sky and the lake are white and the peaks and the sun are black.

## Files

The images are in `imgs/`, named `DayBG_<width>x<height>.png` and `NightBG_<width>x<height>.png`, which is the naming the **Background image URLs** setting uses. The resolutions are 166x166, 176x176, 218x218, 240x240, 260x260, 280x280, 360x360, 390x390, 416x416, 448x486, 454x454 and 466x466. A watch takes the pair of its own screen resolution, 260x260 on a fēnix 7 for example, and the setting names each image by its raw address:

```
https://raw.githubusercontent.com/zlelik/FlexibleConnectedWatchArtifacts/refs/heads/main/imgs/DayBG_260x260.png
```

## Size

Each file is between 429 and 1,567 bytes, 23 KB for all 24. The script writes the PNG itself rather than going through an imaging library, which keeps three things under control: the palette contains exactly the colours listed above and in a known order, the bit depth is the smallest PNG allows for that number of colours, which is one bit per pixel for the two Instinct resolutions and two for every other image rather than eight, and every row filter is tried against three deflate strategies so the smallest result is the one written. Measured over the 22 files of the first set, that is 14% smaller than the same images saved by Pillow with `optimize=True`, and 23% smaller than a plain 8 bit palette file.

## Regenerating

```bash
python3 src/make_backgrounds.py
```

It writes all 24 files into `imgs/`, from whatever folder it is run in. Edit `TARGETS` to add a resolution, `RIDGE` to reshape the mountains, `HORIZON` to move the border between the lake and the sky, `LIT_FRACTION` to change the phase of the moon, and `SUN_BEAMS` to change how many beams the sun has.

# Licence

Copyright zlelik, all rights reserved. The files here may be used only with the FlexibleConnectedWatch watch face, in the ways `LICENSE` sets out. The third-party material `LICENSE` lists is under its own terms.
