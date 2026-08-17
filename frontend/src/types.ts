export type Difficulty = "beginner" | "intermediate" | "advanced";

export interface ExerciseSummary {
  id: string;
  title: string;
  topic: string;
  difficulty: Difficulty;
  order: number;
  solved: boolean;
  times_attempted: number;
}

export interface ExerciseDetail {
  id: string;
  title: string;
  topic: string;
  difficulty: Difficulty;
  description: string;
  starter_code: string;
  function_name: string;
  hint_count: number;
  solved: boolean;
  times_attempted: number;
}

export interface ExerciseListResponse {
  exercises: ExerciseSummary[];
  topics: string[];
}

export interface HintResponse {
  exercise_id: string;
  hint_index: number;
  hint: string;
  hints_remaining: number;
}

export interface TestCaseResult {
  name: string;
  passed: boolean;
  input_repr: string;
  expected_repr: string;
  actual_repr: string | null;
  error: string | null;
  stdout: string | null;
}

export interface SubmitResponse {
  exercise_id: string;
  mode: "run" | "submit";
  passed: boolean;
  total_tests: number;
  passed_tests: number;
  results: TestCaseResult[];
  duration_ms: number;
  error: string | null;
  newly_solved: boolean;
}

export interface TopicMastery {
  topic: string;
  solved: number;
  total: number;
  mastery_pct: number;
}

export interface ProgressPoint {
  day: string;
  attempts: number;
  solves: number;
}

export interface ProgressResponse {
  total_exercises: number;
  solved_exercises: number;
  completion_pct: number;
  current_streak: number;
  longest_streak: number;
  total_attempts: number;
  topic_mastery: TopicMastery[];
  history: ProgressPoint[];
  next_recommended: ExerciseSummary | null;
}

export interface AIStatusResponse {
  enabled: boolean;
  provider: string | null;
}

export interface GeneratedExercise {
  title: string;
  description: string;
  starter_code: string;
  function_name: string;
}

export interface CodeReviewResponse {
  review: string;
}
