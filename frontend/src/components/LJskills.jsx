import { Button } from '@mui/material'
import React from 'react'
import { useGlobalContext } from '../context'
import Modal from './Modal'

const LJskills = () => {
    const {setSkillCode, relatedSkills, selectSkill, showModal} = useGlobalContext()
    console.log(relatedSkills, "related skilllss")

    const emptyCheck = [];

    relatedSkills?.map((skill) => (
    emptyCheck.push(skill.deleted)

  ))

  return (
    <div >
          {showModal && <Modal />}
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
            {relatedSkills?.map((skill) => (
              <tr>
                {skill.deleted === 'no' && (
                  <>
                  <td>
                  {skill.skill_name}
              </td>
              <td>
              <Button variant="contained" onClick={() => selectSkill(skill.skill_code)}>Select Skill</Button>
              
              </td>
              </>
                )
          }
              </tr>
            ))}
            </tbody>
          </table>
          ) : (
            <div>All the skills are deleted LMAO</div>
          )}
        </div>
      </div>

  )
}

export default LJskills