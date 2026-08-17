import { CheckCircle2, XCircle, PartyPopper, Clock } from "lucide-react";
import clsx from "clsx";
import type { SubmitResponse } from "../types";

export function ResultsPanel({ result }: { result: SubmitResponse | null }) {
  if (!result) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-2 p-8 text-center text-slate-400 dark:text-slate-500">
        <Clock className="h-8 w-8" />
        <p className="text-sm">Run your code to see results here.</p>
      </div>
    );
  }

  if (result.error) {
    return (
      <div className="p-4">
        <div className="mb-3 flex items-center gap-2 rounded-lg bg-rose-50 px-3 py-2 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300">
          <XCircle className="h-4 w-4 shrink-0" />
          <span className="text-sm font-medium">Couldn't run your code</span>
        </div>
        <pre className="overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs text-slate-100">{result.error}</pre>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div
        className={clsx(
          "flex items-center gap-2 px-4 py-3 text-sm font-semibold",
          result.passed
            ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300"
            : "bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300",
        )}
      >
        {result.passed ? (
          <span className="animate-success-pop flex items-center gap-2">
            <PartyPopper className="h-4 w-4" />
            All {result.total_tests} tests passed{result.newly_solved ? " — exercise solved!" : "!"}
          </span>
        ) : (
          <span>
            {result.passed_tests} / {result.total_tests} tests passed
          </span>
        )}
        <span className="ml-auto text-xs font-normal opacity-70">{result.duration_ms}ms</span>
      </div>

      <ul className="flex-1 divide-y divide-slate-100 overflow-y-auto dark:divide-slate-800">
        {result.results.map((r, i) => (
          <li key={i} className="p-4">
            <div className="flex items-center gap-2">
              {r.passed ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-500" />
              ) : (
                <XCircle className="h-4 w-4 shrink-0 text-rose-500" />
              )}
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200">{r.name}</span>
            </div>
            {!r.passed && (
              <div className="mt-2 space-y-1.5 pl-6 font-mono text-xs">
                <div className="text-slate-500 dark:text-slate-400">
                  input: <span className="text-slate-700 dark:text-slate-300">{r.input_repr}</span>
                </div>
                <div className="rounded bg-emerald-50 px-2 py-1 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300">
                  expected: {r.expected_repr}
                </div>
                <div className="rounded bg-rose-50 px-2 py-1 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300">
                  actual: {r.actual_repr ?? "(error)"}
                </div>
                {r.error && (
                  <pre className="whitespace-pre-wrap rounded bg-slate-900 px-2 py-1.5 text-slate-100">{r.error}</pre>
                )}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
