import { Box, Button, Checkbox, Chip, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, Grid, ListItem, ListItemButton, ListItemText, TextField } from '@mui/material'
import { Stack } from '@mui/system'
import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useGlobalContext } from '../context'

const Modal = ({skill_code})=>{
    const { ljCourses, setljCourses} = useGlobalContext()

    var x = []
    if (ljCourses !== {}){
      Object.keys(ljCourses).map((key, index) => {
        if(key == skill_code){
          x = ljCourses[key]
        }
        })
    }

    const [checked, setChecked] = React.useState(x);
    const [infoChecked, setInfoChecked] = React.useState(x);

    const handleToggle = (value) => () => {
        const currentIndex = checked.indexOf(value);
        const newChecked = [...checked];
    
        if (currentIndex === -1) {
          newChecked.push(value);
        } else {
          newChecked.splice(currentIndex, 1);
        }
        setChecked(newChecked);
      };

    const viewSkillCoursesUrl = 'http://127.0.0.1:5002/viewCourses?skill_code='
    const [relatedCourses, setRelatedCourses] = useState([]);
    const getTeamMembers = async () => {
        const { data } = await axios.get(`${viewSkillCoursesUrl}${skill_code}`);
        setRelatedCourses(data.data);
    };
    useEffect(() => {
        getTeamMembers();
    }, []);


    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const temp = [];
        temp[skill_code] = checked;
        const finalResult = Object.assign(ljCourses, temp)
        setljCourses(finalResult)
        setOpen(false);
        setInfoChecked(checked);
     };

    return (
      <div>
         <Infobox ljCourses={ljCourses} infoChecked={infoChecked}/>
        <Button variant="contained" style={{backgroundColor:"#5289B5"}}  onClick={handleClickOpen}>
          Add related courses
        </Button>
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>Choose courses to add</DialogTitle>
          <DialogContent>
           {relatedCourses?.map((course) => {
                const labelId = `checkbox-list-secondary-label-${course.course_id}`;
                return (  
                    <ListItem
                    key={course.course_id}
                    secondaryAction={
                      <Checkbox
                        edge="end"
                        onChange={handleToggle(course.course_id)}
                        checked={checked.indexOf(course.course_id) !== -1}
                        inputProps={{ 'aria-labelledby': labelId }}
                      />
                    }
                    disablePadding
                  >
                    <ListItemButton>
                      <ListItemText id={labelId} primary={`${course.course_id} : ${course.course_name}`} />
                    </ListItemButton>
                  </ListItem>

                );
              })}
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleSubmit(e)}>Add Courses</Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }

  const Infobox = ({infoChecked}) => {
    var c = [];

    infoChecked.map((x) => {
      c.push(x)
    })
    

        return (
          <Grid container rowSpacing={1} sx={{ mt: 2 }} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>

          {c.length > 0 && <> Added Courses: &nbsp; &nbsp; &nbsp;   </>}
          
            {c.map((x) => 
              <Stack
              direction="row"
              divider={<Divider orientation="vertical" flexItem />}
              spacing={2}
              sx={{margin:1}}
            >
      
                <Chip label={x} />
            </Stack>     
            
                          
            )}
            </Grid>
          );
  }




const LJskills = () => {
    const { relatedSkills} = useGlobalContext()

  return (
    <div > 
         <div className="app-container">
         {/* <Infobox ljCourses={ljCourses}/> */}
          {(Object.keys(relatedSkills).length!==0) ? (
            <table>
            <thead>
              <tr>
                <th>Skill Name</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {Object.keys(relatedSkills)?.map((skill_code) => (
              <tr key={skill_code}>
                {relatedSkills[skill_code].deleted === 'no' && (
                  <>
                  <td>
                      {relatedSkills[skill_code].skill_name}
                  </td>
                  <td>
                  
                  <Modal skill_code={skill_code} />
                  </td>
                </>
                )}
              </tr>
            ))}
            </tbody>
          </table>
          ) : (
            <div>No skills available</div>
          )}
        </div>
      </div>
  )
}

export default LJskills