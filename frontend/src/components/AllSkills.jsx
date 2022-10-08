import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Checkbox from '@mui/material/Checkbox';
import axios from 'axios';
import { Button } from '@mui/material';

export default function AllSkills() {
  const [checked, setChecked] = React.useState([]);
  const [skills, setSkills] = React.useState();

  React.useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
        try {
            const response = await axios("http://192.168.0.102:5000/view")
              console.log(response)
              if (isMounted) {
                setSkills(response.data)
              }
              console.log(skills)
        } catch (error) {
            console.log(error)
        }
    }
    fetchData()
    return () => (isMounted = false);
  }, [])

  console.log(skills, "kakak")


  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];
    console.log("first", newChecked)

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
    console.log("second", checked)
  };

  const skill_codes = ["AI101", "AI09", "CM02"]
  const skill_name = ["AI101 - French", "AI09 - Chinese", "CM02 - Japanese"]

  return (
    <>
    <List dense sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      {skill_name.map((value) => {
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
              <ListItemAvatar>
              </ListItemAvatar>
              <ListItemText id={labelId} primary={`${value}`} />
            </ListItemButton>
          </ListItem>
          
        );
      })}
    </List>
    <Button variant="contained">Create Role</Button>
    </>

  );
}