import { useGlobalContext } from '../context';

import React, { useEffect } from "react";
import "./../App.css";
import HorizontalLinearStepper from '../components/Stepper';
import LJroles from '../pages/LJroles';
import LJskills from '../pages/LJskills';
// import LJroles from '../components/LJroles';
// import LJskills from '../components/LJskills';
import LJSubmitPage from '../pages/LJSubmit';

const LearningJourney = () => {
  const { activeStep, role, ljCourses } = useGlobalContext()
  console.log(ljCourses)


    return (
      <div style={{marginTop: 80, justifyContent: "center"}} >
        <HorizontalLinearStepper />
        <h2>
        Selected Role Name: {role.role_name}
        </h2>

        {activeStep === 0 && <LJroles />}
        {activeStep === 1 && <LJskills />}
        {activeStep === 2 && <LJSubmitPage />}

      </div>
    );
  };
  

export default LearningJourney