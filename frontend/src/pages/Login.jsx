import React, { useEffect } from 'react'
import { useGlobalContext } from '../context'

import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

const Login = () => {
  const {setPath, userRole, setUserRole} = useGlobalContext()
  useEffect(()=>setPath("Login"),[])

  const handleChange = (event) => {
    setUserRole(event.target.value);
    localStorage.setItem("userRole", event.target.value)
  };

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
        <InputLabel id="demo-simple-select-label">Login As</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={userRole}
          label="Login As"
          onChange={handleChange}
        >
          <MenuItem value={1}>Admin</MenuItem>
          <MenuItem value={2}>User</MenuItem>
          <MenuItem value={3}>Manager</MenuItem>
        </Select>
      </FormControl>
    </Box>
  )
}

export default Login