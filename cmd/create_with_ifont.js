import ifont from 'ifont';
import fs from 'node:fs';

// Generate a TTF font, as a Uint8Array, from some SVG icons

const ttf = ifont({
  icons: [
    {name: 'circle', content: '<svg>...</svg>'},
    {name: 'square', content: '<svg>...</svg>'},
    {name: 'triangle', content: '<svg>...</svg>'},
  ]
});

fs.writeFileSync('ifont.ttf', ttf);