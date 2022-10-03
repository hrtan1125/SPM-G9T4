import { TextField } from '@mui/material';
import React, { useEffect } from 'react'
import { Routes, Route, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

const CreateEditRole = () => {

    const {role, setRoleId, showSkills, setRole} = useGlobalContext()
    console.log("skills", showSkills)
    const {role_id} = useParams()
    console.log(role, "haha")
    if (role !== []){
        setRoleId(role_id)
    }
    console.log("good", role.length)
    
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
        {role.length === 0? (
            <div>
                Role Name: <TextField id="outlined-basic" variant="outlined" />
            </div>
                
        
        ) : (
            <div>
                Role Name: <TextField id="outlined-basic"  variant="outlined" value={role.role_name} />
                {setRole("")}
            </div>
        )
        }
    </div>

  )
}

export default CreateEditRole