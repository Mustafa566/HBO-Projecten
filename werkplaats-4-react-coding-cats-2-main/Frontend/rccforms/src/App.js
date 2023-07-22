import React, { useEffect, useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { Sidebar, Menu, MenuItem, SubMenu, useProSidebar } from "react-pro-sidebar";

import './App.css';
import CurrentUser from './CurrentUser';
import Homepage from "./pages/Homepage";
import OpenQuestions from "./pages/OpenQuestions";
import McQuestions from "./pages/McQuestions";
import Forms from "./components/making_forms/Forms";
import LoginPage from './pages/Login';
import RegistrationForm from './pages/Registration';
import SurveyDetail from './pages/SurveyDetail';
import Users from "./pages/Users";

import MenuOutlinedIcon from '@mui/icons-material/MenuOutlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import NoteAltOutlinedIcon from '@mui/icons-material/NoteAltOutlined';
import QuizOutlinedIcon from '@mui/icons-material/QuizOutlined';
import Diversity3OutlinedIcon from '@mui/icons-material/Diversity3Outlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import LoginOutlinedIcon from '@mui/icons-material/LoginOutlined';
import AddIcon from '@mui/icons-material/Add';

function App() {
  const { collapseSidebar } = useProSidebar();
  const [username, setUsername] = useState(localStorage.getItem("Username"));
  const [role, setRole] = useState(localStorage.getItem("Role"));

  function logOut() {
    localStorage.removeItem('Username');
    localStorage.removeItem('Role');
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setUsername(localStorage.getItem("Username"));
      setRole(localStorage.getItem("Role"));
    }, 500);

    return () => clearInterval(interval);
  }, []);

    return (
        <div
            id="app"
            style={{
                height: "100vh",
                display: "flex"
            }}
        >
            {username ? (
  <Sidebar style={{ height: "100vh" }}>
    <Menu>
      <React.Fragment>
        <MenuItem
          icon={<MenuOutlinedIcon />}
          style={{ textAlign: "center" }}
          onClick={() => {
            collapseSidebar();
          }}
        >
          <h2>
            <CurrentUser />
          </h2>
        </MenuItem>
        <MenuItem icon={<HomeOutlinedIcon />} component={<Link to="/home" />}>
          Home
        </MenuItem>

          <MenuItem
            icon={<Diversity3OutlinedIcon />}
            component={<Link to="/userlist" />}
            >Teamleden</MenuItem>

        <SubMenu icon={<QuizOutlinedIcon />} label="Vragen">
          <MenuItem component={<Link to="/openQuestions" />}>
            Open vragen
          </MenuItem>
          <MenuItem component={<Link to="/mcQuestions" />}>
            Meerkeuzevragen
          </MenuItem>
        </SubMenu>

        <SubMenu icon={<NoteAltOutlinedIcon />} label="Vragenlijsten">
          <MenuItem component={<Link to="/forms" />}>Overzicht</MenuItem>
          <MenuItem>Responsen</MenuItem>
        </SubMenu>

        <MenuItem icon={<AccountCircleOutlinedIcon />} >Mijn account</MenuItem>
      </React.Fragment>

      {role && (
        <MenuItem icon={<AddIcon />} component={<Link to="/registration" />}>
          Create user
        </MenuItem>
      )}

      <MenuItem
        icon={<LoginOutlinedIcon />}
        onClick={() => {
          logOut();
        }}
      >
        Logout
      </MenuItem>
    </Menu>
  </Sidebar>
) : (
  <p></p>
)}


            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path='/home' element={<Homepage/>}/>
                <Route path='/openQuestions' element={<OpenQuestions/>}/>
                <Route path='/mcQuestions' element={<McQuestions/>}/>
                <Route path="/forms" element={<Forms />} />
                <Route path="/registration" element={<RegistrationForm />} />
                <Route path="/survey/:id" element={<SurveyDetail />} />
              <Route path="/userlist" element={<Users />} />
      </Routes>
        </div>
    );
}

export default App;