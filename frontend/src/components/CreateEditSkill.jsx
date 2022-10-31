import { Button, TextField } from '@mui/material';
import React, { useEffect, useState } from 'react'
import { Routes, Route, useParams, useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';

const CreateEditSkill = () => {
  let navigate = useNavigate();
    const {skill_code, skill_name} = useParams()
    console.log("SKILLNAME", skill_name)

    const {updateSkill, createSkill} = useGlobalContext()

    const [formData, setFormData] = React.useState(
      {skill_name: skill_name, skill_code: skill_code}
  )

    function handleChange(event) {
      setFormData(prevFormData => {
          return {
              ...prevFormData,
              [event.target.name]: event.target.value
          }
      })
  }
  console.log(formData, "formmdataa")

  const handleUpdateSubmit = (e) => {
    e.preventDefault();
    updateSkill(formData);
    navigate(`/Skills`);
 };

 const handleCreateSubmit = (e) => {
  e.preventDefault();
  createSkill(formData);
  navigate(`/Skills`);
};




  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >

            <div>
                {skill_name === undefined && (<>Skill Code: <TextField id="outlined-basic"  variant="outlined" name="skill_code" value={formData.skill_code} onChange={handleChange} /></> )}
            </div>
            <div>
              Skill Name: <TextField id="outlined-basic"  variant="outlined" name="skill_name" value={formData.skill_name} onChange={handleChange} />
            </div>
            <div>
              {skill_name === undefined ? (<Button onClick={(e) => handleCreateSubmit(e)} variant="contained">Create Skill</Button>):(<Button onClick={(e) => handleUpdateSubmit(e)} variant="contained">Update Skill Name</Button>)}
            </div>
    </div>
  )
}

export default CreateEditSkill