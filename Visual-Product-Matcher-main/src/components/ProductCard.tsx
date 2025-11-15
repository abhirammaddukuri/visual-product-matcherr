import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  image: string;
  similarity?: number;
}

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  const getSimilarityColor = (score: number) => {
    if (score >= 90) return "bg-success text-success-foreground";
    if (score >= 75) return "bg-primary text-primary-foreground";
    if (score >= 60) return "bg-warning text-warning-foreground";
    return "bg-muted text-muted-foreground";
  };

  return (
    <Card className="group overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
      <div className="relative aspect-square overflow-hidden bg-muted">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
        />
        {product.similarity !== undefined && (
          <Badge 
            className={`absolute top-2 right-2 ${getSimilarityColor(product.similarity)}`}
          >
            {product.similarity}% match
          </Badge>
        )}
      </div>
      
      <div className="p-4 space-y-2">
        <div className="space-y-1">
          <h3 className="font-semibold text-foreground line-clamp-1">
            {product.name}
          </h3>
          <p className="text-sm text-muted-foreground">
            {product.category}
          </p>
        </div>
        
        <div className="flex items-center justify-between pt-2">
          <span className="text-lg font-bold text-primary">
            ${product.price}
          </span>
        </div>
      </div>
    </Card>
  );
};
