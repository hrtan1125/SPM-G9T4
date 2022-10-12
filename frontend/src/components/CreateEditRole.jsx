import { Button, TextField } from '@mui/material';
import axios from 'axios';
import React from 'react'
import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';
import ShowSkills from './ShowSkills';

const CreateEditRole = () => {
  const { relatedSkills, setRoleId, updateRole, skills } = useGlobalContext()
  console.log(relatedSkills, "related skills")

  const skill_codes_relatedToRole = [];

  relatedSkills.map((skill) => skill_codes_relatedToRole.push(skill.skill_code))

    let navigate = useNavigate();
    const {role_id, role_name} = useParams()

    setRoleId(role_id)

    const [roleName, setRoleName] = useState(role_name)


    function handleChange(event) {
        setRoleName(event.target.value)
    }

    const handleUpdateSubmit = (e) => {
      e.preventDefault();
      updateRole({
        "role_id": role_id,
        "role_name": roleName
      });
      // navigate(`/Roles`);
    };

    console.log(role_id)


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
  assignSkillsToRole(role_id, checked)
};

const assignSkillsToRole = async(role_id, skill_code) => {
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({role_id, skill_code})
  };
  fetch("http://127.0.0.1:5001/assignSkills", requestOptions)
    .then(response => response.json())

} catch (error) {
    console.log(error.response)
}
};


  return (
    <div style={{marginTop: 80, justifyContent: "center"}} >
         <div>          
              Role Name: <TextField id="outlined-basic"  variant="outlined" value={roleName} onChange={handleChange}/>  
          </div>
          <div>
              {role_id === undefined ? (<ShowSkills role_name={roleName}/>) : (<Button onClick={(e) => handleUpdateSubmit(e)} variant="contained">Update Role Name</Button>)}
          </div>
            {role_id !== undefined && 
              <>
              <table>
                <thead>
                  <tr>
                    <th>Skills already associated with this Role </th>
                  </tr>
                </thead>
                <tbody>
                {relatedSkills?.map((skill)=> (
                  <tr key={skill.skill_code}>
                      <td>
                    {skill.skill_name}
                    </td>
                  </tr>
                ))}
                </tbody>
              </table>
              <div>Skills to add below</div>
              <Button variant="contained" onClick={(e) => handleSubmit(e)}>Add Skill/s to Role</Button>
              <table>
                <thead>
                  <tr>
                    <th>Skill Code</th>
                    <th>Skill to Add</th>
                    <th>Add Skill</th>
                  </tr>
                </thead>
                <tbody>
                {skills.map((skill)=> (
                  <tr key={skill.skill_code}>
                    {!skill_codes_relatedToRole?.includes(skill.skill_code) && (
                      <>
                      <td>
                    {skill.skill_code}
                    </td>
                    <td>
                    {skill.skill_name}
                    </td>
                    <td>
                    <input value={skill.skill_code} type="checkbox" onChange={handleCheck} />
                    </td>
                      </>
                      )}
                  </tr>
                ))}
                </tbody>
              </table>
              </>
            }
                 
    </div>
  )
}

export default CreateEditRole
