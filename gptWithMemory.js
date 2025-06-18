// gptWithMemory.js
import fs from "fs";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

// Create an OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// File where memory (embeddings and texts) is stored
const memoryFile = "memory.json";

// Function to load memory from the JSON file
function loadMemory() {
  if (!fs.existsSync(memoryFile)) {
    console.error("Memory file not found! Run storeEmbeddings.js first.");
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(memoryFile, "utf8"));
}

// Send a prompt to ChatGPT that includes the stored memory as context
async function askGPTWithMemory(query) {
  const memory = loadMemory();
  // Create a combined text from memory entries
  const combinedMemoryText = memory
    .map((entry) => `From ${entry.file}:\n${entry.text}`)
    .join("\n\n");

  const prompt = `Based on the following historical market data and document text:\n\n${combinedMemoryText}\n\nAnswer the following query:\n\n${query}`;
  
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are an expert market analyst." },
        { role: "user", content: prompt },
      ],
      temperature: 0.7,
      max_completion_tokens: 300,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    });
    console.log("GPT Response:");
    console.log(response.choices[0].message.content);
  } catch (error) {
    console.error("Error calling GPT:", error.response ? error.response.data : error.message);
  }
}

// Define a sample query
const query = "What are some potential market entry signals based on the historical data?";
askGPTWithMemory(query);