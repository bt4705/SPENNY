// downloadFolderAsZip.js
import axios from "axios";
import fs from "fs";
import dotenv from "dotenv";
dotenv.config();

const ACCESS_TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
if (!ACCESS_TOKEN) {
  console.error("Dropbox access token not set in .env");
  process.exit(1);
}

// Update this Dropbox path to where your folder is located.
// For example, if the folder is "DAYTRADING AI" in the root:
const DROPBOX_FOLDER_PATH = "/DAYTRADING AI";

async function downloadFolderAsZip() {
  try {
    console.log("Downloading folder as ZIP from path:", DROPBOX_FOLDER_PATH);
    const response = await axios({
      method: "post",
      url: "https://content.dropboxapi.com/2/files/download_zip",
      data: "", // send an empty string instead of null
      responseType: "arraybuffer",
      headers: {
        "Authorization": `Bearer ${ACCESS_TOKEN}`,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": JSON.stringify({ path: DROPBOX_FOLDER_PATH })
      }
    });
    
    fs.writeFileSync("folder.zip", response.data);
    console.log("Folder downloaded as folder.zip");
  } catch (error) {
    const errorMsg = error.response && error.response.data
      ? error.response.data.toString()
      : error.message;
    console.error("Error downloading folder:", errorMsg);
  }
}

downloadFolderAsZip();