
import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import { Link } from 'react-router-dom';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { useGlobalContext } from '../context';
const drawerWidth = 240;
export default function PermanentDrawerLeft(){
  const { userDetails} = useGlobalContext()
    
    // const url = window.location.pathname
    // let path = ""
    // console.log(url)
    // if (url.includes("learningjourneys")){
    //     path = "Learning Journey"
    // }else if(url.includes("courses")){
    //     path = "Courses"
    // }else if(url.includes("roles")){
    //     path = "Roles"
    // }else{
    //     path = "Skills"
    // }
    const admin_drawer = {
      learningjourneys : 'Learning Journeys', roles: 'Manage Roles', skills : 'Manage Skills', courses: 'Manage Courses', learners: "Learners",  login: 'Logout'
    }

    const user_drawer = {
      learningjourneys : 'Learning Journeys', roles: 'Roles', skills : 'Skills', courses: 'Courses',  login: 'Logout'
    }

    const manager_drawer = {
      learningjourneys : 'Learning Journeys', roles: 'Roles', skills : 'Skills', courses: 'Courses',  teammembers: 'Team Members', login: 'Logout'
    }
    return(
        <>
        {/* <AppBar
        style={{backgroundColor:"#AFD8F2"}}
        position="fixed"
        sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            {path}
          </Typography>
        </Toolbar>
      </AppBar> */}
        <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent"
        anchor="left"
      >
        {/* <Toolbar /> */}
        <h2 style={{color:"#1F3541" ,textAlign:"left", marginLeft:"15px"}}>LJPS</h2>
        <Divider />
        {
          (userDetails.role == 1) &&
          <List>
          {Object.keys(admin_drawer).map((key, index) => (
            <ListItem key={index} component={Link} to={`/${key}`} disablePadding>
              <ListItemButton >
                <ListItemText style={{color:"#5289B5", fontWeight:"bold"}} primary={admin_drawer[key]} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        }
        {
          (userDetails.role == 2) &&
          <List>
          {Object.keys(user_drawer).map((key, index) => (
            <ListItem key={index} component={Link} to={`/${key}`} disablePadding>
              <ListItemButton >
                <ListItemText style={{color:"#5289B5", fontWeight:"bold"}} primary={user_drawer[key]} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        }
        {
          (userDetails.role == 3) &&
          <List>
          {Object.keys(manager_drawer).map((key, index) => (
            <ListItem key={index} component={Link} to={`/${key}`} disablePadding>
              <ListItemButton >
                <ListItemText style={{color:"#5289B5", fontWeight:"bold"}} primary={manager_drawer[key]} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        }
        {/* <Divider />
        <List>
          {['All mail', 'Trash', 'Spam'].map((text, index) => (
            <ListItem key={text} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List> */}
      </Drawer>
      </>
    )
}
