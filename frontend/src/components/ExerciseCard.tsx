import { Link } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import { Card, CardBody } from "./ui/Card";
import { DifficultyBadge, TopicBadge } from "./ui/Badge";
import type { ExerciseSummary } from "../types";

export function ExerciseCard({ exercise }: { exercise: ExerciseSummary }) {
  return (
    <Link to={`/exercises/${exercise.id}`} className="block focus-visible:outline-none">
      <Card className="group h-full transition-all duration-150 hover:-translate-y-0.5 hover:shadow-md hover:border-brand-300 dark:hover:border-brand-700 focus-visible:ring-2 focus-visible:ring-brand-500">
        <CardBody className="flex h-full flex-col gap-3">
          <div className="flex items-center justify-between gap-2">
            <TopicBadge topic={exercise.topic} />
            <DifficultyBadge difficulty={exercise.difficulty} />
          </div>
          <h3 className="text-base font-semibold text-slate-900 group-hover:text-brand-700 dark:text-slate-100 dark:group-hover:text-brand-300">
            {exercise.title}
          </h3>
          <div className="mt-auto flex items-center gap-1.5 text-xs">
            {exercise.solved ? (
              <span className="inline-flex items-center gap-1 font-medium text-emerald-600 dark:text-emerald-400">
                <CheckCircle2 className="h-3.5 w-3.5" /> Solved
              </span>
            ) : exercise.times_attempted > 0 ? (
              <span className="text-slate-400 dark:text-slate-500">
                {exercise.times_attempted} attempt{exercise.times_attempted === 1 ? "" : "s"}
              </span>
            ) : (
              <span className="text-slate-400 dark:text-slate-500">Not started</span>
            )}
          </div>
        </CardBody>
      </Card>
    </Link>
  );
}
