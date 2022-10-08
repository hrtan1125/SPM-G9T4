import { Button } from '@mui/material'
import React from 'react'
import { useGlobalContext } from '../context'

const LJskills = () => {
    const {roles, setRoleId, roleId, skills, skillCode, skill, setSkillCode, activeStep, setActiveStep} = useGlobalContext()
    console.log(skills, "skilllss")

    const emptyCheck = [];

    skills?.map((skill) => (
    emptyCheck.push(skill.deleted)

  ))

  const [formData, setFormData] = React.useState({})

  // const handleSkill = (e, skill_code, skill_name) => {
  //   e.preventDefault();
  //   console.log('fkkkrollee', skill_code)
  //   setSkillCode(skill_code)
    

  // };

  function handleChange(event) {
    const {name, value, type, checked} = event.target
    setFormData(prevFormData => {
        return {
            ...prevFormData,
            [name]: type === "checkbox" ? checked : value
        }
    })
}

  return (
    <div >
         <div className="app-container">
          {(emptyCheck.includes('no')) ? (
            <table>
            <thead>
              <tr>
                <th>Skill Name</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {skills?.map((skill) => (
              <tr>
                {skill.deleted === 'no' && (
                  <>
                  <td>
                  {skill.skill_name}
              </td>
              <td>
              {/* <Button variant="contained" onClick={(e) => handleSkill(e, skill.skill_code, skill.skill_name)}>Select Skill</Button> */}
              <input 
                type="checkbox" 
                id={skill.skill_code}
                checked={formData.skill_code}
                onChange={handleChange}
                name={skill.skill_code}
            />
              </td>
              </>
                )
          }
              </tr>
            ))}
            </tbody>
          </table>
          ) : (
            <div>All the roles are deleted LMAO</div>
          )}
        </div>
      </div>

  )
}

export default LJskills