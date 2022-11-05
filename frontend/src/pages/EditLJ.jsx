import "./../App.css";
import { Button, CardActionArea, IconButton } from '@mui/material'
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import AddIcon from "@mui/icons-material/Add"
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import React, {useEffect, useState, useRef} from 'react'
import axios from 'axios';
import { useGlobalContext } from '../context';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom'
import Grid from "@mui/material/Grid"
import {Card} from "@mui/material"
import { Typography } from '@mui/material';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import ReadMoreOutlinedIcon from '@mui/icons-material/ReadMoreOutlined';
import { Box } from '@mui/material';


//{skillcode:[courses]}
var toUpdateCourses = {}
var coursesList = []

function ShowCourse(){
    const {show,setShow,courses,ljCourses}= useGlobalContext()
    const handleClose = () => {
        setShow(false);
      };

      const handleAdd = () =>{
        setShow(false)
        console.log("courses",coursesList)
      };
      useEffect(()=>{

      },[])
      return (
          <Dialog
              open={show}
              onClose={handleClose}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
          >
              <DialogTitle id="alert-dialog-title">{"Add Courses"}</DialogTitle>
              <DialogContent>
                  <DialogContentText id="alert-dialog-description">
                      select courses..
                  </DialogContentText>
                  <FormGroup>
                      {courses?.length!==0?courses?.map((c)=>(
                      Object.keys(ljCourses.courses).includes(c.course_id)?<FormControlLabel disabled control={<Checkbox defaultChecked/>} label={c.course_name} />:<FormControlLabel control={<Checkbox/>} label={c.course_name} />
                      )):<>No courses available.</>}
                  </FormGroup>
              </DialogContent>
              <DialogActions>
                  <Button onClick={handleClose} color="primary">
                      Cancel
                  </Button>
                  <Button onClick={handleAdd} color="primary" autoFocus>
                      Add Courses
                  </Button>
              </DialogActions>
          </Dialog>
    );
}

const EditLJ = () =>{
    const viewCoursesByLJ = 'http://127.0.0.1:5002/viewCoursesByLearningJourney?'
    const {id,title,sid,rid} = useParams()
    const {relatedSkills, setRoleId, setShow, setSkillCode, setljCourses} = useGlobalContext()
   
    const navigate = useNavigate()
    
    const titleRef = useRef(null);
    const [lj_courses, setLjCourses] = useState(null)

    useEffect(() => {
        if (rid) {
            setRoleId(rid)
        } else {
            setRoleId(0)
        }
    }, [])


    function handleView(e,skill_code){
        console.log(skill_code)
        setSkillCode(skill_code)
        setShow(true)
    }
    React.useEffect(() => {
        let isMounted = true;
        const fetchData = async () => {
            try {
                const response = await axios(`${viewCoursesByLJ}lj_id=${id}&staff_id=${sid}`)
                  if (isMounted) {
                    setLjCourses(response.data)
                    setljCourses(response.data)
                    console.log(response.data)
                  }
            } catch (error) {
                console.log(error)
            }
        }
        fetchData()
        return () => (isMounted = false);
      }, [sid, id])

    const handleUpdateSubmit = (e) => {
        e.preventDefault();
        // to edit use edit learing journey
        // navigate(`/Roles`);
    };

    function refreshPage() {
        navigate(`/learningjourneys`)
        window.location.reload(false);
    }
    console.log("testing")
    return(
        <>
        <h2>{title}</h2>
        <h4>Courses in this learning journey</h4>
        <div>{lj_courses!==null && Object.values(lj_courses.courses).map((c)=>(<p>{c.course_name}</p>))}</div>
        <hr/>
        <h5>Selects Course(s) to add...</h5>
        {relatedSkills!==null && Object.values(relatedSkills).map((skill)=>(
            <div>
                <h3>{skill.skill_name}</h3>
                <Grid item sx={{display:"flex", alignItems:"center"}}>
      <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleView(e,skill.skill_code)}>View Course</Button>
      </Grid>
            </div>
        ))}
        <ShowCourse/>
        </>
    )
}

export default EditLJ