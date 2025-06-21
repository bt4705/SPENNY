// listZipContents.js
import AdmZip from "adm-zip";

// Path to your downloaded ZIP file
const zipFilePath = "downloaded.zip";

// Create an AdmZip instance for the ZIP file
const zip = new AdmZip(zipFilePath);

// Get all entries (files and folders) inside the ZIP
const entries = zip.getEntries();

// Print out each entry's name
console.log("Entries in the ZIP file:");
entries.forEach((entry) => {
  console.log(entry.entryName);
});