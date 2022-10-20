import { Button, TextField, Grid, Chip } from '@mui/material';
import { margin } from '@mui/system';
import axios from 'axios';
import { useEffect } from 'react';
import {React,useContext} from 'react'
import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';
import ShowSkills from './ShowSkills';

var count=0;
var toUpdateSkills = [];
var toDeleteSkills = [];

const MyVar = ({VariantValue, skills, handleUpdate}) => {
  console.log("final stage", skills.length, Object.keys(VariantValue).length)
  console.log(VariantValue)
  return (
    <div>
    {skills.map((skill)=>(
      <Chip key={skill.skill_code} label={skill.skill_name} sx={{margin:1}} onClick={()=>handleUpdate(skill.skill_code)} variant={VariantValue[skill.skill_code]}/>
    ))}
    
    </div>
  )
}

const MyChip = ({skills,related}) => {
  const [VarValue, setVar] = useState({})
  console.log("my skills", skills)

  const myF = (skill,relatedSkills) =>
    new Promise(resolve => 
      setTimeout(()=>{
        let tempDict = {}
        tempDict[skill.skill_code] = Object.keys(relatedSkills).includes(skill.skill_code)?"contained":"outlined"
        resolve(tempDict)},1000)
      )

  const testF = skills =>
        new Promise(resolve =>
          setTimeout(async()=>{
            let VarValues = {}
            for(let skill of skills){
              let tempDict = await myF(skill,related)
              let cV = VarValues
              VarValues = Object.assign({},cV,tempDict)
            }
            resolve(VarValues)
          }),1000)

  const handleUpdate = async(key) =>{
  if (!toUpdateSkills.includes(key) && (toDeleteSkills.includes(key) || !Object.keys(related).includes(key))){
    if(toDeleteSkills.includes(key)){
      let idx = toDeleteSkills.indexOf(key)
      toDeleteSkills.splice(idx,1);
    }
    
    if(!Object.keys(related).includes(key)){
      toUpdateSkills.push(key);
    }
    
    let updateV = {}
    updateV = {[key]:"contained"}
    setVar(VariantValue=>({
      ...VariantValue,
      ...updateV
    }));
  }else{
    console.log("unassigning the skills")
    if(toUpdateSkills.includes(key)){
      let idx = toUpdateSkills.indexOf(key)
      toUpdateSkills.splice(idx,1);
    }
    
    if(Object.keys(related).includes(key)){
      toDeleteSkills.push(key)
    }
    
    let updateV = {}
  
    updateV = {[key]:"outlined"}
    setVar(VariantValue=>({
      ...VariantValue,
      ...updateV
    }));
  }
  console.log(toUpdateSkills)
  }
  useEffect(()=>{
    const mySkills = async() =>{
      let VarValues = await testF(skills)
      setVar(()=>VarValues)
    }
    mySkills()
  },[])

  return(<>
  {Object.keys(VarValue).length === skills.length && <MyVar VariantValue={VarValue} skills={skills} handleUpdate={handleUpdate}/>}
  </>)
}

const CreateEditRole = () =>{
  const { relatedSkills, setRoleId, updateRole, skills, setPath, role } = useGlobalContext()
  useEffect(()=>setPath("Roles"),[])
  console.log(relatedSkills, "related skills")
  console.log(count++,"runs")
  // let BtnName = ""

    let navigate = useNavigate();
    const {role_id, role_name} = useParams()
    useEffect(()=>{
      if (role_id){
        setRoleId(role_id) 
        setRoleName(role.role_name)
      }else{
        setRoleId(0)
      }
      
    },[role])

    const [roleName, setRoleName] = useState()

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


// const [checked, setChecked] = useState([]);


//remove this
// const handleCheck = (event) => {
//   var updatedList = [...checked];
//   if (event.target.checked) {
//     updatedList = [...checked, event.target.value];
//   } else {
//     updatedList.splice(checked.indexOf(event.target.value), 1);
//   }
//   setChecked(updatedList);
// };


function refreshPage() {
  window.location.reload(false);
  navigate(`/${role_id}/${roleName}`)
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
  if(e.target.textContent=="Create"){
    if (!roleName){
      alert("Role Name cannot be empty")
    }else if (toUpdateSkills.length === 0){
      alert("Please select at least one skill")
    }else{
      createNewRole(roleName,toUpdateSkills)
    }
    
    
  }else{
    if (toDeleteSkills.length !== 0) {
      if(toUpdateSkills.length==0 && (toDeleteSkills.length == Object.keys(relatedSkills).length)){
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

    if (roleName != role_name) {
      console.log("Role Name has been changed to", roleName)
      handleUpdateSubmit(e)
      // refreshPage();
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
{(Object.keys(relatedSkills).length!=0 || typeof(role_id)==="undefined") && skills.length!=0  && <MyChip skills={skills} related={relatedSkills}/>}
  </Grid>
  </>
  )
}

export default CreateEditRole