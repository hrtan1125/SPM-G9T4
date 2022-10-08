
import React, { useState, useContext, useEffect } from 'react'
import axios from 'axios'
const AppContext = React.createContext()
// const viewRoles = 'http://192.168.0.102:5001/view'
const rolesUrl = 'http://192.168.0.102:5001/view'
const skillsUrl = 'http://192.168.0.102:5000/view'
const deleteRoleUrl = 'http://192.168.0.102:5001/delete'
const viewSelectedRoleUrl = 'http://192.168.0.102:5001/viewselectedrole?role_id='
const deleteSkillUrl = 'http://192.168.0.102:5000/delete'
const viewSelectedSkillUrl = "http://192.168.0.102:5000/viewselectedskill?skill_code="

const updateSkillUrl = 'http://192.168.0.102:5000/update'
const createSkillUrl = 'http://192.168.0.102:5000/create'

const updateRoleUrl = 'http://192.168.0.102:5001/update'

const viewSkillsByRoleUrl = 'http://192.168.0.102:5002/viewRoleSkills?role_id='
const viewCoursesBySkillUrl = 'http://192.168.0.102:5002/viewCourses?skill_code='




const AppProvider = ({ children }) => {
    const [roles, setRoles] = useState([])
    const [role, setRole] = useState([])
    const [roleId, setRoleId] = useState('')
    const [skills, setSkills] = useState([])
    const [relatedSkills, setRelatedSkills] = useState([])

    const [skill, setSkill] = useState([])
    const [skillCode, setSkillCode] = useState('')
    // const [showSkills, setShowSkills] = useState(true)
    const [activeStep, setActiveStep] = React.useState(0);
    const [skipped, setSkipped] = React.useState(new Set());

    const [courses, setCourses] = useState([])
    const [addCourses, setAddCourses] = useState([])

    const [showModal, setShowModal] = useState(false)
    const [ljCourses, setljCourses] = useState({})

    const closeModal = () => {
      setShowModal(false)
    }


    const fetchRoles = async(url) => {
        try {
            const {data} = await axios(url)
            setRoles(data.data)
        } catch (error) {
            console.log(error.response)
        }
    }
    const fetchRole = async(url) => {
      try {
          const {data} = await axios(url)
          setRole(data)
      } catch (error) {
          console.log(error.response)
      }
  }

  const fetchRelatedSkills = async(url) => {
    try {
        const {data} = await axios(url)
        setRelatedSkills(data.data)
    } catch (error) {
        console.log(error.response)
    }
}



const fetchRelatedCourses = async(url) => {
  try {
      const {data} = await axios(url)
      setCourses(data.data)
  } catch (error) {
      console.log(error.response)
  }
}
  
  const fetchSkills = async(url) => {
    try {
        const {data} = await axios(url)
        setSkills(data.data)
    } catch (error) {
        console.log(error.response)
    }
}
const fetchSkill = async(url) => {
  try {
      const {data} = await axios(url)
      console.log("fetching skill", data)
      setSkill(data)
      
  } catch (error) {
      console.log(error.response)
  }
}
    useEffect(() => {
        fetchRoles(rolesUrl)
    }, [])
    useEffect(() => {
      fetchSkills(skillsUrl)
  }, [])
    useEffect(() => {
      if (roleId){
        fetchRole(`${viewSelectedRoleUrl}${roleId}`)
      }
  }, [roleId])
  useEffect(() => {
    if (skillCode){
      fetchSkill(`${viewSelectedSkillUrl}${skillCode}`)
    }
}, [skillCode])

useEffect(() => {
  if (roleId){
    fetchRelatedSkills(`${viewSkillsByRoleUrl}${roleId}`)
  }
}, [roleId])

// hahahhahhahahahaa

useEffect(() => {
  if (skillCode){
    fetchRelatedCourses(`${viewCoursesBySkillUrl}${skillCode}`)
  }
}, [skillCode])

    const deleteRole = async(role_id) => {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ role_id: role_id })
      };
      fetch(deleteRoleUrl, requestOptions)
        .then(response => response.json())
    } catch (error) {
        console.log(error.response)
    }
      const updatedRoles = roles.filter((role) => role.role_id !== role_id);
      setRoles(updatedRoles)
    }
    const deleteSkill = async(skill_code) => {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skill_code: skill_code })
      };
      fetch(deleteSkillUrl, requestOptions)
        .then(response => response.json())
    } catch (error) {
        console.log(error.response)
    }
      const updatedSkills = skills.filter((skill) => skill.skill_code !== skill_code);
      setSkills(updatedSkills)
    }
    const updateSkill = async(formData) => {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      };
      fetch(updateSkillUrl, requestOptions)
        .then(response => response.json())
    
    } catch (error) {
        console.log(error.response)
    }
      const updatedSkills = skills;
      setSkills(updatedSkills)
    }

    const createSkill = async(formData) => {
      try {
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      };
      fetch(createSkillUrl, requestOptions)
        .then(response => response.json())
    
    } catch (error) {
        console.log(error.response)
    }
    }


    const updateRole = async(formData) => {
      try {
        const requestOptions = {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
      };
      fetch(updateRoleUrl, requestOptions)
        .then(response => response.json())
    
    } catch (error) {
        console.log(error.response)
    }
    }

    const selectSkill = (skill_code) => {
      setSkillCode(skill_code)
      setShowModal(true);
    }

    
  
    return (
      <AppContext.Provider
        value={{roles, deleteRole, role, setRoleId, setRole, skills, deleteSkill, setSkillCode, setSkill, skill, setRoles, fetchRoles, setSkills,
          updateSkill, createSkill, updateRole, activeStep, setActiveStep, skipped, setSkipped, roleId, skillCode, courses, addCourses, setAddCourses,
          closeModal, showModal, relatedSkills, selectSkill, ljCourses, setljCourses
}}
      >
        {children}
      </AppContext.Provider>
    )
  }
  
  export const useGlobalContext = () =>{ 
    return useContext(AppContext)
  }
  export {AppContext, AppProvider}
