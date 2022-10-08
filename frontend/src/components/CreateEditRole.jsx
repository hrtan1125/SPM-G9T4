import { Button, TextField } from '@mui/material';
import React from 'react'
import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';
import ShowSkills from './ShowSkills';

const CreateEditRole = () => {
    let navigate = useNavigate();
    const { setRoleId, updateRole} = useGlobalContext()
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
      navigate(`/Roles`);
    };
 
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
         <div>          
                Role Name: <TextField id="outlined-basic"  variant="outlined" value={roleName} onChange={handleChange}/>  
            </div>
            <div>
                {role_id === undefined ? (<ShowSkills role_name={roleName}/>) : (<Button onClick={(e) => handleUpdateSubmit(e)} variant="contained">Update Role Name</Button>)}
                
            </div>
    </div>
  )
}

export default CreateEditRole