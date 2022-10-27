import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Checkbox from '@mui/material/Checkbox';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useGlobalContext } from '../context';

export default function ShowSkills({role_name}) {
  let navigate = useNavigate();

  const [checked, setChecked] = React.useState([]);
  const {skills} = useGlobalContext()

  const transformed_skills = [];

  skills?.map((skill) => {
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
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const skill_codes_list = [];
    checked.map((skill) => {
      skill_codes_list.push(skill.split(" - ")[0])
    })
    addPosts(role_name, skill_codes_list);
    navigate(`/Roles`);
 };

 console.log(checked, "selected skills")

 const addPosts = async(role_name, skills_list) => {
  console.log(skills_list, "skills list")
  console.log(role_name, "role_name")
  try {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role_name:  role_name, skills: skills_list})
  };
  fetch("http://127.0.0.1:5001/create", requestOptions)
    .then(response => response.json())

} catch (error) {
    console.log(error.response)
}
};
  

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
