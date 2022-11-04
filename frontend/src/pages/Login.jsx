import React, { useEffect } from 'react'
import { useGlobalContext } from '../context'

import Box from '@mui/material/Box';

import { Button, TextField } from '@mui/material';
import axios from 'axios';
import { Navigate, useNavigate } from 'react-router-dom';

const Login = () => {
  const {setPath, setUserDetails, userDetails} = useGlobalContext()
  useEffect(()=>setPath("Login"),[])
  useEffect(()=>  setUserDetails({}),[])
  useEffect(()=>  localStorage.setItem("userDetails", JSON.stringify({})),[])
  const navigate = useNavigate()

  console.log("userDetails", userDetails,  typeof userDetails, Object.keys(userDetails).length !== 0)
  const [staffId, setStaffId] = React.useState('');

  const getUserRoleUrl = 'http://127.0.0.1:5002/checkrole?staff_id='

  const handleChange = (event) => {
    setStaffId(event.target.value);
  };

  const handleSubmit = (event) => {
    axios.get(`${getUserRoleUrl}${staffId}`)
    .then(response => {
      // navigate('/learningjourneys')
      localStorage.setItem("userDetails", JSON.stringify(response.data))
      setUserDetails(response.data)
      // window.location.replace("http://localhost:3000/learningjourneys");
      
    })
    .catch(error => {
        console.error('There was an error!', error);   
    });
    navigate('/learningjourneys')
  };


  return (
    <Box sx={{ minWidth: 120 }}>

      <Box
        component="form"
        sx={{
          display: 'flex',
          justifyContent: 'center',
          p: 1,
          m: 1,
          bgcolor: 'background.paper',
          borderRadius: 1,
        }}
        noValidate
        autoComplete="off"
      >

        <TextField
          id="outlined-name"
          label="Input Staff ID"
          value={staffId}
          onChange={handleChange}
        />
      <Button type="submit" variant="contained" style={{backgroundColor:"#5289B5"}} onClick={handleSubmit}>Login</Button>
      
      </Box>
      <li>Admin: 130001</li>
      <li>User: 150166</li>
      <li>Manager: 140001</li>
      <li>With Learning Journey: 150008</li>
       
      
    </Box>
  )
}

export default Login