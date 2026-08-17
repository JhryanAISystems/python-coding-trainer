import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, BarChart3, Lightbulb, ShieldCheck, Code2 } from "lucide-react";
import { Button } from "../components/ui/Button";
import { Card, CardBody } from "../components/ui/Card";

const FEATURES = [
  {
    icon: Code2,
    title: "25+ hands-on exercises",
    body: "From variables and control flow to recursion, OOP, and decorators — spanning beginner to advanced.",
  },
  {
    icon: Sparkles,
    title: "Instant, precise feedback",
    body: "Every submission runs against real test cases, with a readable diff of expected vs. actual output.",
  },
  {
    icon: Lightbulb,
    title: "Progressive hints",
    body: "Stuck? Reveal hints one at a time instead of jumping straight to the answer.",
  },
  {
    icon: BarChart3,
    title: "Track your progress",
    body: "Streaks, topic mastery, and a visual history of your practice — all stored locally.",
  },
  {
    icon: ShieldCheck,
    title: "Secure sandboxed grading",
    body: "Your code runs in an isolated subprocess with strict time and memory limits — never eval'd directly.",
  },
];

export function Landing() {
  return (
    <div>
      <section className="relative overflow-hidden">
        <div
          className="absolute inset-0 -z-10 opacity-60 dark:opacity-40"
          style={{
            background:
              "radial-gradient(600px circle at 20% 0%, rgba(99,102,241,0.15), transparent 60%), radial-gradient(500px circle at 90% 20%, rgba(168,85,247,0.12), transparent 60%)",
          }}
        />
        <div className="mx-auto max-w-4xl px-6 py-20 text-center sm:py-28">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700 dark:border-brand-800 dark:bg-brand-500/10 dark:text-brand-300">
            <Sparkles className="h-3.5 w-3.5" />
            Learn Python by doing
          </span>
          <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl dark:text-white">
            Practice Python with <span className="text-brand-600 dark:text-brand-400">instant feedback</span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-600 dark:text-slate-300">
            An interactive coding trainer with a built-in editor, sandboxed grading, progressive hints, and
            progress tracking — no setup required.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link to="/exercises">
              <Button size="lg">
                Start practicing <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button size="lg" variant="secondary">
                View dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <Card key={f.title} className="animate-fade-in">
              <CardBody>
                <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-500/15 dark:text-brand-300">
                  <f.icon className="h-5 w-5" />
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-slate-100">{f.title}</h3>
                <p className="mt-1.5 text-sm text-slate-600 dark:text-slate-400">{f.body}</p>
              </CardBody>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
