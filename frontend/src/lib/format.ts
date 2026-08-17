const SPECIAL_WORDS: Record<string, string> = {
  oop: "OOP",
  io: "I/O",
};

/** Turn a topic slug like "file_io" or "oop" into a readable label ("File I/O", "OOP"). */
export function formatTopicLabel(topic: string): string {
  return topic
    .split("_")
    .map((word) => SPECIAL_WORDS[word.toLowerCase()] ?? word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
