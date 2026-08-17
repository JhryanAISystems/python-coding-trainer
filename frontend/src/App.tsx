import { Route, Routes } from "react-router-dom";
import { Navbar } from "./components/layout/Navbar";
import { Landing } from "./pages/Landing";
import { Exercises } from "./pages/Exercises";
import { ExerciseWorkspace } from "./pages/ExerciseWorkspace";
import { Dashboard } from "./pages/Dashboard";

function App() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/exercises" element={<Exercises />} />
          <Route path="/exercises/:id" element={<ExerciseWorkspace />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
