import "./../App.css";
import { Button, CardActionArea, IconButton } from '@mui/material'
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
import AlertDialog from "../components/DeleteConfirmation"


//{skillcode:[courses]}
var toUpdateCourses = {}
var coursesList = []

const EditLJ = () =>{
    const viewCoursesByLJ = 'http://127.0.0.1:5002/viewCoursesByLearningJourney?'
    const {id,title,sid} = useParams()
    const navigate = useNavigate()
    
    const titleRef = useRef(null);
    const [lj_courses, setLjCourses] = useState(null)

    React.useEffect(() => {
        let isMounted = true;
        const fetchData = async () => {
            try {
                const response = await axios(`${viewCoursesByLJ}lj_id=${id}&staff_id=${sid}`)
                  if (isMounted) {
                    setLjCourses(response.data)
                    console.log(response.data)
                  }
            } catch (error) {
                console.log(error)
            }
        }
        fetchData()
        return () => (isMounted = false);
      }, [])

    const handleUpdateSubmit = (e) => {
        e.preventDefault();
        // to edit use edit learing journey
        // navigate(`/Roles`);
    };

    function refreshPage() {
        navigate(`/learningjourneys`)
        window.location.reload(false);
    }

    return(
        <></>
    )
}

export default EditLJ