import { Button, TextField } from '@mui/material'
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useGlobalContext } from '../context'

const LJSubmitPage = () => {
  const { ljCourses, setActiveStep, setljCourses } = useGlobalContext()
  let navigate = useNavigate();

  const [formData, setFormData] = React.useState(
    {title: ""}
)

  function handleChange(event) {
    setFormData(prevFormData => {
        return {
            ...prevFormData,
            [event.target.name]: event.target.value
        }
    })
}

console.log(ljCourses, "LJcourses")

const learningjourneyData = {}

const handleSubmit = (e) => {
  e.preventDefault();
  
  learningjourneyData["courses"] = ljCourses
  // StaffId and RoleID are hard coded for now
  learningjourneyData["staff_id"] = 140105
  learningjourneyData["role_id"] = 10
  learningjourneyData["title"] = formData.title
  console.log(learningjourneyData, "Final LJ Data")
  addPosts(learningjourneyData);
  setActiveStep(0)
  setljCourses([])
  navigate(`/learningjourneys`);
};

const addPosts = async(learningjourneyData) => {
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(learningjourneyData)
  };
  fetch("http://127.0.0.1:5002/createlearningjourney", requestOptions)
    .then(response => response.json())

} catch (error) {
    console.log(error.response)
}
};

  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
      Learning Journey Name: <TextField id="outlined-basic"  variant="outlined" name="title" value={formData.title} onChange={handleChange} />
      <Button variant="contained" onClick={(e) => handleSubmit(e)}>Create Learning Journey</Button>
    </div>
  )
}

export default LJSubmitPage