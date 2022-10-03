import { TextField } from '@mui/material';
import React, { useEffect } from 'react'
import { Routes, Route, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

const CreateEditRole = () => {

    const {role, setRoleId, setRole} = useGlobalContext()
    const {role_id} = useParams()
    console.log(role_id, "haha!!")
    console.log("good", role.role_name)

    if (role !== []){
        setRoleId(role_id)
    }
    console.log("better", role.role_name)


    
    
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
        {/* {role.length === 0? (
            <div>
                Role Name: <TextField id="outlined-basic" variant="outlined" />
            </div>
                
        
        ) : (
            <div>
                Role Name: <TextField id="outlined-basic"  variant="outlined" value={role.role_name} />
                {setRole("")}
            </div>
        )
        } */}
         <div>
            
                Role Name: <TextField id="outlined-basic"  variant="outlined" value={role.role_name} />
                {setRole("")}
                {/* Set role to prevent preset values for create role */}
            </div>
    </div>

  )
}

export default CreateEditRole