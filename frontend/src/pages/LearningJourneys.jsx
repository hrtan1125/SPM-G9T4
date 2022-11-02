import "./../App.css";
import { Button, CardActionArea, IconButton } from '@mui/material'
import AddIcon from "@mui/icons-material/Add"
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import React, {useEffect, useState} from 'react'
import { useGlobalContext } from '../context';
import { Link } from 'react-router-dom'
import Grid from "@mui/material/Grid"
import {Card} from "@mui/material"
import { Typography } from '@mui/material';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import ReadMoreOutlinedIcon from '@mui/icons-material/ReadMoreOutlined';
import { Box } from '@mui/material';


// const testLJ = () => {

// }
// fetch(`http://127.0.0.1:5002/viewlearningjourneys?staff_id=${130001}`).then(res=>{
//   console.log(res.json())
// }).then(data=>{
//   var ljs = data.data;
// })

// const ljs = 
const toEditF = (id) => {
  console.log("your id: ", id)
}

const viewDetails = (e) =>{
  // e.preventDefault();
  // console.log("view details")
  // console.log(e)
  // navigate(`/learningjourney/${id}`)
  //handle view details of learning journeys
}

const deleteLJ = (id,title) =>{
  console.log("deleting in progress")
  fetch("http://127.0.0.1:5002/removelearningjourney",{
    method:"DELETE",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "lj_id":id,
      "title":title
    })
  }).then(res=>{
    res.json()
    window.location.reload(false);
  })
}

const Cards = ({ljs})=>{
  
  return (<>{Object.keys(ljs).map((lj_id)=>(
    <Grid item xs={6} sm={6} md={4} key={lj_id}>
      <Card variant="outlined">
  <React.Fragment>
    <CardContent>
      <Box display="flex" justifyContent="flex-end" alignItems={"flex-end"}>
      <IconButton href={`/learningjourney/${lj_id}`} style={{borderColor:"#5289B5"}}><ReadMoreOutlinedIcon/></IconButton>
      </Box>
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
    <CardActions style={{marginBottom:10}}>
    <Button onClick={()=>toEditF(lj_id)} style={{color:"#5289B5", borderColor:"#5289B5"}} size="small" variant="outlined" startIcon={<EditIcon />}>
      Edit
    </Button>
    <Button onClick={()=>deleteLJ(lj_id,ljs[lj_id].title)} style={{backgroundColor:"#5289B5"}} size="small" variant="contained" startIcon={<DeleteIcon />}>
      Delete
    </Button>
    </CardActions>
    </Grid>
  </React.Fragment>
  </Card>
  </Grid>
  ))}
  </>
  )
}


const LearningJourneys = () => {
  const {setPath, user} = useGlobalContext()
  useEffect(()=>setPath("Learning Journeys"),[])
  const [ljs, setLJs] = useState(null);

  console.log(user, "LJJJ USER")

  useEffect(()=>{
    fetch(`http://127.0.0.1:5002/viewlearningjourneys?staff_id=${user}`)
    .then(res=> {return res.json()})
    .then(data => {
      setLJs(data.data);
      console.log(data.data)
    });
  },[user])
  
  return (
    <div>
      <div style={{display: 'flex',  marginBottom:"20px",justifyContent: "center"}} >
        <Link style={{textDecoration:"none"}} to={`/createlearningjourney`}> 
         <Button variant="contained" style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>}>New Learning Journey</Button>
        </Link>
      </div>
      <Grid className='Font App' container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        
        {ljs && <Cards ljs={ljs}/>}
      </Grid>
    
    </div> 
  )
}

export default LearningJourneys