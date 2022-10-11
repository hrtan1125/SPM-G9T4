
import React, { useState, useContext, useEffect } from 'react'
import axios from 'axios'
const AppContext = React.createContext()

// Roles
const rolesUrl = 'http://127.0.0.1:5001/view'
const viewSelectedRoleUrl = 'http://127.0.0.1:5001/viewselectedrole?role_id='
const deleteRoleUrl = 'http://127.0.0.1:5001/delete'
const updateRoleUrl = 'http://127.0.0.1:5001/update'

// Skills
const skillsUrl = 'http://127.0.0.1:5000/view'
const viewSelectedSkillUrl = "http://127.0.0.1:5000/viewselectedskill?skill_code="
const viewSkillsByRoleUrl = 'http://127.0.0.1:5002/viewRoleSkills?role_id='
const updateSkillUrl = 'http://127.0.0.1:5000/update'
const createSkillUrl = 'http://127.0.0.1:5000/create'
const deleteSkillUrl = 'http://127.0.0.1:5000/delete'

// Courses
const coursesUrl = 'http://127.0.0.1:5002/viewAllCourses'
const viewCoursesBySkillUrl = 'http://127.0.0.1:5002/viewCourses?skill_code='


const AppProvider = ({ children }) => {
    // Roles
    const [roles, setRoles] = useState([])
    const [role, setRole] = useState([])
    const [roleId, setRoleId] = useState('')

    // Skills
    const [skills, setSkills] = useState([])
    const [relatedSkills, setRelatedSkills] = useState([])
    const [skill, setSkill] = useState([])
    const [skillCode, setSkillCode] = useState('')
    
    // Courses
    const [courses, setCourses] = useState([])
    const [allCourses, setAllCourses] = useState([])
    const [addCourses, setAddCourses] = useState([])

    // Learning Journey Pages
    const [ljCourses, setljCourses] = useState({})
    const [showModal, setShowModal] = useState(false)
    const [activeStep, setActiveStep] = React.useState(0);
    const [skipped, setSkipped] = React.useState(new Set());

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

const fetchCourses = async(url) => {
  try {
      const {data} = await axios(url)
      setAllCourses(data.data)
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
      fetchCourses(coursesUrl)
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
        value={{roles, deleteRole, role, setRoleId, setRole, skills, deleteSkill, setSkillCode, setSkill, skill, setRoles, fetchRoles, rolesUrl, setSkills,
          updateSkill, createSkill, updateRole, activeStep, setActiveStep, skipped, setSkipped, roleId, skillCode, courses, allCourses, addCourses, setAddCourses,
          closeModal, showModal, relatedSkills, selectSkill, ljCourses, setljCourses, fetchSkills, skillsUrl, setShowModal
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
