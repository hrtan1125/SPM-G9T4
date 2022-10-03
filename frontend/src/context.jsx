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

const AppProvider = ({ children }) => {
    const [roles, setRoles] = useState([])
    const [role, setRole] = useState([])
    const [roleId, setRoleId] = useState('')

    const [skills, setSkills] = useState([])
    const [skill, setSkill] = useState([])
    const [skillCode, setSkillCode] = useState('')

    const [showSkills, setShowSkills] = useState(true)

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
      console.log("fireball", data)
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
      console.log("rolleeet", roleId)
      if (roleId){
        fetchRole(`${viewSelectedRoleUrl}${roleId}`)
      }
  }, [roleId])

  useEffect(() => {
    console.log("skillllet", skillCode)
    if (skillCode){
      fetchSkill(`${viewSelectedSkillUrl}${skillCode}`)
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
  
    return (
      <AppContext.Provider
        value={{roles, deleteRole, role, setRoleId, showSkills, setRole, skills, deleteSkill, setSkillCode, setSkill, skill}}
      >
        {children}
      </AppContext.Provider>
    )
  }

  
  export const useGlobalContext = () =>{ 
    return useContext(AppContext)
  }

  export {AppContext, AppProvider}
