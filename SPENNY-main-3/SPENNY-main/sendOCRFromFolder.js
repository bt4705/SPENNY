// sendOCRFromFolder.js
import fs from "fs";
import path from "path";
import { createWorker } from "tesseract.js";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

// Create an OpenAI client using the default export (v4)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Set the directory where your images are stored (adjust as needed)
const imagesDir = path.join(process.cwd(), "extracted_content");

// Function to perform OCR on a single image file
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

// Function to aggregate OCR text from all image files in the folder
async function extractTextFromFolder(dir) {
  const files = fs.readdirSync(dir);
  let allText = "";
  for (const file of files) {
    // Process image files with common extensions
    if (
      file.toLowerCase().endsWith(".jpg") ||
      file.toLowerCase().endsWith(".jpeg") ||
      file.toLowerCase().endsWith(".png")
    ) {
      const imagePath = path.join(dir, file);
      console.log(`Performing OCR on: ${file}`);
      const text = await performOCR(imagePath);
      allText += `\n-----\nExtracted from ${file}:\n${text}\n`;
    }
  }
  return allText;
}

// Function to send the aggregated text to ChatGPT
async function sendToChatGPT(prompt) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo", // Change this to "chatgpt-4o-latest" if you have access and want to use that
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt }
      ],
      temperature: 1,
      max_completion_tokens: 2048,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    });
    console.log("ChatGPT response:");
    console.log(response.choices[0].message.content);
  } catch (error) {
    console.error("Error calling OpenAI API:", error.response ? error.response.data : error.message);
  }
}

// Main function: Extract text from images and send it to ChatGPT
async function runOCRAndChat() {
  try {
    const extractedText = await extractTextFromFolder(imagesDir);
    console.log("Combined extracted text:");
    console.log(extractedText);
    await sendToChatGPT(extractedText);
  } catch (error) {
    console.error("Error during OCR and ChatGPT process:", error);
  }
}

runOCRAndChat();