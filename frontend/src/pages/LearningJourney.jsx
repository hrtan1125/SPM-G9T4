
import { useGlobalContext } from '../context';

import React, { useState, Fragment } from "react";
import { nanoid } from "nanoid";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const LearningJourney = () => {
  const {roles, deleteRole, role} = useGlobalContext()

    return (
      <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
         <div className="app-container">

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

</div>
      </div>
     
    );
  };
  

export default LearningJourney