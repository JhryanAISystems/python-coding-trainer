# LinkedIn Post Draft

Copy, tweak to your voice, and post alongside a screenshot or the demo GIF.

---

🐍 I built a Python Coding Trainer — an interactive practice platform with instant feedback, sandboxed grading, and progress tracking.

Learning to code is mostly about reps: write something, find out immediately if it's right, fix it, repeat. So I built the tool I wanted — 25+ hand-crafted exercises spanning variables, control flow, data structures, recursion, OOP, decorators, and more, each with an in-browser editor, hidden test cases, and progressive hints for when you're stuck.

Under the hood it's a full-stack app I'm proud of:
🔧 FastAPI + SQLAlchemy + Alembic backend with a sandboxed subprocess grading engine (no raw eval, strict timeouts, isolated filesystem access)
⚛️ React + TypeScript + Tailwind frontend with a Monaco code editor, dark mode, and Recharts-powered progress dashboards
🤖 Optional AI tutor mode (Claude-powered) that generates fresh exercises and reviews failed attempts — fully optional, the app works completely offline with the bundled exercise library
✅ Full test coverage on both ends, CI on every push, one-command Docker demo

It was a fun exercise (pun intended) in building something that's genuinely pleasant to use, not just functional — dark mode, micro-interactions, a real design system.

Check out the repo and try it yourself in under a minute with `docker-compose up`: [link]

#Python #WebDevelopment #FastAPI #React #OpenSource #BuildInPublic
