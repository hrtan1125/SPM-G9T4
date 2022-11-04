import React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useGlobalContext } from '../context';

export default function AlertDialog() {
  // const [open, setOpen] = React.useState(false);
  const {open, setOpen, lid, ltitle, setLTitle, setLid} = useGlobalContext();

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleDelete = () =>{
    setOpen(false);
    console.log("to delete", lid, ltitle)

    fetch(`http://127.0.0.1:5002/removelearningjourney/${lid}`,{
      method:"DELETE",
      headers: { 'Content-Type': 'application/json' }
    }).then(res=>{
      res.json()

      setLid(0)
      setLTitle("")
      window.location.reload(false);
    })
  }

  return (
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Delete Confirmation"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {ltitle} will be deleted
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleDelete} color="primary" autoFocus>
            Yes, Delete
          </Button>
        </DialogActions>
      </Dialog>
  );
}
