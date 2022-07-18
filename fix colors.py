from PIL import Image

image1 = 'old_comb.png'
image2 = 'comb.png'

size = (512, 512)
#

def from_hex(hex):
    rgb = []
    hex = hex[1:-1]
    for i in (6, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)
    return tuple(rgb)
def to_hex(color): return '#%02x%02x%02x%02x' % (255, color[0], color[1], color[2])


image1 = Image.open(image1)
image2 = Image.open(image2)

x, y = 0, 0
edits = {}

with open('colors.meta', 'r') as f: lines = f.readlines()
for line in lines:
    name, data = line.split(': ')
    if data.startswith('#'): edits[name] = from_hex(data)

while y < size[1]:
    while x < size[0]:
        color = image1.getpixel((x, y))
        for c in list(edits):
            if color == edits[c]:
                edits[c] = image2.getpixel((x, y))
        x += 1
    y += 1
    x = 0
for edit in list(edits):
    i = 0
    while i < len(lines):
        if lines[i].startswith(edit):
            lines[i] = f'{edit}: {to_hex(edits[edit])}\n'
        i += 1

with open('colors_new.meta', 'w') as f:
    f.writelines(lines)