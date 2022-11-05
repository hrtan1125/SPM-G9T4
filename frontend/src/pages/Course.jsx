
import { Button, TextField, Grid, Chip, Checkbox } from '@mui/material';
import axios from 'axios';
import React from 'react'
import { useEffect } from 'react';
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';


var toUpdateSkills = [];
var toDeleteSkills = [];
//need modify backend function to give me a list of related skills
const Course = () => {
    const {skills} = useGlobalContext()
    const {course_id, course_name} = useParams()
    const getSkillsByCourseUrl = "http://127.0.0.1:5000/view_skills_to_add/"
    const [skillsByCourse, setSkillsByCourse] = useState({})
    const [toAdd, setToAdd] = useState(false)
    const [toDelete, setToDelete] = useState(false)

    React.useEffect(() => {
        let isMounted = true;
        const fetchData = async () => {
            try {
                const response = await axios(`${getSkillsByCourseUrl}${course_id}`)
                  if (isMounted) {
                    setSkillsByCourse(response.data)
                  }
            } catch (error) {
                console.log(error)
            }
        }
        fetchData()
        return () => (isMounted = false);
      }, [])


const [checked, setChecked] = useState([]);

const handleUpdate = (e,key)=>{
  // console.log(skillsByCourse.skills, key)

  if(Object.keys(skillsByCourse).includes("skills")&&skillsByCourse.skills.includes(key)){
    if (toDeleteSkills.includes(key)){
      let idx = toDeleteSkills.indexOf(key)
      toDeleteSkills.splice(idx,1);
      e.currentTarget.style.backgroundColor="#e6e6e6";
      e.currentTarget.style.border="0px";
    }else{
      toDeleteSkills.push(key);
      e.currentTarget.style.backgroundColor="#ffffff";
      e.currentTarget.style.border="1px solid #bfbfbf";
    }
  }else{
    if(toUpdateSkills.includes(key)){
      let idx = toUpdateSkills.indexOf(key)
      toUpdateSkills.splice(idx,1);
      e.currentTarget.style.backgroundColor="#ffffff";
      e.currentTarget.style.border="1px solid #bfbfbf";
    }else{
      toUpdateSkills.push(key);
      e.currentTarget.style.backgroundColor="#e6e6e6";
      e.currentTarget.style.border="0px";
    }
  }
}


function refreshPage() {
  window.location.reload(false);
}

useEffect(()=>{
  if(toAdd && toDelete){
    refreshPage()
  }
},[toAdd,toDelete])

const handleSubmit = (e) => {
  e.preventDefault();
  console.log("Event is", e.target.textContent)
  
  if (toDeleteSkills.length !== 0) {
    if(toUpdateSkills.length===0 && (toDeleteSkills.length === skillsByCourse.skills.length)){
      alert("Deletion Failed! A course should have at least one skill!")
    }else{
      console.log("these are to be deleted", toDeleteSkills)
    //call delete function here
      setToDelete(true)
    }
  }else{
    setToDelete(true)
  }

  if (toUpdateSkills.length !== 0) {
    console.log("these are to be updated", toUpdateSkills)
    assignSkillsToCourse(course_id, toUpdateSkills)

  }else{
    setToAdd(true)
  }
};

const assignSkillsToCourse = async(course_id, skills) => {
  console.log(skills, "skills")
  console.log(course_id,  "course_id")
  try {
    fetch("http://127.0.0.1:5000/skill_assigns_course", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ course_id, skills })
    })
      .then(response => {
        response.json()
        setToAdd(true)
      })

} catch (error) {
    console.log(error.response)
}
};

  return (
   <>
   <Grid item sx={{ display: "flex", alignItems: "center", marginTop: 3 }}>    
      </Grid>
      <Grid item sx={{display:"flex", alignItems:"center"}}>
      <h3>Course Name: {course_name}</h3>
      <Button style={{backgroundColor:"#5289B5", marginLeft:"20px"}} variant="contained" onClick={(e) => handleSubmit(e)}>Update Skills</Button>
      </Grid>
      <Grid item sx={{ display: "flex", alignItems: "center", marginTop: 3 }}>
        Selects skills to add....
      </Grid>
      <Grid container spacing={2} marginTop={1}>
        {skills?.map((skill) => (
          <Chip key={skill.skill_code} label={skill.skill_name} sx={{ margin: 1 }} onClick={(e) => handleUpdate(e, skill.skill_code)} variant={skillsByCourse?.skills?.includes(skill.skill_code) ? "filled" : "outlined"} />))}
      </Grid>
   </>
  );
}
export default Course
