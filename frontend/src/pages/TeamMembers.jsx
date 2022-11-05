import { Button, IconButton, Pagination, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';
import VisibilityIcon from '@mui/icons-material/Visibility';

const TeamMembers = () => {
    const {setPath, setRoleId, userDetails} = useGlobalContext()
    const navigate = useNavigate()
    useEffect(()=>setPath("Roles"),[])
    useEffect(()=>setRoleId(0),[])
    console.log(userDetails)
    const viewTeamMembersUrl = 'http://127.0.0.1:5002/viewTeamMembers?dept='
    const [skills_ac, setSkillsAc] = useState(null)
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

    useEffect(()=>{
      fetch(`http://127.0.0.1:5000/viewTeamMembersSkills?dept=${userDetails.dept}&staff_id=${userDetails.staff_id}`)
      .then(res=>{
        return res.json()
      })
      .then(data=>{
        setSkillsAc(data.data)
      })
    },[])

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
              <TableCell align="center">Staff's Skills</TableCell>
              <TableCell align="center">View More</TableCell>
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
                <TableCell align="center" style={{maxWidth:"100px"}}>{skills_ac!==null && (skills_ac[member.Staff_ID]!==undefined)?
                Object.values(skills_ac[member.Staff_ID]).join(", ")
                  :<>no skills</>}
                </TableCell>
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

export default TeamMembers