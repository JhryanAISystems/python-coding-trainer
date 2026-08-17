import { useEffect, useState } from "react";
import { listExercises } from "../api/client";
import type { ExerciseListResponse } from "../types";

export function useExercises(topic?: string, difficulty?: string) {
  const [data, setData] = useState<ExerciseListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    listExercises({ topic, difficulty })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch(() => {
        if (!cancelled) setError("Couldn't load exercises. Is the backend running?");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [topic, difficulty, refreshKey]);

  return { data, loading, error, refresh: () => setRefreshKey((k) => k + 1) };
}
