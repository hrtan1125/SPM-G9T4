import { TextField } from '@mui/material';
import React, { useEffect } from 'react'
import { Routes, Route, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

const CreateEditSkill = () => {
    const {skill, setSkillCode, setSkill} = useGlobalContext()
    const {skill_code} = useParams()

    setSkillCode(skill_code)

  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >

            <div>
                Skill Name: <TextField id="outlined-basic"  variant="outlined" value={skill.skill_name} />
                {setSkill("")}
            </div>
    </div>
  )
}

export default CreateEditSkill