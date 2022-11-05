import "./../App.css";
import { Button } from '@mui/material'
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import React, {useEffect, useState, useRef} from 'react';
import axios from 'axios';
import { useGlobalContext } from '../context';
import { useNavigate, useParams } from 'react-router-dom';
import Grid from "@mui/material/Grid";


function ShowCourse(){
    const {show,setShow,courses,ljCourses,addCourses,setAddCourses,skillCode,setToAddCName,toAddCName}= useGlobalContext()
    const handleClose = () => {
        setShow(false);
      };
      
      const handleToggle = (e,cid,cname) =>{
        console.log(e)
        console.log(skillCode,cid)
        if(Array.isArray(addCourses) && addCourses.length===0){
            // console.log(skillCode,cid)
            let tempDict = {[skillCode]:[cid]}
            console.log(tempDict)
            setAddCourses(tempDict)
            setToAddCName({[cid]:cname})
        }else if(!Object.keys(addCourses).includes(skillCode)){
            // let tempDict = {[skillCode]:[cid]}
            setAddCourses(prvDt =>{
                return {
                    ...prvDt,
                    [skillCode]:[cid]
                }
            })
            setToAddCName(prvCData=>{
                return {
                    ...prvCData,
                    [cid]:cname
                }
            })
        }else if(Object.keys(addCourses).includes(skillCode)){
            let tempList = addCourses[skillCode]
            let copyList = [...tempList]
            if(!copyList.includes(cid)){
                copyList.push(cid)
                setAddCourses(prvDt=>{
                    return {
                        ...prvDt,
                        [skillCode]:copyList
                    }
                })
                setToAddCName(prvCData=>{
                    return {
                        ...prvCData,
                        [cid]:cname
                    }
                })
            }else{
                let idx = copyList.indexOf(cid);
                copyList.splice(idx, 1);
                setAddCourses(prvDt=>{
                    return {
                        ...prvDt,
                        [skillCode]:copyList
                    }
                })
                delete toAddCName[cid]
            }
            console.log(toAddCName)    
        }
        // if(addCourses.length===0||!addCourses.includes(skillCode)){

        //     console.log(cid)
        //     const cs = [...addCourses]
        //     cs.push(cid)
        //     setAddCourses(cs)
        // }else{
        //     const coursesCopy = [...addCourses];
        //     let idx = coursesCopy.indexOf(cid);
        //     coursesCopy.splice(idx, 1);
        //     setAddCourses(coursesCopy)
        // }
      }

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
                      Object.keys(ljCourses.courses).includes(c.course_id)?<FormControlLabel disabled control={<Checkbox defaultChecked/>} 
                      label={c.course_name} />:<FormControlLabel control={<Checkbox onChange={(e)=>handleToggle(e,c.course_id,c.course_name)} checked={toAddCName!==null && Object.keys(toAddCName).includes(c.course_id)}/>} label={c.course_name} />
                      )):<>No courses available.</>}
                  </FormGroup>
              </DialogContent>
              <DialogActions>
                  <Button onClick={handleClose} color="primary">
                      Save & Close
                  </Button>
              </DialogActions>
          </Dialog>
    );
}

const EditLJ = () =>{
    const viewCoursesByLJ = 'http://127.0.0.1:5002/viewCoursesByLearningJourney?'
    const {id,title,sid,rid} = useParams()
    const {relatedSkills, setRoleId, setShow, setSkillCode, setljCourses, addCourses, toAddCName, skillCode,setAddCourses} = useGlobalContext()
   
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
        // console.log(skill_code)
        setSkillCode(skill_code)
        console.log(skillCode)
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

    const handleSubmit = (e) => {
        e.preventDefault();
        // to edit use edit learing journey
        // navigate(`/Roles`);
        fetch('http://127.0.0.1:5002/addlearningjourneycourses',{
    method:"POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "lj_id":id,
      "courses":addCourses
    })
  }).then(res => {
    setAddCourses([])
    refreshPage()
    return res.json();
  })
    };

    function refreshPage() {
        navigate(`/learningjourneys`)
        window.location.reload(false);
    }
    console.log("testing")
    return(
        <>
        <h2>{title}</h2>
            <Button style={{backgroundColor:"#5289B5"}} variant="contained" 
            onClick={(e) => handleSubmit(e)}>Add Courses</Button>
        <hr/>
        <Grid container>
            <Grid item>
                    <h4>Courses in this learning journey</h4>
                    {lj_courses !== null && Object.values(lj_courses.courses).map((c) => (<p>{c.course_name}</p>))}
            </Grid>
            <Grid item xs={1}></Grid>
            <Grid item>
                <h4>Courses to be added</h4>
                {toAddCName!==null && Object.values(toAddCName).map((c)=>(<p>{c}</p>))}
            </Grid>
        </Grid>
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