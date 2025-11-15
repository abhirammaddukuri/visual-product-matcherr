import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";

interface SearchProgressProps {
  current: number;
  total: number;
  isSearching: boolean;
}

export const SearchProgress = ({ current, total, isSearching }: SearchProgressProps) => {
  if (!isSearching) return null;

  const progress = total > 0 ? (current / total) * 100 : 0;

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-card border border-border rounded-lg p-6 shadow-lg max-w-md w-full mx-4">
        <div className="flex items-center gap-3 mb-4">
          <Loader2 className="w-5 h-5 animate-spin text-primary" />
          <h3 className="text-lg font-semibold">Analyzing Images</h3>
        </div>
        <div className="space-y-2">
          <Progress value={progress} className="h-2" />
          <p className="text-sm text-muted-foreground text-center">
            Processing {current} of {total} products...
          </p>
        </div>
      </div>
    </div>
  );
};
