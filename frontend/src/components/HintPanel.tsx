import { useState } from "react";
import { Lightbulb, Loader2 } from "lucide-react";
import { Button } from "./ui/Button";
import { getHint } from "../api/client";

export function HintPanel({ exerciseId, hintCount }: { exerciseId: string; hintCount: number }) {
  const [revealed, setRevealed] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  if (hintCount === 0) return null;

  const nextIndex = revealed.length;
  const canRevealMore = nextIndex < hintCount;

  const revealNext = async () => {
    setLoading(true);
    try {
      const res = await getHint(exerciseId, nextIndex);
      setRevealed((prev) => [...prev, res.hint]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50/60 p-4 dark:border-amber-900/50 dark:bg-amber-950/20">
      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-amber-800 dark:text-amber-300">
        <Lightbulb className="h-4 w-4" />
        Hints ({revealed.length}/{hintCount})
      </div>
      {revealed.length > 0 && (
        <ol className="mb-3 list-decimal space-y-1.5 pl-5 text-sm text-amber-900 dark:text-amber-200">
          {revealed.map((h, i) => (
            <li key={i}>{h}</li>
          ))}
        </ol>
      )}
      {canRevealMore && (
        <Button variant="secondary" size="sm" onClick={revealNext} disabled={loading}>
          {loading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : null}
          {revealed.length === 0 ? "Show a hint" : "Show next hint"}
        </Button>
      )}
    </div>
  );
}
