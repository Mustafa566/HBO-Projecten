import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL_USER_LIST } from "./constants";

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    async function fetchUsers() {
      const response = await axios.get(API_URL_USER_LIST);
      setUsers(response.data);
    }

    fetchUsers();
  }, []);

  return (
    <div>
      <h1>User List</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.username}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;