import { useState, useEffect, useMemo } from "react";
import { ImageUploader } from "@/components/ImageUploader";
import { ProductGrid } from "@/components/ProductGrid";
import { SimilarityFilter } from "@/components/SimilarityFilter";
import { CategoryFilter } from "@/components/CategoryFilter";
import { PriceFilter } from "@/components/PriceFilter";
import { SearchProgress } from "@/components/SearchProgress";
import { Button } from "@/components/ui/button";
import { Search, Sparkles, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { loadModel, calculateSimilarityScore } from "@/utils/imageSimilarity";
import { useEmbeddingCache } from "@/hooks/useEmbeddingCache";

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  image: string;
  similarity?: number;
}

const Index = () => {
  const [selectedImage, setSelectedImage] = useState<string>("");
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [minSimilarity, setMinSimilarity] = useState(40);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 1000]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchProgress, setSearchProgress] = useState(0);
  const [isModelLoading, setIsModelLoading] = useState(false);
  const [modelReady, setModelReady] = useState(false);
  const { toast } = useToast();
  const { getCachedEmbedding, setCachedEmbedding, cacheSize } = useEmbeddingCache();

  // Extract unique categories and price range from products
  const categories = useMemo(() => {
    const uniqueCategories = Array.from(new Set(products.map(p => p.category)));
    return uniqueCategories.sort();
  }, [products]);

  const productPriceRange = useMemo(() => {
    if (products.length === 0) return { min: 0, max: 1000 };
    const prices = products.map(p => p.price);
    return {
      min: Math.floor(Math.min(...prices)),
      max: Math.ceil(Math.max(...prices))
    };
  }, [products]);

  useEffect(() => {
    if (products.length > 0) {
      setPriceRange([productPriceRange.min, productPriceRange.max]);
    }
  }, [productPriceRange, products.length]);

  useEffect(() => {
    // Load products from JSON
    fetch("/data/products.json")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((error) => {
        console.error("Error loading products:", error);
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load products",
        });
      });

    // Pre-load CLIP vision model
    const initModel = async () => {
      setIsModelLoading(true);
      try {
        await loadModel();
        setModelReady(true);
        console.log("CLIP vision model ready for accurate matching");
      } catch (error) {
        console.error("Failed to initialize CLIP model:", error);
        toast({
          variant: "destructive",
          title: "Model Loading Failed",
          description: "Visual similarity features may not work properly",
        });
      } finally {
        setIsModelLoading(false);
      }
    };

    initModel();
  }, [toast]);

  const handleImageSelect = (imageUrl: string) => {
    setSelectedImage(imageUrl);
    setFilteredProducts([]);
  };

  const findSimilarProducts = async () => {
    if (!selectedImage || !modelReady) {
      toast({
        variant: "destructive",
        title: "Not Ready",
        description: modelReady ? "Please upload an image first" : "AI model is still loading...",
      });
      return;
    }
    
    setIsSearching(true);
    setSearchProgress(0);
    
    try {
      const cache = {
        get: getCachedEmbedding,
        set: setCachedEmbedding,
      };

      // Process products with progress tracking
      const productsWithSimilarity: Product[] = [];
      let successCount = 0;
      let failCount = 0;

      for (let i = 0; i < products.length; i++) {
        const product = products[i];
        setSearchProgress(i + 1);

        try {
          const similarity = await calculateSimilarityScore(
            selectedImage,
            product.image,
            cache
          );
          productsWithSimilarity.push({ ...product, similarity });
          successCount++;
        } catch (error) {
          failCount++;
          console.warn(`Failed to process ${product.name}:`, error);
          // Skip products that fail completely rather than adding fake scores
        }
      }
      
      // Sort by similarity (highest first)
      const sorted = productsWithSimilarity.sort((a, b) => 
        (b.similarity || 0) - (a.similarity || 0)
      );
      
      setFilteredProducts(sorted);
      
      toast({
        title: "Search Complete",
        description: `Successfully analyzed ${successCount} products${failCount > 0 ? ` (${failCount} failed)` : ''}. Using ${cacheSize} cached embeddings.`,
      });
    } catch (error) {
      console.error("Error during similarity search:", error);
      toast({
        variant: "destructive",
        title: "Search Failed",
        description: error instanceof Error ? error.message : "Failed to analyze image. Please try a different image.",
      });
    } finally {
      setIsSearching(false);
      setSearchProgress(0);
    }
  };

  const displayedProducts = filteredProducts.filter(
    (p) => {
      const meetsSimiliarity = (p.similarity || 0) >= minSimilarity;
      const meetsCategory = selectedCategory === "all" || p.category === selectedCategory;
      const meetsPrice = p.price >= priceRange[0] && p.price <= priceRange[1];
      return meetsSimiliarity && meetsCategory && meetsPrice;
    }
  );

  return (
    <div className="min-h-screen bg-gradient-subtle">
      <SearchProgress current={searchProgress} total={products.length} isSearching={isSearching} />
      
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col items-center text-center gap-2">
            <div className="flex items-center gap-2">
              <Sparkles className="w-7 h-7 text-primary" />
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                Visual Product Matcher
              </h1>
            </div>
            <p className="text-sm md:text-base text-muted-foreground max-w-2xl">
              Upload any image to instantly find visually similar products using advanced AI
            </p>
            <p className="text-xs text-muted-foreground">
              Powered by CLIP Vision Transformer • Real-time similarity matching
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-7xl mx-auto px-4 py-8 md:py-12">
        <div className="grid lg:grid-cols-[400px_1fr] gap-8 lg:gap-12">
          {/* Left Column - Upload & Preview */}
          <div className="space-y-6">
            <div className="lg:sticky lg:top-24">
              <ImageUploader onImageSelect={handleImageSelect} />
              
              {selectedImage && (
                <div className="mt-6 space-y-4">
                  <div className="rounded-lg overflow-hidden border border-border shadow-md">
                    <img
                      src={selectedImage}
                      alt="Selected"
                      className="w-full aspect-square object-cover"
                    />
                  </div>
                  
                  <Button
                    onClick={findSimilarProducts}
                    disabled={isSearching || !modelReady}
                    size="lg"
                    className="w-full bg-gradient-primary hover:opacity-90"
                  >
                    {isSearching ? (
                      <>
                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                        Analyzing Image...
                      </>
                    ) : (
                      <>
                        <Search className="w-5 h-5 mr-2" />
                        Find Similar Products
                      </>
                    )}
                  </Button>
                  
                  {isModelLoading && (
                    <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Loading AI model...
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {filteredProducts.length > 0 && (
              <>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <div>
                    <h2 className="text-2xl md:text-3xl font-bold text-foreground">
                      Similar Products
                    </h2>
                    <p className="text-sm text-muted-foreground mt-1">
                      Showing {displayedProducts.length} of {filteredProducts.length} results
                    </p>
                  </div>
                </div>

                <SimilarityFilter
                  value={minSimilarity}
                  onChange={setMinSimilarity}
                />

                <CategoryFilter
                  categories={categories}
                  selectedCategory={selectedCategory}
                  onCategoryChange={setSelectedCategory}
                />

                <PriceFilter
                  minPrice={productPriceRange.min}
                  maxPrice={productPriceRange.max}
                  value={priceRange}
                  onChange={setPriceRange}
                />

                <ProductGrid products={displayedProducts} />
              </>
            )}

            {!selectedImage && filteredProducts.length === 0 && (
              <div className="flex items-center justify-center min-h-[400px]">
                <div className="text-center py-12 px-4 max-w-2xl">
                  <div className="inline-block p-6 rounded-full bg-primary/10 mb-6 animate-fade-in">
                    <Search className="w-16 h-16 text-primary" />
                  </div>
                  <h3 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
                    ML-Powered Visual Search
                  </h3>
                  <p className="text-muted-foreground text-base md:text-lg mb-4 leading-relaxed">
                    Upload any product image and our AI will instantly analyze it using advanced computer vision to find visually similar items from our catalog.
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Powered by CLIP Vision Transformer for accurate image understanding
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
