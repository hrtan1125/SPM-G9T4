import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import { Box, Button } from '@mui/material';
import { useGlobalContext } from '../context';

export default function Modal() {
    const { closeModal, skillCode, courses, ljCourses, setljCourses } = useGlobalContext()

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

  console.log(transformed_courses, "TRANSFORMED COURSES")

  const handleSubmit = (e) => {
    e.preventDefault();
    closeModal()
    const courses_codes_list = [];
    checked.map((skill) => {
        courses_codes_list.push(skill.split(" - ")[0])
    })
    console.log(courses_codes_list, "COURSES CODES LIST")
    const transformed_courses = [];
    transformed_courses[skillCode] = courses_codes_list
    console.log(transformed_courses, "TRANSFORMERS")
    const finalResult = Object.assign(ljCourses, transformed_courses)
    console.log(finalResult, "FINAL RESULT")
    setljCourses(finalResult)
 };

  return (
    <>
    <List dense sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
        {transformed_courses.length === 0 ? (
            <Box sx={{ color: 'warning.main' }}>There is no courses related to this skill </Box>
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
    <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleSubmit(e)}>Add Courses</Button>
    </>
  );
}
