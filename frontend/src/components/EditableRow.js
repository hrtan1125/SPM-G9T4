import React from "react";

const EditableRow = ({}) => {
  return (
    <tr>
      <td>
        <input
          type="text"
          required="required"
          placeholder="Enter a role name..."
          name="role_name"
          //   value={editFormData.fullName}
          //   onChange={handleEditFormChange}
        ></input>
      </td>

      <td>
        <button type="submit">Save</button>
        {/* <button type="button" onClick={handleCancelClick}>
          Cancel
        </button> */}
      </td>
    </tr>
  );
};

export default EditableRow;
