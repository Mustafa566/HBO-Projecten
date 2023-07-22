import React, { useEffect, useState } from 'react';

const CurrentUser = () => {
  const [username, setUsername] = useState('');

  const checkLoginStatus = () => {
    // Check if the username is stored in localStorage
    const username = localStorage.getItem('Username');
    setUsername(username);
  };

  useEffect(() => {
    const interval = setInterval(checkLoginStatus, 0); // Run checkLoginStatus every 0 second (realtime)

    return () => {
      clearInterval(interval); // Clean up the interval on component unmount
    };
  }, []);

  return <div>{username}</div>;
};

export default CurrentUser;