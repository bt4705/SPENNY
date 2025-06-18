// storeEmbeddings.js
import fs from "fs";
import path from "path";
import { createWorker } from "tesseract.js";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

// Create an OpenAI client (using the default export from openai v4)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Directory containing your images
const imagesDir = path.join(process.cwd(), "extracted_content");
// File to store the memory (embeddings)
const memoryFile = "memory.json";

// Function to perform OCR on one image file
async function performOCR(imagePath) {
  const worker = createWorker({
    logger: (m) => console.log(`OCR progress for ${path.basename(imagePath)}:`, m),
  });
  await worker.load();
  await worker.loadLanguage("eng");
  await worker.initialize("eng");
  const { data: { text } } = await worker.recognize(imagePath);
  await worker.terminate();
  return text;
}

// Function to generate embedding for a given text
async function getEmbedding(text) {
  try {
    const response = await openai.embeddings.create({
      model: "text-embedding-ada-002",
      input: text,
    });
    return response.data.data[0].embedding;
  } catch (error) {
    console.error("Error generating embedding:", error.response ? error.response.data : error.message);
    return null;
  }
}

// Process all images in the folder and store the extracted text and embeddings
async function processImages() {
  const files = fs.readdirSync(imagesDir);
  const memory = [];
  for (const file of files) {
    if (
      file.toLowerCase().endsWith(".jpg") ||
      file.toLowerCase().endsWith(".jpeg") ||
      file.toLowerCase().endsWith(".png")
    ) {
      const imagePath = path.join(imagesDir, file);
      console.log(`Processing image: ${file}`);
      const text = await performOCR(imagePath);
      console.log(`Extracted text from ${file}:`, text);
      if (text && text.trim().length > 0) {
        const embedding = await getEmbedding(text);
        memory.push({
          file: file,
          text: text,
          embedding: embedding,
        });
      }
    }
  }
  fs.writeFileSync(memoryFile, JSON.stringify(memory, null, 2));
  console.log("Memory saved to", memoryFile);
}

processImages();