import "./../App.css";
import { Button, CardActionArea, IconButton } from '@mui/material'
import AddIcon from "@mui/icons-material/Add"
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import React, {useEffect, useState} from 'react'
import { useGlobalContext } from '../context';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom'
import Grid from "@mui/material/Grid"
import {Card} from "@mui/material"
import { Typography } from '@mui/material';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import ReadMoreOutlinedIcon from '@mui/icons-material/ReadMoreOutlined';
import { Box } from '@mui/material';
import AlertDialog from "../components/DeleteConfirmation"





const Cards = ({ljs,staff})=>{
  console.log("staff is", staff)
  const {setOpen, setLid, setLTitle} = useGlobalContext()
  const navigate = useNavigate()
  const deleteLJ = (id,title) =>{
    console.log("deleting in progress")
    setLTitle(title)
    setLid(id)
    setOpen(true)
  }
  const toEditF = (id,sid) => {
    console.log("your sid: ", sid)
    navigate(`/learningjourneys/team/${sid}`)
  }

  return (<>{Object.keys(ljs).map((lj_id)=>(
    <Grid item xs={6} sm={6} md={4} key={lj_id}>
      <Card variant="outlined">
  <React.Fragment>
    <CardContent>
      {(window.location.href.indexOf('team')>-1)?<></>:<Box display="flex" justifyContent="flex-end" alignItems={"flex-end"}>
      <IconButton href={`/learningjourney/${lj_id}/${staff}`} style={{borderColor:"#5289B5"}}><ReadMoreOutlinedIcon/></IconButton>
      </Box>}
      
      <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
        Role related: {ljs[lj_id].role_name}
      </Typography>
      <Typography variant="h5" component="div">
      {ljs[lj_id].title}
      </Typography>
      <Typography variant="body2" >
        Completed {ljs[lj_id].progress}%
      </Typography>
    </CardContent>
    <Grid justifyContent="center" margin="auto" display="flex" alignItems="center">
    {(window.location.href.indexOf('team')>-1)?<></>:<CardActions style={{marginBottom:10}}>
    <Button onClick={()=>toEditF(lj_id,"150166")} style={{color:"#5289B5", borderColor:"#5289B5"}} size="small" variant="outlined" startIcon={<EditIcon />}>
      Edit
    </Button>
    <Button onClick={()=>deleteLJ(lj_id,ljs[lj_id].title)} style={{backgroundColor:"#5289B5"}} size="small" variant="contained" startIcon={<DeleteIcon />}>
      Delete
    </Button>
    </CardActions>}
    </Grid>
  </React.Fragment>
  </Card>
  <AlertDialog/>
  </Grid>
  ))}
  </>
  )
}


const LearningJourneys = () => {

  const {setPath, userDetails} = useGlobalContext()
  const {staff_id} = useParams()
  useEffect(()=>setPath("Learning Journeys"),[])
  const [ljs, setLJs] = useState(null);
  var sid = (window.location.href.indexOf('team')>-1)?staff_id:userDetails.staff_id;
  console.log("sid",sid)
  // if(window.location.href.indexOf('team')>-1){
  //   sid = staff_id
  // }else{
  //   sid = userDetails.staff_id
  // }
  useEffect(()=>{
    
    fetch(`http://127.0.0.1:5002/viewlearningjourneys?staff_id=${sid}`)
    .then(res=> {return res.json()})
    .then(data => {
      setLJs(data.data);
      console.log(data.data)
    });
  },[sid])

  
  return (
    <div>
      <div style={{display: 'flex',  marginBottom:"20px",justifyContent: "center"}} >
        {(window.location.href.indexOf('team')>-1)?<h3>Created by: user #{sid}</h3>:<Link style={{textDecoration:"none"}} to={`/createlearningjourney`}> 
         <Button variant="contained" style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>}>New Learning Journey</Button>
        </Link>}
      </div>
      <Grid className='Font App' container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        {ljs && <Cards ljs={ljs} staff={sid}/>}
      </Grid>
    
    </div> 
  )
}

export default LearningJourneys