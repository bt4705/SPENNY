import downloadFolderAsZip from './src/ingestion/downloadFolderAsZip.js';
import extractZip           from './src/ingestion/extractZip.js';
import processFiles         from './src/ocr/processFiles.js';
import sendOCRFromFolder    from './src/ocr/sendOCRFromFolder.js';
import sendOCRToChatGPT     from './src/ocr/sendOCRToChatGPT.js';
import processDocuments     from './src/parsing/processDocuments.js';
import storeEmbeddings      from './src/embeddings/storeEmbeddings.js';

async function runPipeline() {
  try {
    console.log('1/6 Downloading ZIP…');
    await downloadFolderAsZip();

    console.log('2/6 Extracting ZIP…');
    await extractZip();

    console.log('3/6 OCR staging…');
    await processFiles();
    await sendOCRFromFolder();

    console.log('4/6 Sending OCR results to ChatGPT…');
    await sendOCRToChatGPT();

    console.log('5/6 Parsing documents…');
    await processDocuments();

    console.log('6/6 Generating & storing embeddings…');
    await storeEmbeddings();

    console.log('✅ Pipeline complete.');
  } catch (err) {
    console.error('❌ Pipeline error:', err);
    process.exit(1);
  }
}

runPipeline();
