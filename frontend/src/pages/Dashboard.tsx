import { Link } from "react-router-dom";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Flame, Target, CheckCircle2, ListChecks, ArrowRight } from "lucide-react";
import { useProgress } from "../hooks/useProgress";
import { Card, CardBody } from "../components/ui/Card";
import { Skeleton } from "../components/ui/Skeleton";
import { Button } from "../components/ui/Button";
import { DifficultyBadge } from "../components/ui/Badge";
import { formatTopicLabel } from "../lib/format";

function StatCard({
  icon: Icon,
  label,
  value,
  accent,
}: {
  icon: typeof Flame;
  label: string;
  value: string;
  accent: string;
}) {
  return (
    <Card>
      <CardBody className="flex items-center gap-3">
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${accent}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <div className="text-xl font-bold text-slate-900 dark:text-slate-100">{value}</div>
          <div className="text-xs text-slate-500 dark:text-slate-400">{label}</div>
        </div>
      </CardBody>
    </Card>
  );
}

export function Dashboard() {
  const { data, loading, error } = useProgress();

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-10">
        <Skeleton className="h-8 w-48" />
        <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-20" />
          ))}
        </div>
        <Skeleton className="mt-6 h-72" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-16 text-center text-slate-600 dark:text-slate-400">
        {error ?? "No progress data available."}
      </div>
    );
  }

  const chartData = data.history.map((p) => ({
    day: p.day.slice(5),
    solves: p.solves,
    attempts: p.attempts,
  }));

  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Your Progress</h1>

      <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          icon={CheckCircle2}
          label="Exercises solved"
          value={`${data.solved_exercises} / ${data.total_exercises}`}
          accent="bg-emerald-50 text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-300"
        />
        <StatCard
          icon={Target}
          label="Completion"
          value={`${data.completion_pct}%`}
          accent="bg-brand-50 text-brand-600 dark:bg-brand-500/15 dark:text-brand-300"
        />
        <StatCard
          icon={Flame}
          label="Current streak"
          value={`${data.current_streak} day${data.current_streak === 1 ? "" : "s"}`}
          accent="bg-amber-50 text-amber-600 dark:bg-amber-500/15 dark:text-amber-300"
        />
        <StatCard
          icon={ListChecks}
          label="Total attempts"
          value={`${data.total_attempts}`}
          accent="bg-violet-50 text-violet-600 dark:bg-violet-500/15 dark:text-violet-300"
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="mb-4 text-sm font-semibold text-slate-700 dark:text-slate-300">
              Solves over the last 30 days
            </h2>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="solvesGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-800" />
                <XAxis dataKey="day" tick={{ fontSize: 11 }} interval={4} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11 }} width={24} />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  labelStyle={{ fontWeight: 600 }}
                />
                <Area type="monotone" dataKey="solves" stroke="#6366f1" fill="url(#solvesGradient)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="mb-4 text-sm font-semibold text-slate-700 dark:text-slate-300">Mastery by topic</h2>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.topic_mastery} layout="vertical" margin={{ left: 8 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} className="stroke-slate-200 dark:stroke-slate-800" />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} unit="%" />
                <YAxis
                  type="category"
                  dataKey="topic"
                  tick={{ fontSize: 11 }}
                  width={90}
                  tickFormatter={formatTopicLabel}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  formatter={(value) => [`${value}%`, "Mastery"]}
                />
                <Bar dataKey="mastery_pct" fill="#818cf8" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardBody>
        </Card>
      </div>

      {data.next_recommended && (
        <Card className="mt-6">
          <CardBody className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="text-xs font-medium uppercase tracking-wide text-slate-400">Up next</div>
              <div className="mt-1 flex items-center gap-2">
                <span className="font-semibold text-slate-900 dark:text-slate-100">
                  {data.next_recommended.title}
                </span>
                <DifficultyBadge difficulty={data.next_recommended.difficulty} />
              </div>
            </div>
            <Link to={`/exercises/${data.next_recommended.id}`}>
              <Button>
                Continue <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
