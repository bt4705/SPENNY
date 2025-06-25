// testDownload.js
import axios from "axios";
import fs from "fs";
import dotenv from "dotenv";
dotenv.config();

const ACCESS_TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
if (!ACCESS_TOKEN) {
  console.error("Dropbox access token not set in .env");
  process.exit(1);
}

// Example: If you have a ZIP file in the root of your Dropbox named "DAYTRADING AI.zip"
// or in a folder "pipeline/DAYTRADING AI.zip", adjust this path accordingly.
const DROPBOX_PATH = "/pipeline/DAYTRADING AI.zip";

async function downloadFile() {
  try {
    console.log("Starting direct download for file:", DROPBOX_PATH);
    const response = await axios.post(
      "https://content.dropboxapi.com/2/files/download",
      null,
      {
        responseType: "arraybuffer",
        headers: {
          "Authorization": `Bearer ${ACCESS_TOKEN}`,
          "Content-Type": "application/octet-stream",
          "Dropbox-API-Arg": JSON.stringify({ path: DROPBOX_PATH })
        }
      }
    );
    
    console.log("File downloaded successfully. Response size:", response.data.byteLength, "bytes");
    fs.writeFileSync("downloaded.zip", response.data);
    console.log("File saved as downloaded.zip");
  } catch (error) {
    const errorMsg = error.response && error.response.data
      ? error.response.data.toString()
      : error.message;
    console.error("Error downloading file:", errorMsg);
  }
}

downloadFile();