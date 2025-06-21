// preprocessAndOCR.js
import fs from "fs";
import path from "path";
import sharp from "sharp";
import { createWorker } from "tesseract.js";
import dotenv from "dotenv";
import OpenAI from "openai"; // Use default import for OpenAI v4

dotenv.config();

// Initialize the OpenAI client using the default import
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Directory containing your images (update if needed)
const imagesDir = path.join(process.cwd(), "extracted_content");

// Preprocess an image (convert to grayscale and normalize for better OCR)
async function preprocessImage(inputPath, outputPath) {
  try {
    await sharp(inputPath)
      .grayscale()
      .normalize()
      .toFile(outputPath);
    console.log(`Preprocessed image saved as ${outputPath}`);
  } catch (error) {
    console.error(`Error preprocessing image ${inputPath}:`, error);
  }
}

// Perform OCR on a single image file using Tesseract.js
async function performOCR(imagePath) {
  const worker = createWorker({
    logger: (m) => console.log(`OCR progress for ${path.basename(imagePath)}:`, m),
  });
  await worker.load();
  await worker.loadLanguage("eng");
  await worker.initialize("eng");
  // Optionally set a page segmentation mode if needed:
  // await worker.setParameters({ tessedit_pageseg_mode: "6" });
  const { data: { text } } = await worker.recognize(imagePath);
  await worker.terminate();
  return text;
}

// Iterate through the folder, preprocess each image, and perform OCR
async function processImagesFromFolder(dir) {
  const files = fs.readdirSync(dir);
  let allText = "";
  for (const file of files) {
    // Process only images with common extensions
    if (
      file.toLowerCase().endsWith(".jpg") ||
      file.toLowerCase().endsWith(".jpeg") ||
      file.toLowerCase().endsWith(".png")
    ) {
      const originalPath = path.join(dir, file);
      const preprocessedPath = path.join(dir, `preprocessed_${file}`);
      
      console.log(`Preprocessing image: ${file}`);
      await preprocessImage(originalPath, preprocessedPath);
      
      console.log(`Performing OCR on: ${file}`);
      const text = await performOCR(preprocessedPath);
      allText += `\n-----\nExtracted from ${file}:\n${text}\n`;
      
      // Optionally, delete the preprocessed file:
      // fs.unlinkSync(preprocessedPath);
    }
  }
  return allText;
}

// Send the aggregated text to ChatGPT via the OpenAI API
async function sendToChatGPT(prompt) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo", // or "chatgpt-4o-latest" if you have access
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
    console.error(
      "Error calling OpenAI API:",
      error.response ? error.response.data : error.message
    );
  }
}

// Main function: Process images and send the extracted text to ChatGPT
async function run() {
  try {
    const extractedText = await processImagesFromFolder(imagesDir);
    console.log("Combined extracted text:");
    console.log(extractedText);
    await sendToChatGPT(extractedText);
  } catch (error) {
    console.error("Error during OCR and ChatGPT process:", error);
  }
}

run();