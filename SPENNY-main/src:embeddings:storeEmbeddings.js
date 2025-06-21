// src/embeddings/storeEmbeddings.js

import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import OpenAI from 'openai';

dotenv.config();  // Loads OPENAI_API_KEY from .env

export default async function storeEmbeddings() {
  const chunksDir     = 'doc-chunks';
  const embeddingsDir = 'embeddings';

  if (!fs.existsSync(chunksDir)) {
    throw new Error(`Document chunks folder not found: ${chunksDir}`);
  }
  if (!fs.existsSync(embeddingsDir)) {
    fs.mkdirSync(embeddingsDir);
  }

  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  });

  const files = fs.readdirSync(chunksDir).filter(f => f.endsWith('.txt'));
  for (const file of files) {
    const filePath = path.join(chunksDir, file);
    const content  = fs.readFileSync(filePath, 'utf8');

    console.log(`🔍 Generating embedding for ${file}`);
    const response = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: content,
    });
    const embeddingData = response.data[0];

    const outPath = path.join(embeddingsDir, `${file}.json`);
    fs.writeFileSync(outPath, JSON.stringify(embeddingData, null, 2));
    console.log(`✅ Saved embedding to ${outPath}`);
  }

  console.log('✅ storeEmbeddings complete.');
}
