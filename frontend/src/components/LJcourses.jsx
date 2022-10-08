import { Button } from '@mui/material'
import React from 'react'
import { useGlobalContext } from '../context'

const LJcourses = () => {
    const {skillCode, courses, addCourses, setAddCourses} = useGlobalContext()
    console.log(courses.data)

    const handleCourse = (e, course_id, course_name) => {
      e.preventDefault();
      setAddCourses(current => [...current, {course_id, course_name}])
    };

  return (
    <>
        <div>LJcourses</div>
        {/* <div>{courses?.data}</div> */}
        <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Description</th>
                <th>Id</th>
                <th>Name</th>
                <th>Status</th>
                <th>Type</th>
                <th></th>
          
              </tr>
            </thead>
            <tbody>
            {courses?.data.map((course) => (
              <tr>
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
                  {course.course_status}
                </td>
                <td>
                  {course.course_type}
                </td>
                <td>
              <Button variant="contained" onClick={(e) => handleCourse(e, course.course_id, course.course_name)}>Add</Button>
              </td>
              </tr>
            ))}
            </tbody>
          </table>
    </>
    
  )
}

export default LJcourses