
import { Button, Checkbox, TextField } from '@mui/material';
import axios from 'axios';
import React from 'react'
import { useState } from 'react';
import { useParams } from 'react-router-dom';

const Course = () => {
    const {course_id} = useParams()
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

  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
       <div className="app-container">
        <table>
          <thead>
            <tr>
              <th>Skill Code</th>
              <th>Skills already associated with this course</th>
            </tr>
          </thead>
          <tbody>
          {skillsByCourse?.skills?.yes?.map((course)=> (
            <tr key={course.skill_code}>
              <td>
                {course.skill_code}
              </td>
              <td>
                {course.skill_name}
              </td>
            </tr>
          ))}
          </tbody>
        </table>
        <Button variant="contained" onClick={(e) => handleSubmit(e)}>Add Skill/s to Course</Button>
      <table>
        <thead>
          <tr>
            <th>Skill Code</th>
            <th>Skill Name</th>
            <th>Add Skill</th>
          </tr>
        </thead>
        <tbody>
        {skillsByCourse?.skills?.no?.map((course)=> (
          <tr key={course.skill_code}>
              <td>
                {course.skill_code}
              </td>
              <td>
                {course.skill_name}
              </td>
              <td>
                <input value={course.skill_code} type="checkbox" onChange={handleCheck} />
              </td>
          </tr>
        ))}
        </tbody>
      </table>
    </div>
  </div>
  );
}
export default Course
