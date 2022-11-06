import { Button, TextField, Grid, Chip } from '@mui/material';
import { useEffect } from 'react';
import {React, createRef} from 'react'
import { useState, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

var count=0;
var toUpdateSkills = [];
var toDeleteSkills = [];

const CreateEditRole = () =>{
  const updateRoleUrl = 'http://127.0.0.1:5001/updaterole'
  const { relatedSkills, setRoleId, skills, setPath } = useGlobalContext()
  const roleRef = useRef(null);
  const [status, setStatus] = useState(null)
  const [res, setRes] = useState(null)
  const [refresh,setRefresh]=useState({rname:false,radd:false,rdelete:false})

  useEffect(()=>{
    if(status===400 && res!==null){
      alert(res)
      setRes(null)
      if(refresh.rname){
        refreshPage();
      }
    }
  },[res])

  useEffect(()=>{
    console.log(refresh.rname,refresh.radd,refresh.rdelete)
    if(refresh.rname && refresh.radd && refresh.rdelete && status!==400){
      setRoleId(0)
      toUpdateSkills=[]
      toDeleteSkills=[]
      setRefresh(prv =>{
        return {
          ...prv,
          rname:false,
          radd:false,
          rdelete:false
        }
      })
      refreshPage();
    }
  },[status,res])

  useEffect(()=>setPath("Roles"),[])

    let navigate = useNavigate();
    const {role_id, role_name} = useParams()
    useEffect(()=>{
      if (role_id){
        setRoleId(role_id) 
      }else{
        setRoleId(0)
      }
    },[])
    
    const updateRole = async(formData) => {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      };
      fetch(updateRoleUrl, requestOptions)
        .then(response => {
          if(response.status!==400){
            setRefresh(prv =>{
              return {
                ...prv,
                rname:true
              }
            })
          }
          setStatus(response.status)
          return response.json()
        }).then(data=>{
          setRes(data.message)
        })
    } catch (error) {
        console.log(error.response)
    }
    }

    const handleUpdateSubmit = (e) => {
      e.preventDefault();
      updateRole({
        "role_id": role_id,
        "role_name": roleRef.current.value
      });
      
    };


function refreshPage() {
  navigate(`/role/${role_id}/${roleRef.current.value}`)
  window.location.reload(false);
}

//handle any updates on click
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

//submit new role to database
const createNewRole=async(roleName,skillsToAssign)=>{
  console.log("Creating new Role")
  fetch('http://127.0.0.1:5001/createrole',{
    method:"POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "role_name":roleName,
      "skills":skillsToAssign
    })
  }).then(res => {
    setStatus(res.status)
    setRefresh(prv =>{
      return {
        ...prv,
        rname:true
      }
    })
    return res.json();
    
  }).then(data => {
    if(data["message"]!==undefined){
      setRes(data.message)
    }else{
      setRoleId(0)
      toUpdateSkills=[]
      navigate('/Roles')
    }
  })
}

const handleSubmit = (e) => {
  e.preventDefault();
  console.log("Event is", e.target.textContent)
  if(e.target.textContent==="Create"){
    let val = roleRef.current.value.trim()
    if (!val){
      alert("Role Name cannot be empty!")
    }else if(!/^[A-Za-z ]*$/.test(roleRef.current.value)){
      alert("Invalid role name!Only alphabets and spaces allowed!")
    }else if (toUpdateSkills.length === 0){
      alert("Please select at least one skill")
    }else{
      createNewRole(roleRef.current.value,toUpdateSkills)
    }
  }else{
    if (toDeleteSkills.length !== 0) {
      if(toUpdateSkills.length===0 && (toDeleteSkills.length === Object.keys(relatedSkills).length)){
        alert("Deletion Failed! A role should have at least one skill!")
      }else{
        console.log("these are to be deleted", toDeleteSkills)
      //function here
      deleteSkillsFromRole(role_id,toDeleteSkills)
      }
    }else{
      setRefresh(prv =>{
        return {
          ...prv,
          rdelete:true
        }
      })
    }

    if (toUpdateSkills.length !== 0) {
      console.log("these are to be updated", toUpdateSkills)
      assignSkillsToRole(role_id, toUpdateSkills)
    }else{
      setRefresh(prv =>{
        return {
          ...prv,
          radd:true
        }
      })
    }
    let val = roleRef.current.value.trim()
    if (!val){
      alert("Role Name cannot be empty!")
    }else if(!/^[A-Za-z ]*$/.test(roleRef.current.value)){
      alert("Invalid role name!Only alphabets and spaces allowed!")
    }else if (val !== role_name) {
      console.log("Role Name will be changed to", val)
      handleUpdateSubmit(e)
    }else{
      setRefresh(prv =>{
        return {
          ...prv,
          rname:true
        }
      })
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
      toUpdateSkills=[]
      setStatus(response.status)
      if(response.status!==400){
        toUpdateSkills=[]
      }
      setRefresh(prv =>{
        return {
          ...prv,
          radd:true
        }
      })
      return response.json();
    }).then(data=>{
      setRes(data.message)
    })

} catch (error) {
    console.log(error.response)
}
};

  const deleteSkillsFromRole = async (role_id, skill_code) => {
    try {
      fetch("http://127.0.0.1:5001/removeSkills", {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role_id, skill_code })
      })
        .then(response => {
          setStatus(response.status)
          setRefresh(prv =>{
            return {
              ...prv,
              rdelete:true
            }
          })
          if(response.status!==400){
           
            toDeleteSkills=[]
          }
          return response.json();
        }).then(data=>{
          setRes(data.message)
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
        <TextField size="small" id="outlined-basic" style={{width:"400px"}} variant="outlined" defaultValue={role_name} inputRef={roleRef}/>  
      </Grid>
      <Grid item sx={{display:"flex", alignItems:"center"}}>
      <Button style={{backgroundColor:"#5289B5"}} variant="contained" onClick={(e) => handleSubmit(e)}>{role_id?"Edit":"Create"}</Button>
      </Grid>
    </Grid>
    <Grid item sx={{display:"flex", alignItems:"center", marginTop:3}}> 
    Selects skills to add....  
    </Grid>
    <Grid container spacing={2} marginTop={1}>
{skills.length!==0  && skills.map((skill)=>(
  <Chip key={skill.skill_code} label={skill.skill_name} sx={{margin:1}} onClick={(e)=>handleUpdate(e,skill.skill_code)} variant={Object.keys(relatedSkills).includes(skill.skill_code)?"filled":"outlined"}/>))}
  </Grid>
  </>
  )
}

export default CreateEditRole