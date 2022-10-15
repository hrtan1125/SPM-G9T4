import "./../App.css";
import { Button } from '@mui/material'
import AddIcon from "@mui/icons-material/Add"
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import React, {useEffect} from 'react'
import { useGlobalContext } from '../context';
import { Link } from 'react-router-dom'
import Grid from "@mui/material/Grid"
import {Card} from "@mui/material"
import { Typography } from '@mui/material';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import { Box } from '@mui/material';

//get from view all learning journeys
const ljs = [
  {lj_id:1,lj_title:"My Learning Journey 1", role_id:"Engineer"},
  {lj_id:2,lj_title:"My Learning Journey 2", role_id:"CEO"},
  {lj_id:3,lj_title:"My Learning Journey 3", role_id:"CTO"},
  {lj_id:4,lj_title:"My Learning Journey 4", role_id:"Software Engineer"},
  {lj_id:5,lj_title:"My Learning Journey 5", role_id:"Financial Advisor"}
]

const cards = (
  ljs.map((lj)=>(<React.Fragment>
    <CardContent>
      <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
        Role related: {lj.role_id}
      </Typography>
      <Typography variant="h5" component="div">
      {lj.lj_title}
      </Typography>
      <Typography variant="body2" >
        on-going
      </Typography>
    </CardContent>
    <Grid justifyContent="center" margin="auto" display="flex" alignItems="center">
    <CardActions >
    <Button style={{color:"#5289B5", borderColor:"#5289B5"}} size="small" variant="outlined" startIcon={<EditIcon />}>
      Edit
    </Button>
    <Button style={{backgroundColor:"#5289B5"}} size="small" variant="contained" startIcon={<DeleteIcon />}>
      Delete
    </Button>
    </CardActions>
    </Grid>
  </React.Fragment>))
);

// const card = (
//   <React.Fragment>
//     <CardContent>
//       <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
//         Word of the Day
//       </Typography>
//       <Typography variant="h5" component="div">
//         LJ01
//       </Typography>
//       <Typography sx={{ mb: 1.5 }} color="text.secondary">
//         adjective
//       </Typography>
//       <Typography variant="body2">
//         well meaning and kindly.
//         <br />
//         {'"a benevolent smile"'}
//       </Typography>
//     </CardContent>
//     <CardActions>
//       <Button size="small">Learn More</Button>
//     </CardActions>
//   </React.Fragment>
// );

const LearningJourneys = () => {
  const {setPath} = useGlobalContext()
  useEffect(()=>setPath("Learning Journeys"))
  return (
    <div>
      <div style={{display: 'flex',  marginBottom:"20px",justifyContent: "center"}} >
        <Link style={{textDecoration:"none"}} to={`/createlearningjourney`}> 
         <Button variant="contained" style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>}>New Learning Journey</Button>
        </Link>
      </div>
      <Grid className='Font App' container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        {cards.map((card,index) => (
        <Grid item xs={2} sm={4} md={4} key={index}>
          <Card variant="outlined">{card}</Card>
        </Grid>
        ))}
      </Grid>
    
    </div> 
  )
}

export default LearningJourneys