import { useGlobalContext } from '../context';
import React, {useEffect, useState} from "react";
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
import { Pagination } from '@mui/material';

const Courses = () => {
  const {setPath, userRole} = useGlobalContext()
  useEffect(()=>setPath("Courses"))
  const {allCourses} = useGlobalContext()
  var width = 500;
  var marginTop = 0;
  if (userRole == 1) {
    width = 640;
    marginTop = 80;
  }

    function sliceIntoChunks(arr, chunkSize) {
      const res = [];
      for (let i = 0; i < arr.length; i += chunkSize) {
          const chunk = arr.slice(i, i + chunkSize);
          res.push(chunk);
      }
      return res;
    }

    const [page, setPage] = useState(1);

    const courses_chunks = sliceIntoChunks(allCourses, 20)

    const handleChange = (event, value) => {
      setPage(value);
    };

    return (
        <div style={{display: 'flex', marginTop: marginTop, justifyContent: "center"}} >
           <div className="app-container">
           <Pagination count={courses_chunks.length} page={page} onChange={handleChange} />
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
                {courses_chunks[page-1]?.map((course) => (
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
                        <Link to={`/course/${course.course_id}`} style={{textDecoration:"none"}}> 
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