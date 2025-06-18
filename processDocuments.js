// src/pipeline/processDocuments.js
import { promises as fs } from "fs";
import path from "path";
import { listFilesInFolder, downloadFileDirect } from "../helpers/dropboxHelper.js";
import { extractZip, processPDF, processImage, processWordDoc } from "../helpers/fileHelper.js";

// Dropbox folder and file settings
const dropboxFolderPath = "/DAYTRADING AI";           // Dropbox folder to list
const zipFilePath = "/DAYTRADING AI/DAYTRADING AI.zip"; // ZIP file path in Dropbox
const localZipPath = "./DAYTRADING_AI.zip";             // Where to save the ZIP locally
const extractFolder = "./extracted_content";            // Where to extract ZIP contents
const outputFolder = "./processed_content";             // Where to save processed text outputs

export async function runPipeline() {
  console.log("✅ Pipeline started!");
  try {
    // Ensure local directories exist
    await fs.mkdir(extractFolder, { recursive: true });
    await fs.mkdir(outputFolder, { recursive: true });

    console.log(`📂 Listing files in Dropbox folder: ${dropboxFolderPath}`);
    const entries = await listFilesInFolder(dropboxFolderPath);
    console.log(`Found ${entries.length} entries in Dropbox folder.`);

    console.log(`\n⬇️ Downloading file: ${zipFilePath}`);
    await downloadFileDirect(zipFilePath, localZipPath);

    console.log(`\n📂 Extracting ZIP file: ${localZipPath}`);
    await extractZip(localZipPath, extractFolder);

    console.log(`\n🔍 Processing extracted files in: ${extractFolder}`);
    await processFolder(extractFolder);

    console.log("✅ Pipeline completed successfully!");
  } catch (error) {
    console.error("❌ Error in pipeline:", error.message);
  }
}

// Recursively scan and process files within a folder in alphabetical order
async function processFolder(folderPath) {
  console.log(`🔎 Scanning folder: ${folderPath}`);
  let items = await fs.readdir(folderPath);
  items.sort((a, b) => a.localeCompare(b)); // sort alphabetically

  for (const item of items) {
    const fullPath = path.join(folderPath, item);
    const stats = await fs.lstat(fullPath);
    if (stats.isDirectory()) {
      await processFolder(fullPath);
    } else {
      const ext = path.extname(item).toLowerCase();
      if (ext === ".pdf") {
        await processPDF(fullPath, outputFolder);
      } else if ([".jpg", ".jpeg", ".png"].includes(ext)) {
        await processImage(fullPath, outputFolder);
      } else if (ext === ".docx") {
        await processWordDoc(fullPath, outputFolder);
      } else {
        console.log(`⚠️ Skipping unsupported file: ${item}`);
      }
    }
  }
}
