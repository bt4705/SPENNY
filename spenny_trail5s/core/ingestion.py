import os
import logging
import pdfplumber
import docx
from PIL import Image
import pytesseract
import dropbox
from config.secrets import DROPBOX_ACCESS_TOKEN, DROPBOX_REMOTE_PATH

logger = logging.getLogger(__name__)

def download_dropbox_folder(dbx, remote_folder, local_folder):
    try:
        res = dbx.files_list_folder(remote_folder)
        for entry in res.entries:
            remote_path = entry.path_lower
            local_path = os.path.join(local_folder, os.path.basename(entry.path_lower))
            if isinstance(entry, dropbox.files.FileMetadata):
                dbx.files_download_to_file(local_path, remote_path)
            elif isinstance(entry, dropbox.files.FolderMetadata):
                sub_local = os.path.join(local_folder, entry.name)
                os.makedirs(sub_local, exist_ok=True)
                download_dropbox_folder(dbx, remote_path, sub_local)
    except Exception as e:
        logger.error(f"Dropbox download error: {e}")

def ingest_directory(input_dir: str, output_dir: str):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            filepath = os.path.join(root, file)
            rel_dir = os.path.relpath(root, input_dir)
            out_subdir = os.path.join(output_dir, rel_dir)
            os.makedirs(out_subdir, exist_ok=True)
            base, ext = os.path.splitext(file)
            txt_out = os.path.join(out_subdir, base + '.txt')
            try:
                if ext.lower() == '.pdf':
                    text = ''
                    with pdfplumber.open(filepath) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text() or ''
                            text += page_text + '\n'
                elif ext.lower() in ('.docx', '.doc'):
                    doc = docx.Document(filepath)
                    text = '\n'.join([para.text for para in doc.paragraphs])
                elif ext.lower() in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff'):
                    img = Image.open(filepath)
                    text = pytesseract.image_to_string(img)
                else:
                    logger.info(f'Skipping unsupported file: {filepath}')
                    continue
                with open(txt_out, 'w', encoding='utf-8') as fout:
                    fout.write(text)
                logger.info(f'Ingested {filepath} to {txt_out}')
            except Exception as e:
                logger.error(f'Failed to ingest {filepath}: {e}')

def ingest_all_strategies():
    # Setup Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    # Download remote folder
    if DROPBOX_REMOTE_PATH:
        download_dropbox_folder(dbx, DROPBOX_REMOTE_PATH, "data/strategy")
    # Ingest local strategy files
    ingest_directory("data/strategy", "data/ingested_text")
