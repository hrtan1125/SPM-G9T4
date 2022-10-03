import React from "react";

const ReadOnlyRow = ({ role }) => {
  return (
    <tr>
      <td>{role.role_name}</td>
      {/* <td>{contact.address}</td>
      <td>{contact.phoneNumber}</td>
      <td>{contact.email}</td> */}
      <td>
        {/* <button
          type="button"
          onClick={(event) => handleEditClick(event, contact)}
        >
          Edit
        </button>
        <button type="button" onClick={() => handleDeleteClick(contact.id)}>
          Delete
        </button> */}
      </td>
    </tr>
  );
};

export default ReadOnlyRow;
