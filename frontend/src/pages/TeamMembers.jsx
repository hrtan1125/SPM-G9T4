import { Button, IconButton, Pagination, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import { useGlobalContext } from '../context';

const TeamMembers = () => {
    const {setPath, setRoleId, userDetails} = useGlobalContext()
    useEffect(()=>setPath("Roles"),[])
    useEffect(()=>setRoleId(0),[])
    console.log(userDetails)
    const viewTeamMembersUrl = 'http://127.0.0.1:5002/viewTeamMembers?dept='
  
    const {rolesUrl, fetchRoles} = useGlobalContext()
    useEffect(() => {
      fetchRoles(rolesUrl)
    }, [])
  
    const [page, setPage] = useState(1);

    const [teamMembers, setTeamMembers] = useState([]);
    const getTeamMembers = async () => {
        const { data } = await axios.get(`${viewTeamMembersUrl}${userDetails.dept}&staff_id=${userDetails.staff_id}`);
        setTeamMembers(data.data);
    };
    useEffect(() => {
        getTeamMembers();
    }, []);

    console.log(teamMembers)
  
    

  
    var width = 500;
    if (userDetails.role == 3) {
      width = 750;
    }

  
    function sliceIntoChunks(arr, chunkSize) {
      const res = [];
      for (let i = 0; i < arr.length; i += chunkSize) {
          const chunk = arr.slice(i, i + chunkSize);
          res.push(chunk);
      }
      return res;
    }
  
    const teamMembers_chunks = sliceIntoChunks(teamMembers, 20)
  
    const handleChange = (event, value) => {
      setPage(value);
    };
  
  
  return (
    <div style={{display: 'flex', justifyContent: "center"}} >
        <div className="app-container" style={{display: 'flex',justifyContent:"center"}} >
          <Pagination count={teamMembers_chunks.length} page={page} onChange={handleChange} />
        
          <TableContainer component={Paper} elevation={3}>
        <Table sx={{ minWidth: width, "& td": { border: 0 }}} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Staff ID</TableCell>
              <TableCell align="left">Staff Name</TableCell>
              <TableCell align="center">Staff Email</TableCell>
              <TableCell align="center">Staff Role</TableCell>
              
            </TableRow>
          </TableHead>
          <TableBody>
            {teamMembers_chunks[page-1]?.map((member) => (
              <TableRow
                key={member.Staff_id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell align="left">
                  {member.Staff_ID}
                </TableCell>
                <TableCell align="left">{member.Staff_FName}</TableCell>
                <TableCell align="center">{member.Email}</TableCell>
                <TableCell align="center">{member.Role === 1 ? (`Admin`): (member.Role === 3 ? (`Manager`):(`User`))}</TableCell>
                
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
        </div>
      </div>
    );
    };

export default TeamMembers