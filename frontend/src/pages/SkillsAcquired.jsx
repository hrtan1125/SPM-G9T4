import { useGlobalContext } from '../context';
import React, { useEffect, useState } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Pagination } from '@mui/material';
import { Link, useParams } from 'react-router-dom';
import AddIcon from "@mui/icons-material/Add"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';

const SkillsAc = () =>{
    const [skills_ac,setSkillsAc] = useState(null)
    var width = 500;
    const {sid} = useParams()
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/viewLearnersSkills?staff_id=${sid}`)
        .then(res=>{
            return res.json()
        }).then(data=>{
            setSkillsAc(data.data)
            console.log("testing only")
            console.log(skills_ac)
        })
    },[sid])

    return(
    <>
    <h3>Following are the skills acquired</h3>
    <TableContainer component={Paper} elevation={3}>
      <Table sx={{ minWidth: width, "& td": { border: 0 }}} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Skill Code</TableCell>
            <TableCell align="left">Skill Name</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {skills_ac?.map((skill) => (
            <TableRow
              key={Object.keys(skill)[0]}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="left">
                {Object.keys(skill)[0]}
              </TableCell>
              <TableCell align="left">{Object.values(skill)[0]}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </>
    )
}

export default SkillsAc