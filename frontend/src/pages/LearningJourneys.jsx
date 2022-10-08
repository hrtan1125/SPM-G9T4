import { Button } from '@mui/material'
import React from 'react'
import { Link } from 'react-router-dom'

const LearningJourneys = () => {
  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
      <Link to={`/createlearningjourney`}> 
         <Button variant="contained">Create New Learning Journey</Button>
        </Link>
    </div>
  )
}

export default LearningJourneys