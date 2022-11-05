import "./../App.css";
import { Button, CardActionArea, IconButton } from '@mui/material'
import AddIcon from "@mui/icons-material/Add"
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import React, {useEffect, useState} from 'react'
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
    const {id,title} = useParams()
    const navigate = useNavigate()
    
    const titleRef = useRef(null);

    const handleUpdateSubmit = (e) => {
        e.preventDefault();
        // to edit use edit learing journey
        updateRole({
          "role_id": id,
          "role_name": titleRef.current.value
        });
        // navigate(`/Roles`);
      };

    function refreshPage() {
        navigate(`/learningjourneys`)
        window.location.reload(false);
    }
}

export default EditLJ