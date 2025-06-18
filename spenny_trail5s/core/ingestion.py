# core/ingestion.py

import os
import logging
import pdfplumber
import docx
from PIL import Image
import pytesseract
import dropbox
from config.secrets import DROPBOX_ACCESS_TOKEN, DROPBOX_REMOTE_FOLDERS

logger = logging.getLogger(__name__)

def download_dropbox_folder(dbx, remote_folder: str, local_folder: str):
    """
    Recursively download all files and subfolders from a Dropbox path
    into a local directory.
    """
    try:
        res = dbx.files_list_folder(remote_folder)
        for entry in res.entries:
            remote_path = entry.path_lower
            local_path = os.path.join(local_folder, entry.name)
            if isinstance(entry, dropbox.files.FileMetadata):
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                dbx.files_download_to_file(local_path, remote_path)
            elif isinstance(entry, dropbox.files.FolderMetadata):
                os.makedirs(local_path, exist_ok=True)
                download_dropbox_folder(dbx, remote_path, local_path)
    except Exception as e:
        logger.error(f"Dropbox download error for {remote_folder}: {e}")

def ingest_directory(input_dir: str, output_dir: str):
    """
    Walk through input_dir, OCR/PDF/docx-extract each file,
    and write its plain text to a parallel structure under output_dir.
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            filepath = os.path.join(root, file)
            rel_dir = os.path.relpath(root, input_dir)
            out_subdir = os.path.join(output_dir, rel_dir)
            os.makedirs(out_subdir, exist_ok=True)
            base, ext = os.path.splitext(file)
            txt_out = os.path.join(out_subdir, base + ".txt")
            try:
                if ext.lower() == ".pdf":
                    text = ""
                    with pdfplumber.open(filepath) as pdf:
                        for page in pdf.pages:
                            pg = page.extract_text()
                            if pg:
                                text += pg + "\n"
                elif ext.lower() in (".docx", ".doc"):
                    doc = docx.Document(filepath)
                    text = "\n".join([p.text for p in doc.paragraphs])
                elif ext.lower() in (".png", ".jpg", ".jpeg", ".bmp", ".tiff"):
                    img = Image.open(filepath)
                    text = pytesseract.image_to_string(img)
                else:
                    logger.info(f"Skipping unsupported file type: {filepath}")
                    continue

                with open(txt_out, "w", encoding="utf-8") as fout:
                    fout.write(text)
                logger.info(f"Ingested {filepath} → {txt_out}")
            except Exception as e:
                logger.error(f"Failed to ingest {filepath}: {e}")

def ingest_all_strategies():
    """
    1) Download each Dropbox folder into data/strategy/<folder_name>
    2) OCR/extract every file into data/ingested_text/
    """
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    # 1) download each configured remote path
    for remote in DROPBOX_REMOTE_FOLDERS:
        folder_name = os.path.basename(remote)
        local_folder = os.path.join("data/strategy", folder_name)
        os.makedirs(local_folder, exist_ok=True)
        download_dropbox_folder(dbx, remote, local_folder)

    # 2) ingest all downloaded strategy files
    ingest_directory("data/strategy", "data/ingested_text")
