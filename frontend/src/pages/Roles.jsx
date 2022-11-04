import { useGlobalContext } from '../context';
import React, { useEffect, useState } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Pagination } from '@mui/material';
import { Link } from 'react-router-dom';
import AddIcon from "@mui/icons-material/Add"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';

const Roles = () => {
  const {setPath, setRoleId, userRole} = useGlobalContext()
  useEffect(()=>setPath("Roles"),[])
  useEffect(()=>setRoleId(0),[])

  const {rolesUrl, fetchRoles} = useGlobalContext()
  useEffect(() => {
    fetchRoles(rolesUrl)
}, [])

  const {roles, deleteRole} = useGlobalContext()

  const [page, setPage] = useState(1);

  

  const toDelete = (id) =>{
    console.log("deleting",id)
    deleteRole(id)
    window.location.reload(false)
  }

  const reseTableRowole = () => {
    console.log("reset")
  }

  var width = 500;
  if (userRole == 1) {
    width = 640;
  }

  function sliceIntoChunks(arr, chunkSize) {
    const res = [];
    for (let i = 0; i < arr.length; i += chunkSize) {
        const chunk = arr.slice(i, i + chunkSize);
        res.push(chunk);
    }
    return res;
  }

  const roles_chunks = sliceIntoChunks(roles, 20)

  const handleChange = (event, value) => {
    setPage(value);
  };


return (
  <div style={{display: 'flex', justifyContent: "center"}} >
      <div className="app-container" style={{display: 'flex',justifyContent:"center"}} >
        <Pagination count={roles_chunks.length} page={page} onChange={handleChange} />
        {userRole == 1 && <div style={{display: 'flex', justifyContent: "center"}} >
        <Link to={`/createrole`} style={{textDecoration:"none"}}> 
          <Button variant="contained" style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>} onClick={reseTableRowole}>Create New Role</Button>
        </Link>
        </div>}
      
        <TableContainer component={Paper} elevation={3}>
      <Table sx={{ minWidth: width, "& td": { border: 0 }}} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Role ID</TableCell>
            <TableCell align="left">Role Name</TableCell>
            {userRole == 1 && <><TableCell align="center"></TableCell>
            <TableCell align="center"></TableCell></>}
            
          </TableRow>
        </TableHead>
        <TableBody>
          {roles_chunks[page - 1]?.map((role) => (
            <TableRow
              key={role.role_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="left">
                {role.role_id}
              </TableCell>
              <TableCell align="left">{role.role_name}</TableCell>
              
              {userRole == 1 && <><TableCell align="center">
              <IconButton aria-label="delete" style={{color:"#5289B5"}} onClick={()=>toDelete(role.role_id)}>
                  <DeleteOutlinedIcon/>
              </IconButton>
              </TableCell>
              <TableCell align="center">
              <IconButton aria-label="edit" style={{color:"#5289B5"}} href={`/role/${role.role_id}/${role.role_name}`}>
                  <EditIcon/>
              </IconButton>
              </TableCell></>}
              
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
      </div>
    </div>
    );
  };

export default Roles