import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";

interface SimilarityFilterProps {
  value: number;
  onChange: (value: number) => void;
}

export const SimilarityFilter = ({ value, onChange }: SimilarityFilterProps) => {
  return (
    <div className="space-y-4 p-4 rounded-lg bg-card border border-border">
      <div className="flex items-center justify-between">
        <Label className="text-sm font-medium">
          Minimum Similarity
        </Label>
        <span className="text-sm font-bold text-primary">
          {value}%
        </span>
      </div>
      
      <Slider
        value={[value]}
        onValueChange={([newValue]) => onChange(newValue)}
        min={0}
        max={100}
        step={5}
        className="w-full"
      />
      
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </div>
  );
};
