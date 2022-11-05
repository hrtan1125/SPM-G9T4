import { Button, IconButton, Pagination, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';
import VisibilityIcon from '@mui/icons-material/Visibility';

const Learners = () => {
    const {setPath, setRoleId, userDetails} = useGlobalContext()
    useEffect(()=>setPath("Roles"),[])
    useEffect(()=>setRoleId(0),[])
    const navigate = useNavigate()

    const adminViewLearnersUrl = 'http://127.0.0.1:5002/AdminViewLearners?staff_id='
  
    const {rolesUrl, fetchRoles} = useGlobalContext()
    useEffect(() => {
      fetchRoles(rolesUrl)
    }, [])
  
    const [page, setPage] = useState(1);

    const [learners, setLearners] = useState([]);
    const getTeamMembers = async () => {
        const { data } = await axios.get(`${adminViewLearnersUrl}${userDetails.staff_id}`);
        setLearners(data.data);
    };
    useEffect(() => {
        getTeamMembers();
    }, [userDetails.staff_id]);
  
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
  
    const teamMembers_chunks = sliceIntoChunks(learners, 20)
  
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
              <TableCell align="center">Dept</TableCell>
              <TableCell align="center">View More</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teamMembers_chunks[page-1]?.map((member, index) => (
              <TableRow
                key={index}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell align="left">
                  {member.Staff_ID}
                </TableCell>
                <TableCell align="left">{member.Staff_FName} {member.Staff_LName}</TableCell>
                <TableCell align="center">{member.Email}</TableCell>
                <TableCell align="center">{member.Dept}</TableCell>
                {/* <TableCell align="center">{member.Role === 1 ? (`Admin`): (member.Role === 2 ? (`User`):(`Manager`))}</TableCell> */}
                <TableCell align="center"><VisibilityIcon style={{color:"#5289B5"}} onClick={()=>navigate(`/learningjourneys/team/${member.Staff_ID}`)}/></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
        </div>
      </div>
    );
    };

export default Learners