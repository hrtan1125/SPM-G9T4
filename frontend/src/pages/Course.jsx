
import { Button, TextField, Grid, Chip, Checkbox } from '@mui/material';
import axios from 'axios';
import React from 'react'
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
  console.log("add skills", key)
  if(Object.keys(skillsByCourse).includes(key)){
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
  }
}

const handleCheck = (event) => {
  var updatedList = [...checked];
  if (event.target.checked) {
    updatedList = [...checked, event.target.value];
  } else {
    updatedList.splice(checked.indexOf(event.target.value), 1);
  }
  setChecked(updatedList);
};

function refreshPage() {
  window.location.reload(false);
}

const handleSubmit = (e) => {
  e.preventDefault();
  refreshPage()
  assignSkillsToCourse(course_id, checked)
};

const assignSkillsToCourse = async(course_id, skills) => {
  console.log(skills, "skills")
  console.log(course_id,  "course_id")
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({course_id, skills})
  };
  fetch("http://127.0.0.1:5000/skill_assigns_course", requestOptions)
    .then(response => response.json())

} catch (error) {
    console.log(error.response)
}
};

console.log(Object.keys(skillsByCourse).length)

  return (
   <>
   <Grid item sx={{ display: "flex", alignItems: "center", marginTop: 3 }}>
        <h3>Course Name: {course_name}</h3>
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
