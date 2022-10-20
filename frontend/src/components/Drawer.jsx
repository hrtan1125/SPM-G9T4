import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import { Link } from 'react-router-dom';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';

const drawerWidth = 240;

export default function PermanentDrawerLeft(){
    
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
        <List>
          {['Roles', 'Skills', 'Courses', 'Learning Journeys'].map((text) => (
            <ListItem key={text} component={Link} to={`/${text==="Learning Journeys"? "learningjourneys":text}`} disablePadding>
              <ListItemButton >
                <ListItemText style={{color:"#5289B5", fontWeight:"bold"}} primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
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