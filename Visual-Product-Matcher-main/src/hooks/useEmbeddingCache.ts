import { useState, useEffect } from 'react';

interface CacheEntry {
  embedding: number[];
  timestamp: number;
}

const CACHE_DURATION = 60 * 60 * 1000; // 1 hour
const embeddingCache = new Map<string, CacheEntry>();

export const useEmbeddingCache = () => {
  const [cacheSize, setCacheSize] = useState(0);

  useEffect(() => {
    // Clean up expired cache entries periodically
    const interval = setInterval(() => {
      const now = Date.now();
      for (const [key, entry] of embeddingCache.entries()) {
        if (now - entry.timestamp > CACHE_DURATION) {
          embeddingCache.delete(key);
        }
      }
      setCacheSize(embeddingCache.size);
    }, 5 * 60 * 1000); // Check every 5 minutes

    return () => clearInterval(interval);
  }, []);

  const getCachedEmbedding = (imageUrl: string): number[] | null => {
    const cached = embeddingCache.get(imageUrl);
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      return cached.embedding;
    }
    return null;
  };

  const setCachedEmbedding = (imageUrl: string, embedding: number[]) => {
    embeddingCache.set(imageUrl, {
      embedding,
      timestamp: Date.now(),
    });
    setCacheSize(embeddingCache.size);
  };

  const clearCache = () => {
    embeddingCache.clear();
    setCacheSize(0);
  };

  return {
    getCachedEmbedding,
    setCachedEmbedding,
    clearCache,
    cacheSize,
  };
};
