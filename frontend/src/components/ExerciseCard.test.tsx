import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ExerciseCard } from "./ExerciseCard";
import type { ExerciseSummary } from "../types";

const baseExercise: ExerciseSummary = {
  id: "recursion-01-factorial",
  title: "Factorial (Recursive)",
  topic: "recursion",
  difficulty: "beginner",
  order: 1,
  solved: false,
  times_attempted: 0,
};

function renderCard(exercise: ExerciseSummary) {
  return render(
    <MemoryRouter>
      <ExerciseCard exercise={exercise} />
    </MemoryRouter>,
  );
}

describe("ExerciseCard", () => {
  it("shows the exercise title and topic", () => {
    renderCard(baseExercise);
    expect(screen.getByText("Factorial (Recursive)")).toBeInTheDocument();
    expect(screen.getByText("Recursion")).toBeInTheDocument();
  });

  it("shows 'Not started' when there are no attempts", () => {
    renderCard(baseExercise);
    expect(screen.getByText("Not started")).toBeInTheDocument();
  });

  it("shows 'Solved' when the exercise is solved", () => {
    renderCard({ ...baseExercise, solved: true, times_attempted: 2 });
    expect(screen.getByText("Solved")).toBeInTheDocument();
  });

  it("shows attempt count when attempted but not solved", () => {
    renderCard({ ...baseExercise, times_attempted: 3 });
    expect(screen.getByText("3 attempts")).toBeInTheDocument();
  });

  it("links to the exercise workspace", () => {
    renderCard(baseExercise);
    expect(screen.getByRole("link")).toHaveAttribute("href", "/exercises/recursion-01-factorial");
  });
});
