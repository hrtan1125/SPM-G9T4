import { Button, TextField, Grid, Chip } from '@mui/material';
import { useEffect } from 'react';
import {React,} from 'react'
import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

var count=0;
var toUpdateSkills = [];
var toDeleteSkills = [];

const CreateEditRole = () =>{

  const { relatedSkills, setRoleId, updateRole, skills, setPath } = useGlobalContext()
  useEffect(()=>setPath("Roles"),[])
  console.log(count++,"runs")

    let navigate = useNavigate();
    const {role_id, role_name} = useParams()
    useEffect(()=>{
      if (role_id){
        setRoleId(role_id) 
      }else{
        setRoleId(0)
      }
    },[])
    
    const [roleName, setRoleName] = useState(role_name)

    function handleChange(event) {
        setRoleName(event.target.value)
    }

    const handleUpdateSubmit = (e) => {
      e.preventDefault();
      updateRole({
        "role_id": role_id,
        "role_name": roleName
      });
      // navigate(`/Roles`);
    };

    console.log(role_id)


function refreshPage() {
  window.location.reload(false);
  navigate(`/${role_id}/${roleName}`)
}

function handleUpdate(e,key){
  if(Object.keys(relatedSkills).includes(key)){
    if (toDeleteSkills.includes(key)){
      let idx = toDeleteSkills.indexOf(key)
      toDeleteSkills.splice(idx,1);
      e.currentTarget.style.backgroundColor="#e6e6e6";
      e.currentTarget.style.border="0px";
    }else{
      toDeleteSkills.push(key);
      e.currentTarget.style.backgroundColor="#ffffff";
      e.currentTarget.style.border="1px solid #bfbfbf";
    }
  }else{
    if(toUpdateSkills.includes(key)){
      let idx = toUpdateSkills.indexOf(key)
      toUpdateSkills.splice(idx,1);
      e.currentTarget.style.backgroundColor="#ffffff";
      e.currentTarget.style.border="1px solid #bfbfbf";
    }else{
      toUpdateSkills.push(key);
      e.currentTarget.style.backgroundColor="#e6e6e6";
      e.currentTarget.style.border="0px";
    }
  }
  console.log("these will be updated",toUpdateSkills)
  console.log("these will be deleted",toDeleteSkills)
}

const createNewRole=async(roleName,skillsToAssign)=>{
  console.log("Creating new Role")
  fetch('http://127.0.0.1:5001/create',{
    method:"POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "role_name":roleName,
      "skills":skillsToAssign
    })
  }).then(res => {
    res.json();
    setRoleId(0)
    toUpdateSkills=[]
    navigate('/Roles')
  })
}

const handleSubmit = (e) => {
  e.preventDefault();
  console.log("Event is", e.target.textContent)
  if(e.target.textContent==="Create"){
    if (!roleName){
      alert("Role Name cannot be empty")
    }else if (toUpdateSkills.length === 0){
      alert("Please select at least one skill")
    }else{
      createNewRole(roleName,toUpdateSkills)
    }
    
    
  }else{
    if (toDeleteSkills.length !== 0) {
      if(toUpdateSkills.length===0 && (toDeleteSkills.length === Object.keys(relatedSkills).length)){
        alert("Deletion Failed! A role should have at least one skill!")
      }else{
        console.log("these are to be deleted", toDeleteSkills)
      //function here
      }
    }

    if (toUpdateSkills.length !== 0) {
      console.log("these are to be updated", toUpdateSkills)
      assignSkillsToRole(role_id, toUpdateSkills)
    }

    if (roleName !== role_name) {
      console.log("Role Name has been changed to", roleName)
      handleUpdateSubmit(e)
      refreshPage();
    }
  }
  
};

const assignSkillsToRole = async(role_id, skill_code) => {
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({role_id, skill_code})
  };
  fetch("http://127.0.0.1:5001/assignSkills", requestOptions)
    .then(response => {
      response.json();
      setRoleId(0)
      toUpdateSkills=[]
      refreshPage();
    })

} catch (error) {
    console.log(error.response)
}
};

const deleteSkillsFromRole = async(role_id, skill_code) => {
  try {
    const requestOptions = {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({role_id, skill_code})
  };
  fetch("http://127.0.0.1:5001/assignSkills", requestOptions)
    .then(response => {
      response.json();
      setRoleId(0)
      refreshPage();
    })

} catch (error) {
    console.log(error.response)
}
}

  return (
    <>
    <Grid container spacing={2} >
      <Grid item sx={{display:"flex", alignItems:"center"}}> 
      Role Name:   &nbsp;
        <TextField size="small" id="outlined-basic"  variant="outlined" value={roleName} onChange={handleChange}/>  
      </Grid>
      <Grid item sx={{display:"flex", alignItems:"center"}}>
      <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleSubmit(e)}>{role_id?"Edit":"Create"}</Button>
      </Grid>
    </Grid>
    <Grid item sx={{display:"flex", alignItems:"center", marginTop:3}}> 
    Selects skills to add....  
    </Grid>
    <Grid container spacing={2} marginTop={1}>
{(Object.keys(relatedSkills).length!==0 || typeof(role_id)==="undefined") && skills.length!==0  && skills.map((skill)=>(
  <Chip key={skill.skill_code} label={skill.skill_name} sx={{margin:1}} onClick={(e)=>handleUpdate(e,skill.skill_code)} variant={Object.keys(relatedSkills).includes(skill.skill_code)?"filled":"outlined"}/>))}
  </Grid>
  </>
  )
}

export default CreateEditRole