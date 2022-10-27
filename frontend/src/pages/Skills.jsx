import { useGlobalContext } from '../context';
import React, { useEffect } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link } from 'react-router-dom';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const Skills = () => {
  const {setPath} = useGlobalContext()
  useEffect(()=>setPath("Skills"))

  const {skills, deleteSkill, setSkill, fetchSkills, skillsUrl} = useGlobalContext()
  useEffect(() => {
    fetchSkills(skillsUrl)
}, [])

  const resetSkill = () => {
    setSkill("")
  }

    return (
      <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
        <div className="app-container" style={{display: 'flex',justifyContent:"center"}}>
          <div style={{display: 'flex', justifyContent: "center"}}>
            <Link to={`/createskill`} style={{textDecoration:"none"}}> 
            <Button onClick={resetSkill} style={{backgroundColor:"#5289B5"}} variant="contained">Create New Skill</Button>
            </Link>
          </div>
          <TableContainer component={Paper}>
          {/* TableContainer */}
          <Table sx={{ minWidth: 640, "& td": { border: 0 }}} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Skill Code</TableCell>
                <TableCell>Skill Name</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {skills.map((skill) => (
              <TableRow key={skill.skill_code} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              {skill.deleted === "no" && (
                <>
                <TableCell>
                  {skill.skill_code}
                </TableCell>
                <TableCell>
                  {skill.skill_name}
                </TableCell>
                <TableCell>
                  {skill.deleted === "yes" ? ("Yes"): ("No")}
                </TableCell>
                <TableCell>
                  <Grid item xs={8}>
                    <DeleteOutlinedIcon onClick={() => deleteSkill(skill.skill_code)}/>
                  </Grid>
                </TableCell>
                <TableCell>
                  <Grid item xs={8}>
                    <Link to={`/skill/${skill.skill_code}/${skill.skill_name}`}>
                      <EditIcon/>
                    </Link>
                  </Grid>
                </TableCell>
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