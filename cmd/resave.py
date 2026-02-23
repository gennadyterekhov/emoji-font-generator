from svgutils.compose import Figure, SVG
import svgutils.transform as sg

for i in [0, 1, 3, 4]:
    nm = f'emojis/1f44{i}.svg'
    nm2 = f'emojis/1f44{i}_resaved.svg'
    fig = sg.fromfile(nm)
    fig.save(nm2)
