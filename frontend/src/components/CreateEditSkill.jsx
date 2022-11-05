import { Button, TextField } from '@mui/material';
import React, { useEffect, useState } from 'react'
import { Routes, Route, useParams, useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';

const CreateEditSkill = () => {
  const updateSkillUrl = 'http://127.0.0.1:5000/update'
  const createSkillUrl = 'http://127.0.0.1:5000/create'
  let navigate = useNavigate();
  const { skill_code, skill_name } = useParams()

  const [status, setStatus] = useState(null)
  const [formData, setFormData] = React.useState(
    { skill_name: skill_name, skill_code: skill_code }
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

  useEffect(()=>{
    if(status===400){
      alert("Skill Name/Code has been used! Please try a new one.")
    }else if(status===200||status===201){
      navigate(`/Skills`);
    }
  },[status])

  const createSkill = async (formData) => {
    try {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      };
      fetch(createSkillUrl, requestOptions)
        .then(response => {
          setStatus(response.status)
          return response.json()
        })

    } catch (error) {
      console.log(error.response)
    }
  }

  const updateSkill = async (formData) => {
    try {
      const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      };
      fetch(updateSkillUrl, requestOptions)
        .then(response => {
          setStatus(response.status)
          return response.json()
        })

    } catch (error) {
      console.log(error.response)
    }
  }

  const handleUpdateSubmit = (e) => {
    e.preventDefault();
    updateSkill(formData);
  };

  const handleCreateSubmit = (e) => {
    e.preventDefault();
    createSkill(formData);
  };




  return (
    <div style={{ display: 'flex', marginTop: 80, justifyContent: "center" }} >

      <div>
        {skill_name === undefined && (<>Skill Code: <TextField id="outlined-basic" style={{ width: "100px" }} size="small" variant="outlined" name="skill_code" value={formData.skill_code} onChange={handleChange} /></>)}
      </div>
      <div>
        Skill Name: <TextField id="outlined-basic" style={{ width: "400px" }} variant="outlined" name="skill_name" size="small" value={formData.skill_name} onChange={handleChange} />
      </div>
      <div>
        {skill_name === undefined ? (<Button style={{ backgroundColor: "#5289B5" }} onClick={(e) => handleCreateSubmit(e)} variant="contained">Create Skill</Button>) : (<Button style={{ backgroundColor: "#5289B5" }} onClick={(e) => handleUpdateSubmit(e)} variant="contained">Update Skill Name</Button>)}
      </div>
    </div>
  )
}

export default CreateEditSkill