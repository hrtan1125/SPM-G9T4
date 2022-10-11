import { useGlobalContext } from '../context';

import React from "react";
import "./../App.css";
import HorizontalLinearStepper from '../components/Stepper';
import LJroles from '../components/LJroles';
import LJskills from '../components/LJskills';
import LJSubmitPage from '../components/LJSubmitPage';

const LearningJourney = () => {
  const { activeStep, role, ljCourses } = useGlobalContext()
    return (
      <div style={{marginTop: 80, justifyContent: "center"}} >
        <HorizontalLinearStepper />
        <h2>
        Selected Role Name: {role.role_name}
        </h2>

        {Object.keys(ljCourses).map((key, index) => {
          return (
            <div key={key}>
              <h2>
                 Skill Code: {key} ----- Courses Code:{ljCourses[key].toString()}
              </h2>
            </div>
          )
        })}
        {activeStep === 0 && <LJroles />}
        {activeStep === 1 && <LJskills />}
        {activeStep === 2 && <LJSubmitPage />}
      </div>
    );
  };
  

export default LearningJourney