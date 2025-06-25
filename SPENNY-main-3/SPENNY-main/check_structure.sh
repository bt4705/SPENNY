#!/usr/bin/env bash

# List of all files/folders we expect to see in this pipeline project
declare -a EXPECTED=(
  "pipeline.js"
  "src/ingestion/downloadFolderAsZip.js"
  "src/ingestion/extractZip.js"
  "src/ocr/processFiles.js"
  "src/ocr/sendOCRFromFolder.js"
  "src/ocr/sendOCRToChatGPT.js"
  "src/parsing/processDocuments.js"
  "src/embeddings/storeEmbeddings.js"
  "src/agents/spennyAgent.js"
  "test-data/test.zip"
)

echo "🔍 Checking pipeline project structure…"
MISSING=0

for path in "${EXPECTED[@]}"; do
  if [ ! -e "$path" ]; then
    echo "❌ Missing: $path"
    MISSING=1
  else
    echo "✅ Found:   $path"
  fi
done

if [ $MISSING -eq 1 ]; then
  echo "→ Some files or folders are missing. Please create or move them."
  exit 1
else
  echo "🎉 All required files are present!"
  exit 0
fi
