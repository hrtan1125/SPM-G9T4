import { Button } from '@mui/material';
import React from 'react'
import { useGlobalContext } from '../context'

const LJroles = () => {
const {roles, setRoleId, activeStep, setActiveStep} = useGlobalContext()

const emptyCheck = [];

  roles.map((role) => (
    emptyCheck.push(role.deleted)
  ))

  const handleRole = (e, role_id) => {
    e.preventDefault();
    setRoleId(role_id)
    setActiveStep(activeStep + 1)
  };

  return (
    <div >
         <div className="app-container">
          {(emptyCheck.includes('no')) ? (
            <table>
            <thead>
              <tr>
                <th>Role Name</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {roles.map((role) => (
              <tr key={role.role_id}>
                {role.deleted === 'no' && (
                  <>
                  <td>
                  {role.role_name}
              </td>
              <td>
              <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleRole(e, role.role_id)}>Select Role</Button>
              </td>
              </>
                )}
              </tr>
            ))}
            </tbody>
          </table>
          ) : (
            <div>No roles available</div>
          )}
        </div>
      </div>
  )
}

export default LJroles