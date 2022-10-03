
import { useGlobalContext } from '../context';

import React from "react";
import "./../App.css";
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const LearningJourney = () => {
  const {roles} = useGlobalContext()

  const emptyCheck = [];

  roles.map((role) => (
    emptyCheck.push(role.deleted)
  ))

    return (
      <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
         <div className="app-container">
          {(emptyCheck.includes('yes')) ? (
            <table>
            <thead>
              <tr>
                <th>Role Name</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {roles.map((role) => (
              <tr>
                {role.deleted === 'no' && (
                  <>
                  <td>
                  {role.role_name}
              </td>
              <td>
              <Button variant="contained" >Select Role</Button>
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
     
    );
  };
  

export default LearningJourney