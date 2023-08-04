import React, { useState, useEffect } from "react";

import axios from "axios";
export const LandingPage= () => {
  const [user, setUser] = useState({});
  const [error,setError]=useState()

  const logoutUser =()=>{
    axios.post('http://127.0.0.1:5000/logout',{},{
      withCredentials: true,
    });
    window.location.href='/about';

  }

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/me',{
        withCredentials: true,
      }).then((response)=>{setUser(response.data); console.log(response)}).catch(function(error){
      console.log(error,error.response.status)
      setError(error.response.status)
    })},[])

  return (
    <div>
      <h1>Welcome to this React Application</h1>
      {Object.keys(user) == 0 ? (
        <div>
        <p>You are not logged in</p>
        <div>
          <a href="/login">
            <button>Login</button>
          </a>
          <a href="/register">
            <button>Register</button>
          </a>
        </div>
      </div>
      ) : (
        <div>
          <h2>Logged in</h2>
          <h3>ID: {user.id}</h3>
          <h3>Email: {user.email}</h3>
          <button onClick={logoutUser}>Logout</button>
        </div>
      )}
    </div>
  );
};
