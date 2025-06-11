
import { GoogleGenAI, GenerateContentResponse } from "@google/genai";

// Assume process.env.API_KEY is available in the execution environment
// DO NOT add UI for API key input.
const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  console.warn("Gemini API key not found in process.env.API_KEY. Gemini features will be disabled.");
}

const ai = API_KEY ? new GoogleGenAI({ apiKey: API_KEY }) : null;

const TEXT_MODEL = 'gemini-2.5-flash-preview-04-17';
// const IMAGE_MODEL = 'imagen-3.0-generate-002'; // For future use if image generation is needed

export const generateTextSummary = async (textToSummarize: string): Promise<string> => {
  if (!ai) {
    return "Gemini API key not configured. Summary generation disabled.";
  }
  if (!textToSummarize.trim()) {
    return "No text provided for summary.";
  }

  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: TEXT_MODEL,
      contents: `Please summarize the following text concisely:\n\n${textToSummarize}`,
      // config: {
      //   temperature: 0.7,
      //   topK: 1,
      //   topP: 1,
      //   maxOutputTokens: 256,
      // }
    });
    
    return response.text;
  } catch (error) {
    console.error("Error generating summary with Gemini API:", error);
    if (error instanceof Error) {
      return `Error generating summary: ${error.message}`;
    }
    return "An unknown error occurred while generating the summary.";
  }
};

// Placeholder for more complex AI agent interactions for crawler management
export const assistCrawlerCreation = async (prompt: string): Promise<string> => {
  if (!ai) {
    return "Gemini API key not configured. AI assistance disabled.";
  }
  try {
    const response: GenerateContentResponse = await ai.models.generateContent({
      model: TEXT_MODEL,
      contents: prompt, // e.g., "Generate a YAML config for a web crawler for news articles on site X about topic Y"
    });
    return response.text;
  } catch (error) {
    console.error("Error with AI crawler assistance:", error);
     if (error instanceof Error) {
      return `Error assisting crawler creation: ${error.message}`;
    }
    return "An unknown error occurred during AI assistance for crawler creation.";
  }
};
