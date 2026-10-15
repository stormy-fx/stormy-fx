from PIL import Image, ImageDraw
import math
import os

# Original Minecraft-inspired blocky avatar animation.
# This is a stylized pixel-art mascot, not an official Minecraft asset.
W, H = 480, 360
FRAMES = 16
SCALE = 3
OUT = os.path.join("assets", "stormy-mascot.gif")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

BG = (9, 10, 18)
PURPLE = (158, 111, 255)
CYAN = (84, 231, 246)
SKIN = (198, 143, 103)
HAIR = (38, 27, 37)
SHIRT = (32, 33, 58)
PANTS = (25, 28, 42)
WHITE = (240, 244, 255)

def draw_frame(i):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    t = i / FRAMES
    # Ambient pixel-like particles and moving glow bands
    for k in range(13):
        x = int((k * 41 + i * 5) % W)
        y = int(24 + (k * 23) % 300)
        color = CYAN if k % 3 == 0 else PURPLE
        d.rectangle((x, y, x + 3, y + 3), fill=color)
    for band in range(3):
        x = int((i * 9 + band * 170) % (W + 160)) - 80
        d.rectangle((x, 0, x + 2, H), fill=(20, 22, 38))
    # Framed card
    d.rounded_rectangle((16, 16, W-16, H-16), radius=18, outline=(64, 60, 94), width=2)
    d.line((34, 54, 150, 54), fill=PURPLE, width=2)
    d.line((330, H-42, 446, H-42), fill=CYAN, width=2)
    d.text((34, 30), "STORMY FX  /  PIXEL MASCOT", fill=(193, 178, 255))
    d.text((34, H-34), "CREATE  •  REFINE  •  EVOLVE", fill=(128, 211, 227))

    bob = int(round(math.sin(t * math.tau) * 4))
    cx = W // 2
    # Ground shadow
    d.ellipse((cx-70, 290, cx+70, 306), fill=(22, 25, 43))
    # Legs
    d.rectangle((cx-35, 235+bob, cx-4, 285+bob), fill=PANTS)
    d.rectangle((cx+5, 235+bob, cx+36, 285+bob), fill=PANTS)
    d.rectangle((cx-39, 278+bob, cx-2, 291+bob), fill=(50, 55, 80))
    d.rectangle((cx+2, 278+bob, cx+40, 291+bob), fill=(50, 55, 80))
    # Body / hoodie
    d.rectangle((cx-48, 155+bob, cx+48, 242+bob), fill=SHIRT)
    d.rectangle((cx-48, 155+bob, cx+48, 162+bob), fill=PURPLE)
    d.rectangle((cx-8, 166+bob, cx+8, 225+bob), fill=(46, 48, 78))
    # Arms swing gently
    swing = int(round(math.sin(t * math.tau) * 5))
    d.rectangle((cx-69, 164+bob+swing, cx-49, 226+bob+swing), fill=SHIRT)
    d.rectangle((cx+49, 164+bob-swing, cx+69, 226+bob-swing), fill=SHIRT)
    d.rectangle((cx-67, 217+bob+swing, cx-51, 232+bob+swing), fill=SKIN)
    d.rectangle((cx+51, 217+bob-swing, cx+67, 232+bob-swing), fill=SKIN)
    # Neck
    d.rectangle((cx-14, 137+bob, cx+14, 163+bob), fill=SKIN)
    # Square head
    d.rectangle((cx-44, 78+bob, cx+44, 150+bob), fill=SKIN)
    # Hair cap and side blocks
    d.rectangle((cx-47, 70+bob, cx+47, 96+bob), fill=HAIR)
    d.rectangle((cx-47, 85+bob, cx-34, 122+bob), fill=HAIR)
    d.rectangle((cx+34, 85+bob, cx+47, 116+bob), fill=HAIR)
    d.rectangle((cx-35, 72+bob, cx-7, 83+bob), fill=(65, 42, 56))
    # Eyes blink for two frames per cycle
    blink = i in (7, 8)
    if blink:
        d.line((cx-27, 111+bob, cx-13, 111+bob), fill=HAIR, width=4)
        d.line((cx+13, 111+bob, cx+27, 111+bob), fill=HAIR, width=4)
    else:
        d.rectangle((cx-27, 105+bob, cx-14, 119+bob), fill=WHITE)
        d.rectangle((cx+14, 105+bob, cx+27, 119+bob), fill=WHITE)
        d.rectangle((cx-21, 109+bob, cx-15, 118+bob), fill=CYAN)
        d.rectangle((cx+15, 109+bob, cx+21, 118+bob), fill=CYAN)
    # Pixel smile
    d.rectangle((cx-13, 132+bob, cx+13, 137+bob), fill=(104, 48, 55))
    d.rectangle((cx-7, 132+bob, cx+7, 134+bob), fill=(246, 205, 183))
    # Tiny floating pixel cube
    cube_x = cx + 92 + int(math.sin(t*math.tau)*6)
    cube_y = 125 + int(math.cos(t*math.tau)*7)
    d.rectangle((cube_x-13, cube_y-13, cube_x+13, cube_y+13), fill=(42, 45, 72), outline=CYAN, width=2)
    d.line((cube_x-13, cube_y-13, cube_x, cube_y-22, cube_x+13, cube_y-13), fill=PURPLE, width=2)
    d.line((cube_x, cube_y-22, cube_x, cube_y+3), fill=CYAN, width=2)
    return im

frames = [draw_frame(i) for i in range(FRAMES)]
frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=95,
    loop=0,
    optimize=True,
    disposal=2
)
print(f"Generated {OUT} ({os.path.getsize(OUT)} bytes)")
