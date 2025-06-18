// src/parsing/processDocuments.js

import fs from 'fs';
import path from 'path';

export default async function processDocuments() {
  const responsesDir = 'gpt-responses';
  const chunksDir    = 'doc-chunks';

  if (!fs.existsSync(responsesDir)) {
    throw new Error(`ChatGPT responses folder not found: ${responsesDir}`);
  }
  if (fs.existsSync(chunksDir)) {
    fs.rmSync(chunksDir, { recursive: true, force: true });
  }
  fs.mkdirSync(chunksDir);

  const files = fs.readdirSync(responsesDir).filter(f => f.endsWith('.json'));
  for (const file of files) {
    const data = JSON.parse(fs.readFileSync(path.join(responsesDir, file), 'utf8'));
    const reply = data.choices?.[0]?.message?.content || '';
    const paragraphs = reply.split(/\n{2,}/g);
    paragraphs.forEach((para, idx) => {
      const chunkName = `${path.basename(file, '.json')}_chunk${idx+1}.txt`;
      const outPath   = path.join(chunksDir, chunkName);
      fs.writeFileSync(outPath, para.trim());
      console.log(`✅ Wrote chunk ${idx + 1} → ${chunkName}`);
    });
  }

  console.log('✅ processDocuments complete.');
}
