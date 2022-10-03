import React, { useEffect } from 'react'
import { Routes, Route, useParams } from 'react-router-dom';
import { useGlobalContext } from '../context';

const SelectedRole = () => {
    const {role_id} = useParams()
    const {role, setRoleId} = useGlobalContext()
    setRoleId(role_id)

  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
        <div>{role.role_id}{role.deleted}{role.role_name}</div>
    </div>
    
  )
}

export default SelectedRole