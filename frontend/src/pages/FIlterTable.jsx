import * as React from 'react';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';
import { useGlobalContext } from '../context';

const VISIBLE_FIELDS = ['name', 'rating', 'country', 'dateCreated', 'isAdmin'];

export default function FilterTable() {
  const { data } = useDemoData({
    dataSet: 'Employee',
    visibleFields: VISIBLE_FIELDS,
    rowLength: 100,
  });

  console.log(data)

  const {roles, deleteRole, role} = useGlobalContext()

  const transformed = roles.map(({ role_name, role_id, deleted}) => ({ role_name, id: role_id,  deleted}));

  const x = {
    columns: [
        {
    "field": "id"
        },
        {
    "field": "role_name"
        },
        {

    "field": "deleted"
        }

    ],
    rows: transformed
    
}

  

  return (
    <div style={{display: 'flex', marginTop: 80, justifyContent: "center"}} >
            <div style={{ height: 700, width: '100%' }}>
      <DataGrid {...x} components={{ Toolbar: GridToolbar }} />
    </div>

    </div>
    
  );
}
