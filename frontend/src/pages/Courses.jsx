import { useGlobalContext } from '../context';
import React from "react";
import "./../App.css";
import { Button } from '@mui/material';
import { Link } from 'react-router-dom';

const Courses = () => {
  const {allCourses} = useGlobalContext()
    console.log(allCourses, "ALLLL COURSES")
    return (
        <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
           <div className="app-container">

              <table>
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Add Skill</th>
              
                  </tr>
                </thead>
                <tbody>
                {allCourses.map((course) => (
                  <tr key={course.course_id}>
                      <td>
                        {course.course_category}
                      </td>
                      <td>
                        {course.course_desc}
                      </td>
                      <td>
                          {course.course_id}
                      </td>
                      <td>
                        {course.course_name}
                      </td>
                      <td>
                        {course.course_type}
                      </td>
                      <td>
                        <Link to={`/course/${course.course_id}`}>
                            <Button variant="contained">Add Skills</Button>
                        </Link>
                      </td>
                  </tr>
                ))}
                </tbody>
              </table>

        </div>
      </div> 
      );
  };

export default Courses