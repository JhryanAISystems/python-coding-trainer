import { useMemo, useState } from "react";
import { SearchX } from "lucide-react";
import { useExercises } from "../hooks/useExercises";
import { ExerciseCard } from "../components/ExerciseCard";
import { ExerciseCardSkeleton } from "../components/ui/Skeleton";
import { formatTopicLabel } from "../lib/format";
import type { Difficulty } from "../types";

const DIFFICULTIES: Difficulty[] = ["beginner", "intermediate", "advanced"];

export function Exercises() {
  const [topic, setTopic] = useState<string>("");
  const [difficulty, setDifficulty] = useState<string>("");
  const { data, loading, error } = useExercises(topic || undefined, difficulty || undefined);

  const topics = useMemo(() => data?.topics ?? [], [data]);

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Exercises</h1>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Browse by topic and difficulty, or just pick one and start coding.
        </p>
      </div>

      <div className="mb-6 flex flex-wrap gap-3">
        <select
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          aria-label="Filter by topic"
          className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-slate-700 dark:bg-surface-dark-subtle dark:text-slate-200"
        >
          <option value="">All topics</option>
          {topics.map((t) => (
            <option key={t} value={t}>
              {formatTopicLabel(t)}
            </option>
          ))}
        </select>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          aria-label="Filter by difficulty"
          className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-slate-700 dark:bg-surface-dark-subtle dark:text-slate-200"
        >
          <option value="">All difficulties</option>
          {DIFFICULTIES.map((d) => (
            <option key={d} value={d} className="capitalize">
              {d}
            </option>
          ))}
        </select>
        {(topic || difficulty) && (
          <button
            onClick={() => {
              setTopic("");
              setDifficulty("");
            }}
            className="text-sm font-medium text-brand-600 hover:underline dark:text-brand-400"
          >
            Clear filters
          </button>
        )}
      </div>

      {error && (
        <div className="rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300">
          {error}
        </div>
      )}

      {loading && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <ExerciseCardSkeleton key={i} />
          ))}
        </div>
      )}

      {!loading && !error && data && data.exercises.length === 0 && (
        <div className="flex flex-col items-center gap-2 rounded-xl border border-dashed border-slate-300 py-16 text-center text-slate-400 dark:border-slate-700">
          <SearchX className="h-8 w-8" />
          <p className="text-sm">No exercises match those filters.</p>
        </div>
      )}

      {!loading && !error && data && data.exercises.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.exercises.map((ex) => (
            <ExerciseCard key={ex.id} exercise={ex} />
          ))}
        </div>
      )}
    </div>
  );
}
