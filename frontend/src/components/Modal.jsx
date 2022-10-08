import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import axios from 'axios';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';

export default function Modal({role_name}) {
    const { closeModal, skillCode, courses, ljCourses, setljCourses } = useGlobalContext()
  let navigate = useNavigate();

  // const {role_id, setRoles, roles, fetchRoles} = useGlobalContext()
  const [checked, setChecked] = React.useState([]);

  const transformed_courses = [];

  console.log(courses, "COURSES")

  courses?.map((course) => {
    return (
      <>
          {transformed_courses.push(`${course.course_id} - ${course.course_name}` )}
      </>
        
    )
  })

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

  console.log(checked, "hahhahah")


  // const testdata = ["a - hello", "b - hihi", "c - kikik"]
  console.log(transformed_courses, "dammmm")

  const handleSubmit = (e) => {
    e.preventDefault();
    closeModal()
    const courses_codes_list = [];
    checked.map((skill) => {
        courses_codes_list.push(skill.split(" - ")[0])
    })
    console.log(courses_codes_list, "IIIII")
    const transformed_courses = [];
    transformed_courses[skillCode] = courses_codes_list
    console.log(transformed_courses, "TRANSFORMERS")
    const finalResult = Object.assign(ljCourses, transformed_courses)
    console.log(finalResult, "HAHHAHA")
    setljCourses(finalResult)
 };

  return (
    <>
    <List dense sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
        {transformed_courses === [] ? (
            <div>There is no course related to this skill </div>
        ) : (
            <div>
                <h1>Select your courses</h1>
                {transformed_courses.map((value) => {
                const labelId = `checkbox-list-secondary-label-${value}`;
                return (
                  <ListItem
                    key={value}
                    secondaryAction={
                      <Checkbox
                        edge="end"
                        onChange={handleToggle(value)}
                        checked={checked.indexOf(value) !== -1}
                        inputProps={{ 'aria-labelledby': labelId }}
                      />
                    }
                    disablePadding
                  >
                    <ListItemButton>
                      <ListItemText id={labelId} primary={`${value}`} />
                    </ListItemButton>
                  </ListItem>
                );
              })}
            </div>
            
        )}
      
    </List>
    {/* <Button variant="contained" color="error" onClick={closeModal}>Close</Button> */}
    <Button variant="contained" onClick={(e) => handleSubmit(e)}>Add Courses</Button>
    </>
  );
}
