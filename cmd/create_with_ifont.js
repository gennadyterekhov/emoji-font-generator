import ifont from 'ifont';
import fs from 'node:fs';

function readSvgFileSync(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');

  } catch (error) {
    throw new Error(`Error reading JSON file: ${error.message}`);
  }
}

function readJsonFileSync(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    throw new Error(`Error reading JSON file: ${error.message}`);
  }
}

function getAiDictionary() {
  return readJsonFileSync('config/ai_output.json')
}

function getIfontOptions(dict) {
  const options = {
    icons: []
  }

  for (let i; i < dict.length; i++) {
    const wordformData = dict[i]
    const svgPath = `emojis/combined/${wordformData['wordform']}.svg`
    const svgContent = readSvgFileSync(svgPath)
    options.icons.push({name: wordformData['wordform'], content: svgContent});
  }

  return options
}

function main() {
  const dict = getAiDictionary()
  const options = getIfontOptions(dict)
  // const ttf = ifont({
  //   icons: [
  //     {name: 'circle', content: '<svg>...</svg>'},
  //     {name: 'square', content: '<svg>...</svg>'},
  //     {name: 'triangle', content: '<svg>...</svg>'},
  //   ]
  // });
  const ttf = ifont(options);
  fs.writeFileSync('ifont.ttf', ttf);
}

main()