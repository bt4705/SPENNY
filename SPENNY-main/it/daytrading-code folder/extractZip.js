// extractZip.js
import AdmZip from "adm-zip";
import fs from "fs";

// Path to the downloaded ZIP file
const zipFilePath = "folder.zip";

// Folder where the ZIP contents will be extracted
const extractFolder = "extracted_content";

// Create the extraction folder if it doesn't exist
if (!fs.existsSync(extractFolder)) {
  fs.mkdirSync(extractFolder, { recursive: true });
}

const zip = new AdmZip(zipFilePath);
zip.extractAllTo(extractFolder, true);
console.log("Extracted contents to", extractFolder);