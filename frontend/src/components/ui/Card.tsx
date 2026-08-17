import type { HTMLAttributes } from "react";
import clsx from "clsx";

export function Card({ className, children, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={clsx(
        "rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-surface-dark-subtle",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export function CardBody({ className, children, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={clsx("p-5", className)} {...rest}>
      {children}
    </div>
  );
}
