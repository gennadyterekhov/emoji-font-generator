// this solution doesn't support svg's `defs` . so it won't work
import ifont from 'ifont';
import fs from 'node:fs';
import path from 'path';


/**
 * Reads all files in a directory and returns a Map of filename to file contents
 * @param {string} directoryPath - Path to the directory to read
 * @returns {Map<string, string>} Map where keys are filenames and values are file contents
 */
function getFilesContentMap(directoryPath) {
  const filesMap = {}

  try {
    // Read all files in the directory
    const files = fs.readdirSync(directoryPath);

    // Filter for files only (not subdirectories)
    files.forEach(file => {
      console.log('file', file);
      const filePath = path.join(directoryPath, file);
      const stat = fs.statSync(filePath);

      if (stat.isFile()) {
        try {
          // Read file contents as UTF-8 string
          const content = fs.readFileSync(filePath, 'utf8');
          // filesMap.set(file, content);
          filesMap[file] = content;

        } catch (readError) {
          console.error(`Error reading file ${file}:`, readError.message);
        }
      }
    });

  } catch (error) {
    console.error(`Error reading directory ${directoryPath}:`, error.message);
  }

  return filesMap;
}

/**
 * Asynchronously reads all files in a directory and returns a Map of filename to file contents
 * @param {string} directoryPath - Path to the directory to read
 * @returns {Promise<Map<string, string>>} Promise that resolves to a Map of filename to file contents
 */
async function getFilesContentMapAsync(directoryPath) {
  const filesMap = {};

  try {
    // Read all files in the directory
    const files = await fs.readdir(directoryPath);

    // Process all files
    await Promise.all(files.map(async (file) => {
      const filePath = path.join(directoryPath, file);
      const stat = await fs.stat(filePath);

      if (stat.isFile()) {
        try {
          const content = await fs.readFile(filePath, 'utf8');
          // filesMap.set(file, content);
          filesMap[file] = content;
        } catch (readError) {
          console.error(`Error reading file ${file}:`, readError.message);
        }
      }
    }));

  } catch (error) {
    console.error(`Error reading directory ${directoryPath}:`, error.message);
  }

  return filesMap;
}


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

function getIfontOptions(dict = {}) {

  const fileToCont = getFilesContentMap('/Users/gena/code/projects/languages/lirbantu/emojis/combined')
  const options = {
    icons: []
  }

  // for (let i; i < dict.length; i++) {
  //   const wordformData = dict[i]
  //   const svgPath = `emojis/combined/${wordformData['wordform']}.svg`
  //   const svgContent = readSvgFileSync(svgPath)
  //   options.icons.push({name: wordformData['wordform'], content: svgContent});
  // }
  for (const key in fileToCont) {
    if (fileToCont.hasOwnProperty(key)) { // Ensures only own properties are accessed

      const word = key.replaceAll('.svg', '')
      options.icons.push({name: word, content: fileToCont[key]});
    }
  }
  return options
}

function main() {
  // const dict = getAiDictionary()
  const options = getIfontOptions()
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