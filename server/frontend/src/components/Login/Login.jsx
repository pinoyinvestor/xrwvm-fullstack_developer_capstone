import React, { useState } from 'react';
import "./Login.css";
import Header from '../Header/Header';

const Login = ({ onClose }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true);

  // Lägg till ett snedstreck i slutet av login_url
  let login_url = window.location.origin + "/djangoapp/login/";

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(login_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "userName": userName,
          "password": password
        }),
      });

      const json = await res.json();
      if (json.status != null && json.status === "Authenticated") {
        sessionStorage.setItem('username', json.userName);
        setOpen(false);
      } else {
        alert("The user could not be authenticated.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred during login. Please try again.");
    }
  };

  if (!open) {
    window.location.href = "/";
  };

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <form className="login_panel" onSubmit={login}>
            <div>
              <span className="input_field">Username </span>
              <input type="text" name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)} />
            </div>
            <div>
              <span className="input_field">Password </span>
              <input name="psw" type="password" placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)} />
            </div>
            <div>
              <input className="action_button" type="submit" value="Login" />
              <input className="action_button" type="button" value="Cancel" onClick={() => setOpen(false)} />
            </div>
            <a className="loginlink" href="/register">Register Now</a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
