import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Editor from "@monaco-editor/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ArrowLeft, Play, Send, RotateCcw, Loader2 } from "lucide-react";
import { getExercise, submitSolution, getApiErrorMessage } from "../api/client";
import { useTheme } from "../context/ThemeContext";
import { useToast } from "../context/ToastContext";
import { Button } from "../components/ui/Button";
import { DifficultyBadge, TopicBadge } from "../components/ui/Badge";
import { HintPanel } from "../components/HintPanel";
import { ResultsPanel } from "../components/ResultsPanel";
import type { ExerciseDetail, SubmitResponse } from "../types";

export function ExerciseWorkspace() {
  const { id } = useParams<{ id: string }>();
  const { theme } = useTheme();
  const { showToast } = useToast();

  const [exercise, setExercise] = useState<ExerciseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [code, setCode] = useState("");
  const [result, setResult] = useState<SubmitResponse | null>(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    setLoading(true);
    setLoadError(null);
    getExercise(id)
      .then((data) => {
        if (cancelled) return;
        setExercise(data);
        setCode(data.starter_code);
        setResult(null);
      })
      .catch(() => {
        if (!cancelled) setLoadError("Couldn't load this exercise. Is the backend running?");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  const run = async (mode: "run" | "submit") => {
    if (!id) return;
    if (mode === "run") {
      setRunning(true);
    } else {
      setSubmitting(true);
    }
    try {
      const res = await submitSolution(id, code, mode);
      setResult(res);
      if (mode === "submit" && res.passed) {
        showToast(res.newly_solved ? "Nice work — exercise solved!" : "Passed again!", "success");
      } else if (!res.passed) {
        showToast("Not quite — check the results below.", "info");
      }
    } catch (err) {
      showToast(getApiErrorMessage(err, "Something went wrong while grading."), "error");
    } finally {
      setRunning(false);
      setSubmitting(false);
    }
  };

  const resetCode = () => {
    if (exercise) setCode(exercise.starter_code);
  };

  if (loading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-brand-500" />
      </div>
    );
  }

  if (loadError || !exercise) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-16 text-center">
        <p className="text-slate-600 dark:text-slate-400">{loadError ?? "Exercise not found."}</p>
        <Link to="/exercises" className="mt-4 inline-block text-brand-600 hover:underline dark:text-brand-400">
          Back to exercises
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
      <Link
        to="/exercises"
        className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
      >
        <ArrowLeft className="h-3.5 w-3.5" /> All exercises
      </Link>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Left: prompt + hints */}
        <div className="flex flex-col gap-4">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <TopicBadge topic={exercise.topic} />
              <DifficultyBadge difficulty={exercise.difficulty} />
            </div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">{exercise.title}</h1>
          </div>
          <div className="prose prose-sm prose-slate max-w-none rounded-xl border border-slate-200 bg-white p-5 dark:prose-invert dark:border-slate-800 dark:bg-surface-dark-subtle">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{exercise.description}</ReactMarkdown>
          </div>
          <HintPanel exerciseId={exercise.id} hintCount={exercise.hint_count} />
        </div>

        {/* Right: editor + results */}
        <div className="flex flex-col gap-4">
          <div className="overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800">
            <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-3 py-2 dark:border-slate-800 dark:bg-slate-900/60">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">solution.py</span>
              <button
                onClick={resetCode}
                aria-label="Reset to starter code"
                className="flex items-center gap-1 text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
              >
                <RotateCcw className="h-3 w-3" /> Reset
              </button>
            </div>
            <Editor
              height="360px"
              language="python"
              theme={theme === "dark" ? "vs-dark" : "light"}
              value={code}
              onChange={(v) => setCode(v ?? "")}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
              }}
            />
          </div>

          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => run("run")} loading={running} disabled={submitting}>
              <Play className="h-4 w-4" /> Run
            </Button>
            <Button variant="primary" onClick={() => run("submit")} loading={submitting} disabled={running}>
              <Send className="h-4 w-4" /> Submit
            </Button>
          </div>

          <div className="min-h-[200px] flex-1 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800">
            <ResultsPanel result={result} />
          </div>
        </div>
      </div>
    </div>
  );
}
