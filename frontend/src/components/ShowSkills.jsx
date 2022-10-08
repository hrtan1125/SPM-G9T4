import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import axios from 'axios';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';

export default function ShowSkills({role_name}) {
  let navigate = useNavigate();

  // const {role_id, setRoles, roles, fetchRoles} = useGlobalContext()
  const [checked, setChecked] = React.useState([]);
  const [skills, setSkills] = React.useState();

  React.useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
        try {
            const response = await axios("http://192.168.0.102:5000/view")
              if (isMounted) {
                setSkills(response.data)
              }
        } catch (error) {
            console.log(error)
        }
    }
    fetchData()
    return () => (isMounted = false);
  }, [])


  const transformed_skills = [];

  skills?.data.map((skill) => {
    return (
      <>
        {skill.deleted === "no" && (
          transformed_skills.push(`${skill.skill_code} - ${skill.skill_name}` )
        )}
        
      </>
        
    )
  })

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }
    setChecked(newChecked);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const skill_codes_list = [];
    checked.map((skill) => {
      skill_codes_list.push(skill.split(" - ")[0])
    })
    addPosts(role_name, skill_codes_list);
    navigate(`/Roles`);
 };

 const addPosts = async(role_name, skills_list) => {
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role_name:  role_name, skills: skills_list})
  };
  fetch("http://192.168.0.102:5001/create", requestOptions)
    .then(response => response.json())

} catch (error) {
    console.log(error.response)
}
      // const updatedRoles = roles.filter((role) => role.role_id !== role_id);
      // console.log("UPDATTEE", updatedRoles)

      // const x = await fetchRoles()
      // console.log(x, "SLEEEEPPP")
};

  // const testdata = ["a - hello", "b - hihi", "c - kikik"]
  

  return (
    <>
    <List dense sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      {transformed_skills.map((value) => {
        const labelId = `checkbox-list-secondary-label-${value}`;
        return (
          <ListItem
            key={value}
            secondaryAction={
              <Checkbox
                edge="end"
                onChange={handleToggle(value)}
                checked={checked.indexOf(value) !== -1}
                inputProps={{ 'aria-labelledby': labelId }}
              />
            }
            disablePadding
          >
            <ListItemButton>
              <ListItemText id={labelId} primary={`${value}`} />
            </ListItemButton>
          </ListItem>
        );
      })}
    </List>
    <Button variant="contained" onClick={(e) => handleSubmit(e)}>Create Role</Button>
    </>
  );
}
