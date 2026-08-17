import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ResultsPanel } from "./ResultsPanel";
import type { SubmitResponse } from "../types";

describe("ResultsPanel", () => {
  it("shows a placeholder when there is no result yet", () => {
    render(<ResultsPanel result={null} />);
    expect(screen.getByText(/Run your code/i)).toBeInTheDocument();
  });

  it("shows a fatal error message when grading errors out", () => {
    const result: SubmitResponse = {
      exercise_id: "x",
      mode: "run",
      passed: false,
      total_tests: 0,
      passed_tests: 0,
      results: [],
      duration_ms: 5,
      error: "SyntaxError: invalid syntax",
      newly_solved: false,
    };
    render(<ResultsPanel result={result} />);
    expect(screen.getByText(/Couldn't run your code/i)).toBeInTheDocument();
    expect(screen.getByText(/SyntaxError/)).toBeInTheDocument();
  });

  it("shows a success banner when all tests pass", () => {
    const result: SubmitResponse = {
      exercise_id: "x",
      mode: "submit",
      passed: true,
      total_tests: 2,
      passed_tests: 2,
      results: [
        { name: "a", passed: true, input_repr: "()", expected_repr: "1", actual_repr: "1", error: null, stdout: null },
        { name: "b", passed: true, input_repr: "()", expected_repr: "2", actual_repr: "2", error: null, stdout: null },
      ],
      duration_ms: 12,
      error: null,
      newly_solved: true,
    };
    render(<ResultsPanel result={result} />);
    expect(screen.getByText(/All 2 tests passed/)).toBeInTheDocument();
  });

  it("shows expected vs actual for failing tests", () => {
    const result: SubmitResponse = {
      exercise_id: "x",
      mode: "run",
      passed: false,
      total_tests: 1,
      passed_tests: 0,
      results: [
        {
          name: "case 1",
          passed: false,
          input_repr: "{'args': [5]}",
          expected_repr: "120",
          actual_repr: "5",
          error: null,
          stdout: null,
        },
      ],
      duration_ms: 8,
      error: null,
      newly_solved: false,
    };
    render(<ResultsPanel result={result} />);
    expect(screen.getByText(/0 \/ 1 tests passed/)).toBeInTheDocument();
    expect(screen.getByText(/expected: 120/)).toBeInTheDocument();
    expect(screen.getByText(/actual: 5/)).toBeInTheDocument();
  });
});
