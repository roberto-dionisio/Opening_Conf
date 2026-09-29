"""Build the two institution lockups for the StaND4LQ deck.

    python3 figures/make_logos.py

Sources (both RGBA with real alpha):
    marchio_unipi_orizz_pant541.png  horizontal Pisa mark, Pantone 541 blue
    Logo_INFN.png                    INFN ellipse + "INFN", with the long
                                     "Istituto Nazionale di Fisica Nucleare"
                                     wordmark underneath (rows 240-266)

Two lockups, because they live on opposite backgrounds:

    header_stand4lq.png  white on transparent, for the dark navy header bar.
                         Small, so INFN is cropped to just the mark -- its
                         wordmark is illegible at ~110px wide.
    title_stand4lq.png   full colour, for the light title slide, where there is
                         room to carry the INFN wordmark.
"""

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
ROOT = HERE.parent

UNIPI = ROOT / "marchio_unipi_orizz_pant541.png"
INFN = ROOT / "Logo_INFN.png"

# Rows 0-214 are the ellipse + "INFN"; 240-266 are the spelled-out wordmark.
INFN_MARK_BOTTOM = 216


def trim(im):
    """Crop to the non-transparent bounding box, so gaps are measured between
    the marks themselves rather than between whatever padding each file has."""
    a = np.array(im.convert("RGBA"))
    ys, xs = np.nonzero(a[..., 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def to_white(im):
    """Recolor to white, keeping the alpha channel so edges stay antialiased."""
    a = np.array(im.convert("RGBA"))
    a[..., :3] = 255
    return Image.fromarray(a)


def scale_to_height(im, h):
    w = max(1, round(im.width * h / im.height))
    return im.resize((w, h), Image.LANCZOS)


def lockup(left, right, height, gap, rule=None):
    """Place two already-scaled marks side by side, each centred vertically in a
    box `height` tall, optionally with a thin vertical rule between them."""
    w = left.width + gap + right.width
    out = Image.new("RGBA", (w, height), (0, 0, 0, 0))
    out.alpha_composite(left, (0, (height - left.height) // 2))
    out.alpha_composite(right, (left.width + gap, (height - right.height) // 2))
    if rule is not None:
        rw = max(2, height // 110)
        bar = Image.new("RGBA", (rw, round(height * 0.78)), rule)
        out.alpha_composite(bar, (left.width + gap // 2 - rw // 2,
                                  (height - bar.height) // 2))
    return out


def main():
    unipi = trim(Image.open(UNIPI).convert("RGBA"))
    infn_full = trim(Image.open(INFN).convert("RGBA"))
    infn_mark = trim(Image.open(INFN).convert("RGBA")
                     .crop((0, 0, Image.open(INFN).width, INFN_MARK_BOTTOM)))

    # --- header: white, compact, no INFN wordmark -----------------------------
    # The INFN mark is squatter than the Pisa lockup, so matching heights exactly
    # would let it out-weigh Pisa; 0.82 evens them out optically.
    h = 300
    head = lockup(to_white(scale_to_height(unipi, h)),
                  to_white(scale_to_height(infn_mark, round(h * 0.82))),
                  h, gap=96, rule=(255, 255, 255, 90))
    head.save(ROOT / "header_stand4lq.png")
    print(f"  wrote header_stand4lq.png  {head.size}")

    # --- title slide: full colour, INFN wordmark included ---------------------
    h = 420
    title = lockup(scale_to_height(unipi, h),
                   scale_to_height(infn_full, round(h * 0.94)), h, gap=130)
    title.save(ROOT / "title_stand4lq.png")
    print(f"  wrote title_stand4lq.png  {title.size}")


if __name__ == "__main__":
    print("building StaND4LQ logo lockups")
    main()
    print("done")
