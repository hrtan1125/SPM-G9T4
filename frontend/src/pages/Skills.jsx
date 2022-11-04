import { useGlobalContext } from '../context';
import React, { useEffect, useState } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid, Pagination } from '@mui/material';
import { Link } from 'react-router-dom';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import AddIcon from "@mui/icons-material/Add"
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';


const Skills = () => {
  const {setPath, userDetails} = useGlobalContext()
  useEffect(()=>setPath("Skills"))
  const [page, setPage] = useState(1);

  const {skills, deleteSkill, setSkill, fetchSkills, skillsUrl} = useGlobalContext()
  useEffect(() => {
    fetchSkills(skillsUrl)
}, [])

  const resetSkill = () => {
    setSkill("")
  }

  var width = 500;
  if (userDetails.role == 1) {
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

  const skills_chunks = sliceIntoChunks(skills, 20)

  const handleChange = (event, value) => {
    setPage(value);
  };

    return (
      <div style={{display: 'flex', justifyContent: "center"}} >
        <div className="app-container" style={{display: 'flex',justifyContent:"center"}}>
        <Pagination count={skills_chunks.length} page={page} onChange={handleChange} />
        {userDetails.role == 1 &&
          <div style={{display: 'flex', justifyContent: "center"}}>
            <Link to={`/createskill`} style={{textDecoration:"none"}}> 
            <Button onClick={resetSkill} style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>} variant="contained">Create New Skill</Button>
            </Link>
          </div>    
          }
          <TableContainer component={Paper} elevation={3}>
          {/* TableContainer */}
          <Table sx={{ minWidth: width, "& td": { border: 0 }}} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Skill Code</TableCell>
                <TableCell>Skill Name</TableCell>
                {userDetails.role == 1 && <>
                <TableCell></TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
                </>}
                
              </TableRow>
            </TableHead>
            <TableBody>
              {skills_chunks[page-1]?.map((skill) => (
              <TableRow key={skill.skill_code} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              {skill.deleted === "no" && (
                <>
                <TableCell>
                  {skill.skill_code}
                </TableCell>
                <TableCell>
                  {skill.skill_name}
                </TableCell>
                {userDetails.role == 1 && 
                <>
                <TableCell>
                  <IconButton aria-label="delete" style={{color:"#5289B5"}} onClick={()=>deleteSkill(skill.skill_code)}>
                      <DeleteOutlinedIcon/>
                  </IconButton>
                </TableCell>
                <TableCell align="center">
                  <IconButton aria-label="edit" style={{color:"#5289B5"}} href={`/skill/${skill.skill_code}/${skill.skill_name}`}>
                  <EditIcon/>
                </IconButton>
                </TableCell>
                </>}
                
                </>
              )}
            </TableRow>
          ))}
          </TableBody>
        </Table>
          </TableContainer>
          
        </div>
      </div>
    );
  };
  

export default Skills