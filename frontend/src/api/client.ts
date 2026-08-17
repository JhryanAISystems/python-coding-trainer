import axios from "axios";
import type {
  AIStatusResponse,
  CodeReviewResponse,
  ExerciseDetail,
  ExerciseListResponse,
  GeneratedExercise,
  HintResponse,
  ProgressResponse,
  SubmitResponse,
} from "../types";

const api = axios.create({ baseURL: "/api" });

export interface ApiErrorShape {
  detail?: string;
}

export function getApiErrorMessage(err: unknown, fallback: string): string {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data as ApiErrorShape | undefined;
    if (data?.detail) return data.detail;
    if (err.response?.status === 429) return "Too many requests. Please slow down.";
  }
  return fallback;
}

export async function listExercises(params?: { topic?: string; difficulty?: string }) {
  const { data } = await api.get<ExerciseListResponse>("/exercises", { params });
  return data;
}

export async function getExercise(id: string) {
  const { data } = await api.get<ExerciseDetail>(`/exercises/${id}`);
  return data;
}

export async function getHint(id: string, hintIndex: number) {
  const { data } = await api.get<HintResponse>(`/exercises/${id}/hints/${hintIndex}`);
  return data;
}

export async function submitSolution(id: string, code: string, mode: "run" | "submit") {
  const { data } = await api.post<SubmitResponse>(`/exercises/${id}/submit`, { code, mode });
  return data;
}

export async function getProgress() {
  const { data } = await api.get<ProgressResponse>("/progress");
  return data;
}

export async function getAIStatus() {
  const { data } = await api.get<AIStatusResponse>("/ai/status");
  return data;
}

export async function generateAIExercise(topic: string, difficulty: string) {
  const { data } = await api.post<GeneratedExercise>("/ai/generate-exercise", { topic, difficulty });
  return data;
}

export async function reviewCodeWithAI(exerciseId: string, code: string) {
  const { data } = await api.post<CodeReviewResponse>("/ai/review", { exercise_id: exerciseId, code });
  return data;
}
