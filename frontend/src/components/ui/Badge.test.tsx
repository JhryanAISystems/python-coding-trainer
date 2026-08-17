import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { DifficultyBadge, TopicBadge } from "./Badge";

describe("DifficultyBadge", () => {
  it("renders the difficulty label", () => {
    render(<DifficultyBadge difficulty="beginner" />);
    expect(screen.getByText("beginner")).toBeInTheDocument();
  });
});

describe("TopicBadge", () => {
  it("replaces underscores with spaces and title-cases each word", () => {
    render(<TopicBadge topic="data_structures" />);
    expect(screen.getByText("Data Structures")).toBeInTheDocument();
  });

  it("upper-cases known acronyms like OOP", () => {
    render(<TopicBadge topic="oop" />);
    expect(screen.getByText("OOP")).toBeInTheDocument();
  });
});
