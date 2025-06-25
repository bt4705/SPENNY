// sendOCRFromFolder.js
import fs from "fs";
import path from "path";
import { createWorker } from "tesseract.js";
import dotenv from "dotenv";
import { Configuration, OpenAIApi } from "openai";

dotenv.config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY) {
  console.error("OpenAI API key not set in .env");
  process.exit(1);
}

// Set up the OpenAI client.
const configuration = new Configuration({
  apiKey: OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Directory containing your images
const imagesDir = path.join(process.cwd(), "images");

// Function to perform OCR on a single image file.
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

// Function to iterate through the images folder and aggregate text.
async function extractTextFromFolder(dir) {
  const files = fs.readdirSync(dir);
  let allText = "";
  for (const file of files) {
    // Process common image file types (adjust as needed)
    if (file.toLowerCase().endsWith(".jpg") || file.toLowerCase().endsWith(".jpeg") || file.toLowerCase().endsWith(".png")) {
      const imagePath = path.join(dir, file);
      console.log(`Processing image: ${file}`);
      const text = await performOCR(imagePath);
      allText += `\n-----\nExtracted from ${file}:\n${text}\n`;
    }
  }
  return allText;
}

// Function to send a prompt to ChatGPT.
async function askChatGPT(prompt) {
  try {
    const response = await openai.createChatCompletion({
      model: "gpt-3.5-turbo",  // You can change to another model if needed.
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt },
      ],
    });
    console.log("ChatGPT response:");
    console.log(response.data.choices[0].message.content);
  } catch (error) {
    console.error("Error calling OpenAI API:", error.response ? error.response.data : error.message);
  }
}

// Main function: extract text from all images and send it to ChatGPT.
async function runOCRAndChat() {
  try {
    const extractedText = await extractTextFromFolder(imagesDir);
    console.log("Combined extracted text:");
    console.log(extractedText);
    await askChatGPT(extractedText);
  } catch (error) {
    console.error("Error during OCR and Chat:", error);
  }
}

runOCRAndChat();