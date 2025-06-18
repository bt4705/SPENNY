// sendToChatGPT.js
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function sendToChatGPT(prompt) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo", // Change to "chatgpt-4o-latest" or "gpt-4-32k" if available and needed
      messages: [
        { role: "system", content: "You are a financial market analyst." },
        { role: "user", content: prompt }
      ],
      temperature: 1,
      max_completion_tokens: 2048,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    });
    const output = response.choices[0].message.content;
    console.log("ChatGPT response:");
    console.log(output);
    return output;
  } catch (error) {
    console.error(
      "Error calling OpenAI API:",
      error.response ? error.response.data : error.message
    );
    return null;
  }
}

export default sendToChatGPT;
