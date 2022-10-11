import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Roles from "./pages/Roles";
import Skills from "./pages/Skills";
import Header from "./components/Header";
import LearningJourneys from "./pages/LearningJourneys";
import CreateEditRole from "./components/CreateEditRole";
import CreateEditSkill from "./components/CreateEditSkill";
import CreateLJ from "./pages/CreateLJ";
import Courses from "./pages/Courses";
import Course from "./pages/Course";

function App() {
  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<LearningJourneys />}></Route>
          <Route
            path="/learningjourneys"
            element={<LearningJourneys />}
          ></Route>
          <Route path="/createlearningjourney" element={<CreateLJ />} />

          <Route path="/roles" element={<Roles />}></Route>
          <Route path="/createrole" element={<CreateEditRole />} />
          <Route path="/:role_id/:role_name" element={<CreateEditRole />} />

          <Route path="/skills" element={<Skills />}></Route>
          <Route path="/createskill" element={<CreateEditSkill />} />
          <Route
            path="/skill/:skill_code/:skill_name"
            element={<CreateEditSkill />}
          ></Route>

          <Route path="/courses" element={<Courses />} />
          <Route path="/course/:course_id" element={<Course />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
