import { useGlobalContext } from '../context';
import React, {useEffect} from "react";
import "./../App.css";
import { Link } from 'react-router-dom';
import AddIcon from "@mui/icons-material/Add"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';

const Courses = () => {
  const {setPath, userRole} = useGlobalContext()
  useEffect(()=>setPath("Courses"))
  const {allCourses} = useGlobalContext()
  var width = 500;
  if (userRole == 1) {
    width = 640;
  }
    return (
        <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
           <div className="app-container">

           <TableContainer component={Paper} elevation={3}>
      <Table sx={{ minWidth: width, "& td": { border: 0 }}} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Course ID</TableCell>
            <TableCell align="left">Course Name</TableCell>
            {userRole == 1 && 
            <TableCell align="center"></TableCell>}
          </TableRow>
        </TableHead>
        <TableBody>
          {allCourses?.map((course) => (
            <TableRow
              key={course.course_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="left">
                {course.course_id}
              </TableCell>
              <TableCell align="left">{course.course_name}</TableCell>
              {userRole == 1 && 
              <>
                <TableCell align="center">
                  <div style={{display: 'flex', justifyContent: "center"}} >
                  <Link to={`/course/${course.course_id}/${course.course_name}`} style={{textDecoration:"none"}}> 
                    <Button variant="contained" style={{backgroundColor:"#5289B5"}} startIcon={<AddIcon/>}>Add Skills</Button>
                  </Link>
                  </div>
                </TableCell>
              </>
}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>

        </div>
      </div> 
      );
  };

export default Courses