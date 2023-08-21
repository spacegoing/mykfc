const path = require('path');
const os = require('os');
console.log(process.argv[2]);

const pkg_map = {
    "slicetool": ""
}


const binaryPath = path.join(__dirname, os.platform() === 'win32' ? 'slice-tool-custom\\dist\\KungfuSliceToolCustom' : 'path/to/binary');

console.log(__dirname)


const fs = require('fs');

main()

function main() {
    let allFiles = getAllFiles(__dirname);
    console.log(`文件数量:${allFiles.length}`);
    for (let i = 0; i < allFiles.length; i++) {
        console.log(allFiles[i]);
        // 同步读取文件内容
        let content = fs.readFileSync(filePath).toString();
        console.log(content);
	}
}

/**
 * 递归遍历，获取指定文件夹下面的所有文件路径
 */
function getAllFiles(filePath) {
    let allFilePaths = [];
    if (fs.existsSync(filePath)) {
        const files = fs.readdirSync(filePath);
        for (let i = 0; i < files.length; i++) {
            let file = files[i]; // 文件名称（不包含文件路径）
            let currentFilePath = filePath + '/' + file;
            let stats = fs.lstatSync(currentFilePath);
            if (stats.isDirectory()) {
                allFilePaths = allFilePaths.concat(getAllFiles(currentFilePath));
            } else {
               allFilePaths.push(currentFilePath);
            }
        }
    } else {
        console.warn(`指定的目录${filePath}不存在！`);
    }

    return allFilePaths;
}
