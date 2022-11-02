import "./App.css";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useGlobalContext } from "./context";
import Box from "@mui/material/Box";
import PermanentDrawerLeft from "./components/Drawer";
import Roles from "./pages/Roles";
import Skills from "./pages/Skills";
import Header from "./components/Header";
import { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import AppBar from "@mui/material/AppBar";
import LearningJourneys from "./pages/LearningJourneys";
import CreateEditRole from "./components/CreateEditRole";
import CreateEditSkill from "./components/CreateEditSkill";
import CreateLJ from "./pages/CreateLJ";
import Courses from "./pages/Courses";
import Course from "./pages/Course";
import LJDetails from "./pages/LJdetails";
import Login from "./pages/Login";
import TeamMembers from "./pages/TeamMembers";

const drawerWidth = 240;

const theme = createTheme({
  typography: {
    fontFamily: ["EBGaramond", "serif"],
  },
});

export default function App() {
  const { path, userRole } = useGlobalContext();
  const roles_id_role_name = {
    1: "Admin",
    2: "User",
    3: "Manager",
  };

  const sx = {
    width: userRole !== "" && `calc(100% - ${drawerWidth}px)`,
    ml: userRole !== "" && `${drawerWidth}px`,
  };
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: "flex" }}>
          <AppBar
            elevation={0}
            style={{ backgroundColor: "#AFD8F2", color: "#1F3541" }}
            // sx={{
            //   width: `calc(100% - ${drawerWidth}px)`,
            //   ml: `${drawerWidth}px`,
            // }}
            // sx={sx}
          >
            <Toolbar>
              <Typography
                variant="h6"
                noWrap
                component="div"
                style={{ fontWeight: "bold" }}
                sx={{ flexGrow: 1 }}
              >
                {path}
              </Typography>
              <Typography
                variant="h6"
                noWrap
                component="div"
                style={{ fontWeight: "bold" }}
              >
                {userRole !== "" && (
                  <>Logged in as {roles_id_role_name[userRole]}</>
                )}
              </Typography>
            </Toolbar>
          </AppBar>
          {userRole != "" && <PermanentDrawerLeft />}

          <Box
            style={{ margin: "60px" }}
            component="main"
            sx={{ flexGrow: 1, bgcolor: "background.default", p: 3 }}
          >
            <Routes>
              <Route path="/" element={<Login />}></Route>
              <Route path="/Login" element={<Login />}></Route>
              <Route
                path="/learningjourneys"
                element={<LearningJourneys />}
              ></Route>
              <Route path="/createlearningjourney" element={<CreateLJ />} />

              <Route path="/roles" element={<Roles />}></Route>
              <Route path="/createrole" element={<CreateEditRole />} />
              <Route
                path="/role/:role_id/:role_name"
                element={<CreateEditRole />}
              />
              <Route
                path="/learningjourney/:id"
                element={<LJDetails />}
              ></Route>

              <Route path="/skills" element={<Skills />}></Route>
              <Route path="/createskill" element={<CreateEditSkill />} />
              <Route
                path="/skill/:skill_code/:skill_name"
                element={<CreateEditSkill />}
              ></Route>

              <Route path="/courses" element={<Courses />} />
              <Route path="/course/:course_id" element={<Course />} />

              <Route path="/teammembers" element={<TeamMembers />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

// export default App;
