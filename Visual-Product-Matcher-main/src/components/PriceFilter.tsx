import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";

interface PriceFilterProps {
  minPrice: number;
  maxPrice: number;
  value: [number, number];
  onChange: (value: [number, number]) => void;
}

export const PriceFilter = ({ minPrice, maxPrice, value, onChange }: PriceFilterProps) => {
  return (
    <div className="space-y-4 p-4 border border-border rounded-lg bg-card">
      <div className="flex items-center justify-between">
        <Label className="text-sm font-medium">Price Range</Label>
        <span className="text-sm text-muted-foreground">
          ${value[0]} - ${value[1]}
        </span>
      </div>
      <Slider
        min={minPrice}
        max={maxPrice}
        step={10}
        value={value}
        onValueChange={onChange}
        className="w-full"
      />
    </div>
  );
};
