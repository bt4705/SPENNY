// src/ingestion/downloadFolderAsZip.js

import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import fetch from 'node-fetch';
import { Dropbox } from 'dropbox';

dotenv.config();  // Load DROPBOX_ACCESS_TOKEN from .env

export default async function downloadFolderAsZip() {
  const TOKEN = process.env.DROPBOX_ACCESS_TOKEN;
  if (!TOKEN) {
    throw new Error('Missing DROPBOX_ACCESS_TOKEN in .env');
  }

  // Initialize the Dropbox SDK
  const dbx = new Dropbox({ accessToken: TOKEN, fetch });

  // === UPDATE BELOW: Because your ZIPs live under two nested "DAYTRADING AI" folders ===
  const dropboxFolder = '/DAYTRADING AI/DAYTRADING AI';
  const zipFiles = [
    `Spenny’s trading course copy.zip`,
    `GENERAL GRAPHS.zip`
  ];
  // ======================================================================================

  // Create (or recreate) a local folder to store downloaded ZIPs
  const localDownloadDir = 'downloaded_zips';
  if (fs.existsSync(localDownloadDir)) {
    fs.rmSync(localDownloadDir, { recursive: true, force: true });
  }
  fs.mkdirSync(localDownloadDir);

  // Loop through each ZIP filename and download it
  for (const fileName of zipFiles) {
    // Build the full Dropbox path, e.g. "/DAYTRADING AI/DAYTRADING AI/Spenny’s trading course copy.zip"
    const dropboxPath = `${dropboxFolder}/${fileName}`;

    console.log(`🔽 Downloading "${dropboxPath}" from Dropbox…`);
    try {
      // filesDownload expects an object with { path: '<full path>' }
      const response = await dbx.filesDownload({ path: dropboxPath });

      // The downloaded file’s binary is under response.result.fileBinary
      const fileBinary = response.result.fileBinary;

      // Save it locally under downloaded_zips/<filename>
      const outPath = path.join(localDownloadDir, fileName);
      fs.writeFileSync(outPath, fileBinary, 'binary');
      console.log(`✅ Saved Dropbox file to ${outPath}`);
    } catch (err) {
      console.error(`❌ Failed to download "${fileName}":`, err.error_summary || err);
      throw err;
    }
  }

  console.log('✅ downloadFolderAsZip: all ZIPs downloaded successfully.\n');
}

