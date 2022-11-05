import { Button } from '@mui/material'
import React from 'react'
import { useGlobalContext } from '../context'
import Modal from './Modal'

const LJskills = () => {
    const { relatedSkills, selectSkill, showModal} = useGlobalContext()
    console.log(relatedSkills, "related skilllss")

    const emptyCheck = [];

  //   Object.keys(relatedSkills)?.map((skill) => (
  //   emptyCheck.push(skill.deleted)

  // ))

  return (
    <div >
          {showModal && <Modal />}
         <div className="app-container">
          {(Object.keys(relatedSkills).length!==0) ? (
            <table>
            <thead>
              <tr>
                <th>Skill Name</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {Object.keys(relatedSkills)?.map((skill_code) => (
              <tr key={skill_code}>
                {relatedSkills[skill_code].deleted === 'no' && (
                  <>
                  <td>
                      {relatedSkills[skill_code].skill_name}
                  </td>
                  <td>
                    <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={() => selectSkill(skill_code)}>View related courses</Button>
                  </td>
                </>
                )}
              </tr>
            ))}
            </tbody>
          </table>
          ) : (
            <div>No skills available</div>
          )}
        </div>
      </div>
  )
}

export default LJskills