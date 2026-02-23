from svgutils.compose import Figure, SVG
import svgutils.transform as sg

fig2 = sg.fromfile('/Users/gena/code/projects/spectral/arabic/transliteration/python_cli/svg/emojis/1f440_resaved.svg')
print(fig2)
fig2 = sg.fromfile('emojis/1f440_resaved.svg')
print(fig2)
print(fig2.getroot())
print(fig2.getroot().scale(1).moveto(100, 100))

# obj=SVG('emojis/1f440_resaved.svg')
# obj.scale(1)

# 假设每个小 SVG 是 100x100，创建一个 200x200 的画布
# Figure(200, 200,
#        # 按 (row, col) 放置，起始点为 (0,0)
#        SVG('emojis/1f440_resaved.svg').scale(1).move(0, 0),
#        SVG('emojis/1f441_resaved.svg').scale(1).move(100, 0),
#        SVG('emojis/1f443_resaved.svg').scale(1).move(0, 100),
#        SVG('emojis/1f444_resaved.svg').scale(1).move(100, 100)
#        ).save('combined_grid.svg')

# Figure(200, 200,
#        # 按 (row, col) 放置，起始点为 (0,0)
#        sg.fromfile('emojis/1f440_resaved.svg').getroot().scale(1).moveto(0, 0),
#        sg.fromfile('emojis/1f441_resaved.svg').getroot().scale(1).moveto(100, 0),
#        sg.fromfile('emojis/1f443_resaved.svg').getroot().scale(1).moveto(0, 100),
#        sg.fromfile('emojis/1f444_resaved.svg').getroot().scale(1).moveto(100, 100)
#        ).save('combined_grid.svg')

elems = []
for i in [0, 1, 3, 4]:
    nm = f'emojis/1f44{i}.svg'
    elem = sg.fromfile(nm)
    if i == 0:
        elem.getroot().scale(1).moveto(0, 0)
    if i == 1:
        elem.getroot().scale(1).moveto(100, 0)
    if i == 3:
        elem.getroot().scale(1).moveto(0, 100)
    if i == 4:
        elem.getroot().scale(1).moveto(100, 100)
    elems.append(elem.getroot())

Figure(200, 200,
       elems[0],
       elems[1],
       elems[2],
       elems[3],
       ).save('combined_grid.svg')
