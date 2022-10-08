import { Button } from '@mui/material'
import React from 'react'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
      <Link to={`/createlearningjourney`}> 
         <Button variant="contained">Create New Skill</Button>
        </Link>
    </div>
  )
}

export default Dashboard