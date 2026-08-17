import type { HTMLAttributes } from "react";
import clsx from "clsx";
import type { Difficulty } from "../../types";
import { formatTopicLabel } from "../../lib/format";

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  beginner: "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300",
  intermediate: "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
  advanced: "bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300",
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize",
        DIFFICULTY_STYLES[difficulty],
      )}
    >
      {difficulty}
    </span>
  );
}

export function TopicBadge({ topic, className, ...rest }: { topic: string } & HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-semibold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300",
        className,
      )}
      {...rest}
    >
      {formatTopicLabel(topic)}
    </span>
  );
}
