import { useGlobalContext } from '../context';
import React, { useEffect } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';

const Roles = () => {
  const {rolesUrl, fetchRoles} = useGlobalContext()
  useEffect(() => {
    fetchRoles(rolesUrl)
}, [])

  const {roles, deleteRole, setRole} = useGlobalContext()

  const resetRole = () => {
    setRole("")
  }

return (
  <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
      <div className="app-container">
        <Link to={`/createrole`}> 
          <Button onClick={resetRole} variant="contained">Create New Role</Button>
        </Link>
      <table>
        <thead>
          <tr>
            <th>Role Id</th>
            <th>Role Name</th>
            <th>Deleted?</th>
            <th>Delete</th>
            <th>Edit</th>
            {/* <th>Add Skills</th> */}

          </tr>
        </thead>
        <tbody>
        {roles.map((role) => (
          <tr key={role.role_id}>
            {role.deleted === "no" && (
              <>
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
                    <Link to={`/${role.role_id}/${role.role_name}`}>
                      <EditIcon/>
                    </Link>
                </Grid>
              </td> 
            </>
            )} 
          </tr>
        ))}
        </tbody>
      </table>
      </div>
    </div>
    );
  };

export default Roles