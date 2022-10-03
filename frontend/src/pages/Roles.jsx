
import { useGlobalContext } from '../context';

import React, { useState, Fragment } from "react";
import { nanoid } from "nanoid";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const Roles = () => {
  const {roles, deleteRole, role} = useGlobalContext()

  console.log("ROLEESS", roles)
  console.log("ROLEE", role)

    return (
      <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
         <div className="app-container">
         <Link to={`/createrole`}> 
         <Button variant="contained">Create New Role</Button>
         </Link>
<table>
  <thead>
    <tr>
      <th>Role Id</th>
      <th>Role Name</th>
      <th>Deleted?</th>
      <th>Delete</th>
      <th>Edit</th>

    </tr>
  </thead>
  <tbody>
  {roles.map((role) => (
    <tr>
      <td>
      {role.role_id}
      </td>

        <td>
        {role.role_name}
    </td>
    <td>
      {role.deleted === "yes" ? ("Yes"): ("No")}
    </td>

    <td>
    <Grid item xs={8}>
        <DeleteOutlinedIcon onClick={() => deleteRole(role.role_id)}/>
    </Grid>
    </td>
    <td>
    <Grid item xs={8}>
        <Link to={`/${role.role_id}`}>
        <EditIcon/>
        </Link>
        
    </Grid>
    </td>

    </tr>
  ))}
  </tbody>
</table>

</div>
      </div>
     
    );
  };
  

export default Roles