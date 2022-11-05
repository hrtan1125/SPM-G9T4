import { useGlobalContext } from '../context';
import React, { useEffect, useMemo } from "react";
import "./../App.css";
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import EditIcon from '@mui/icons-material/Edit';
import { Button, Grid } from '@mui/material';
import { Link, useParams, useNavigate } from 'react-router-dom';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import AddIcon from "@mui/icons-material/Add"
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import { useState } from 'react';

const LJDetails = () => {
  const {setPath, userDetails} = useGlobalContext()
  const [courses,setCourses] = useState(null)
  const [ljs, setLJs] = useState(null)
  const {id, sid} = useParams()
  const navigate = useNavigate()
  useEffect(()=>setPath("Learning Journey"),[])


  useEffect(()=>{
    fetch(`http://127.0.0.1:5002/viewCoursesByLearningJourney?staff_id=${sid}&lj_id=${id}`)
    .then(res=> {return res.json()})
    .then(data => {
      setCourses(data.courses);
      console.log(data)
    });

    fetch(`http://127.0.0.1:5002/viewlearningjourneys?staff_id=${sid}`)
    .then(res=> {return res.json()})
    .then(data => {
      setLJs(data.data);
      console.log(data.data)
    });
  },[sid])

  function toDelete(cid,id){
    console.log(cid,id)
    fetch(`http://127.0.0.1:5002/removecourses`,{
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        course:cid,
        lj_id:id
      })
    }).then(response => {
      navigate(`/learningjourneys`)
      window.location.reload(false);
    })
  }

    return (
      <div style={{display: 'flex', justifyContent: "center"}} >
        <div className="app-container" style={{display: 'flex',justifyContent:"center"}}>
          <div style={{display: 'flex', justifyContent: "center"}}>
            <h3>{ljs && ljs[id]?.title}</h3>
          </div>
          <div style={{display: 'flex', justifyContent: "center"}}>
          <h4>Role related: {ljs && ljs[id]?.role_name}</h4>
          </div>
          <TableContainer component={Paper}>
          <Table sx={{ minWidth: 640, "& td": { border: 0 }}} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Course Code</TableCell>
                <TableCell>Course Name</TableCell>
                <TableCell>Status</TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {courses && Object.keys(courses).map((cid) => (
              <TableRow key={cid} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                <TableCell>
                  {cid}
                </TableCell>
                <TableCell>
                  {courses[cid]["course_name"]}
                </TableCell>
                <TableCell>
                  {courses[cid]["completion_status"]?courses[cid]["completion_status"]:"Not Registered"}
                </TableCell>
                {(window.location.href.indexOf('team')>-1)?<></>:<TableCell>
                <IconButton aria-label="delete" style={{color:"#5289B5"}} onClick={()=>toDelete(cid,id)}>
                  <DeleteOutlinedIcon/>
              </IconButton>
                </TableCell>}
            </TableRow>
          ))}
          </TableBody>
        </Table>
          </TableContainer>
          
        </div>
      </div>
    );
  };
  

export default LJDetails