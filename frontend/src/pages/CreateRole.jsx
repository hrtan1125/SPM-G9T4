import { Button, TextField } from '@mui/material'
import React from 'react'
import ShowSkills from '../components/ShowSkills'
import { useGlobalContext } from '../context'


const CreateRole = () => {
    const {roles, deleteRole, role, showSkills} = useGlobalContext()
    console.log("skills", showSkills)
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
        <div>
        <TextField
            helperText="Please enter your Role Name"
            id="demo-helper-text-aligned"
            label="Role Name"
            />
        {showSkills && <ShowSkills />}
        </div>
        <div>
        <Button variant="text">Add Skills</Button>
        </div>
        

    </div>
    
  )
}

export default CreateRole