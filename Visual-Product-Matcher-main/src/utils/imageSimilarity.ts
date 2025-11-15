import { AutoProcessor, CLIPVisionModelWithProjection, RawImage } from "@huggingface/transformers";

let imageProcessor: any = null;
let visionModel: any = null;

const MODEL_NAME = "Xenova/clip-vit-base-patch32";

export const loadModel = async () => {
  if (imageProcessor && visionModel) return { imageProcessor, visionModel };
  
  console.log("Loading CLIP vision model for accurate visual similarity...");
  
  try {
    // Load processor and model separately for better control
    imageProcessor = await AutoProcessor.from_pretrained(MODEL_NAME);
    visionModel = await CLIPVisionModelWithProjection.from_pretrained(MODEL_NAME, {
      device: "webgpu", // Use WebGPU for better performance if available
    });
    
    console.log("CLIP model loaded successfully (WebGPU)");
    return { imageProcessor, visionModel };
  } catch (error) {
    console.warn("WebGPU not available, falling back to CPU");
    // Fallback to CPU if WebGPU fails
    imageProcessor = await AutoProcessor.from_pretrained(MODEL_NAME);
    visionModel = await CLIPVisionModelWithProjection.from_pretrained(MODEL_NAME);
    
    console.log("CLIP model loaded successfully (CPU mode)");
    return { imageProcessor, visionModel };
  }
};

export const getImageEmbedding = async (imageUrl: string, cache?: {
  get: (url: string) => number[] | null;
  set: (url: string, embedding: number[]) => void;
}) => {
  // Check cache first
  if (cache) {
    const cached = cache.get(imageUrl);
    if (cached) {
      console.log("Using cached embedding for:", imageUrl);
      return cached;
    }
  }

  if (!imageProcessor || !visionModel) {
    await loadModel();
  }

  try {
    // Load image using RawImage from transformers.js
    const image = await RawImage.fromURL(imageUrl);
    
    // Preprocess image
    const inputs = await imageProcessor(image);
    
    // Get image embeddings
    const { image_embeds } = await visionModel(inputs);
    
    // Return the embedding as a regular array for easier computation
    const embedding = Array.from(image_embeds.data) as number[];
    
    // Cache the result
    if (cache) {
      cache.set(imageUrl, embedding);
    }
    
    return embedding;
  } catch (error) {
    console.error("Error extracting embedding:", error);
    throw error;
  }
};

export const computeCosineSimilarity = (embedding1: number[], embedding2: number[]): number => {
  if (embedding1.length !== embedding2.length) {
    throw new Error("Embeddings must have the same length");
  }
  
  // Compute dot product
  let dotProduct = 0;
  let magnitude1 = 0;
  let magnitude2 = 0;
  
  for (let i = 0; i < embedding1.length; i++) {
    dotProduct += embedding1[i] * embedding2[i];
    magnitude1 += embedding1[i] * embedding1[i];
    magnitude2 += embedding2[i] * embedding2[i];
  }
  
  magnitude1 = Math.sqrt(magnitude1);
  magnitude2 = Math.sqrt(magnitude2);
  
  // Compute cosine similarity
  const similarity = dotProduct / (magnitude1 * magnitude2);
  
  // Convert to percentage (0-100)
  // CLIP embeddings are already normalized, so similarity is between -1 and 1
  return Math.round(((similarity + 1) / 2) * 100);
};

export const calculateSimilarityScore = async (
  uploadedImageUrl: string,
  productImageUrl: string,
  cache?: {
    get: (url: string) => number[] | null;
    set: (url: string, embedding: number[]) => void;
  }
): Promise<number> => {
  try {
    const [embedding1, embedding2] = await Promise.all([
      getImageEmbedding(uploadedImageUrl, cache),
      getImageEmbedding(productImageUrl, cache),
    ]);

    const similarity = computeCosineSimilarity(embedding1, embedding2);
    
    return similarity;
  } catch (error) {
    console.error("Error calculating similarity:", error);
    throw error;
  }
};
