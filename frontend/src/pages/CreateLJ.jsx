import { useGlobalContext } from '../context';

import React from "react";
import "./../App.css";
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';
import HorizontalLinearStepper from '../components/Stepper';
import LJroles from '../components/LJroles';
import LJskills from '../components/LJskills';
import LJcourses from '../components/LJcourses';

const LearningJourney = () => {
  const { activeStep, roleId, skillCode } = useGlobalContext()
    return (
      <div style={{marginTop: 80, justifyContent: "center"}} >
        <HorizontalLinearStepper />
        Selected Role ID: {roleId}
        <p></p>
        Selected Skill Code: {skillCode}
        {activeStep === 0 && <LJroles />}
        {activeStep === 1 && <LJskills />}
        {activeStep === 2 && <LJcourses />}
      </div>
     
    );
  };
  

export default LearningJourney