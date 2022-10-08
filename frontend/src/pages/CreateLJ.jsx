import { useGlobalContext } from '../context';

import React from "react";
import "./../App.css";
import HorizontalLinearStepper from '../components/Stepper';
import LJroles from '../components/LJroles';
import LJskills from '../components/LJskills';
import LJcourses from '../components/LJcourses';

const LearningJourney = () => {
  const { activeStep, roleId, skillCode, role, ljCourses } = useGlobalContext()
    return (
      <div style={{marginTop: 80, justifyContent: "center"}} >
        <HorizontalLinearStepper />
        {/* Selected Role ID: {roleId}
        <br/> */}
        <h2>
        Selected Role Name: {role.role_name}
        </h2>
        
        <p></p>
        {/* Selected Skill Code: {skillCode}
        <br/>
        Selected Skill Name: {role.role_name}
        <br/> */}
        <h2>
        Selected Courses Name: 
        </h2>
        {Object.keys(ljCourses).map((key, index) => {
          return (
            <div key={key}>
              <h2>
                {ljCourses[key]}
              </h2>
            </div>
          )
        })}
        {activeStep === 0 && <LJroles />}
        {activeStep === 1 && <LJskills />}
        {activeStep === 2 && <LJcourses />}
      </div>
     
    );
  };
  

export default LearningJourney