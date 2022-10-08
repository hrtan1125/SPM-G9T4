import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Roles from "./pages/Roles";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import Dashboard from "./pages/Dashboard";
import Skills from "./pages/Skills";
import Header from "./components/Header";
import LearningJourney from "./pages/LearningJourney";
import FilterTable from "./pages/FIlterTable";
import Tables from "./pages/Tables";
import CreateEditRole from "./components/CreateEditRole";
import CreateEditSkill from "./components/CreateEditSkill";
import CreateLJ from "./pages/CreateLJ";

function App() {
  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/courses" element={<Courses />}></Route>
          <Route path="/dashboard" element={<Dashboard />}></Route>
          <Route path="/roles" element={<Roles />}></Route>
          <Route path="/:role_id/:role_name" element={<CreateEditRole />} />
          <Route path="/skills" element={<Skills />}></Route>
          <Route
            path="/skill/:skill_code/:skill_name"
            element={<CreateEditSkill />}
          ></Route>
          <Route path="/learningjourney" element={<LearningJourney />} />
          {/* <Route path="/table" element={<FilterTable />} />
          <Route path="/tables" element={<Tables />} /> */}
          <Route path="/createrole" element={<CreateEditRole />} />
          <Route path="/createskill" element={<CreateEditSkill />} />
          <Route path="/createlearningjourney" element={<CreateLJ />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
