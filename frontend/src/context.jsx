import React, { useState, useContext, useEffect } from 'react'
import axios from 'axios'

const AppContext = React.createContext()

// const viewRoles = 'http://192.168.0.102:5001/view'

const rolesUrl = 'http://192.168.0.102:5001/view'
const deleteRoleUrl = 'http://192.168.0.102:5001/delete'
const viewSelectedRoleUrl = 'http://192.168.0.102:5001/viewselectedrole?role_id='

const AppProvider = ({ children }) => {
    const [roles, setRoles] = useState([])
    const [role, setRole] = useState([])
    const [roleId, setRoleId] = useState('')

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

    useEffect(() => {
        fetchRoles(rolesUrl)
    }, [])

    useEffect(() => {
      if (roleId){
        fetchRole(`${viewSelectedRoleUrl}${roleId}`)
      }
  }, [roleId])

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
  
    return (
      <AppContext.Provider
        value={{roles, deleteRole, role, setRoleId, showSkills, setRole}}
      >
        {children}
      </AppContext.Provider>
    )
  }

  
  export const useGlobalContext = () =>{ 
    return useContext(AppContext)
  }

  export {AppContext, AppProvider}
