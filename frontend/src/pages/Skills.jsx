import { useGlobalContext } from '../context';
import React, { useEffect } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const Skills = () => {
  const {skills, deleteSkill, setSkill, fetchSkills, skillsUrl} = useGlobalContext()
  useEffect(() => {
    fetchSkills(skillsUrl)
}, [])

  const resetSkill = () => {
    setSkill("")
  }

    return (
      <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
         <div className="app-container">
         <Link to={`/createskill`}> 
          <Button onClick={resetSkill} variant="contained">Create New Skill</Button>
         </Link>
        <table>
          <thead>
            <tr>
              <th>Skill Code</th>
              <th>Skill Name</th>
              <th>Deleted?</th>
              <th>Delete</th>
              <th>Edit</th>

            </tr>
          </thead>
          <tbody>
          {skills.map((skill) => (
            <tr key={skill.skill_code}>
              {skill.deleted === "no" && (
                <>
                <td>
                  {skill.skill_code}
                </td>
                <td>
                  {skill.skill_name}
                </td>
                <td>
                  {skill.deleted === "yes" ? ("Yes"): ("No")}
                </td>
                <td>
                  <Grid item xs={8}>
                    <DeleteOutlinedIcon onClick={() => deleteSkill(skill.skill_code)}/>
                  </Grid>
                </td>
                <td>
                  <Grid item xs={8}>
                    <Link to={`/skill/${skill.skill_code}/${skill.skill_name}`}>
                      <EditIcon/>
                    </Link>
                  </Grid>
                </td>
                </>
              )}
            </tr>
          ))}
          </tbody>
        </table>
        </div>
      </div>
    );
  };
  

export default Skills