// src/ocr/processFiles.js

import fs from 'fs';
import path from 'path';

export default async function processFiles() {
  const inputDir = 'extracted';
  const ocrDir   = 'ocr-files';

  if (!fs.existsSync(inputDir)) {
    throw new Error(`Input folder not found: ${inputDir}`);
  }

  if (fs.existsSync(ocrDir)) {
    fs.rmSync(ocrDir, { recursive: true, force: true });
  }
  fs.mkdirSync(ocrDir);

  const files = fs.readdirSync(inputDir);
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    if (['.png', '.jpg', '.jpeg', '.pdf'].includes(ext)) {
      const srcPath  = path.join(inputDir, file);
      const destPath = path.join(ocrDir, file);
      fs.copyFileSync(srcPath, destPath);
      console.log(`Copied ${file} → ${ocrDir}/`);
    }
  }

  console.log('✅ processFiles: OCR staging folder is ready.');
}
