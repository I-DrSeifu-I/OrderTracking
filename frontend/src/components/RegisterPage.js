import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
    const [first_name, setfirst_name] = useState('');
    const [last_name, setlast_name] = useState('');
    const [email, setemail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
    
        const response = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ first_name, last_name, email, password}),
        });
    
        if (response.status === 409) {
          setError('Email already exists, please register with a different email.');
        } else if (response.ok) {
          navigate('/home');
        } else {
          setError('Please ensure you have all information entered.');
        }
    };

    return (
        <div className="form-container">
          <h2>Register</h2>
          <form onSubmit={handleRegister}>
            <input
              className="input-field"
              type="text"
              placeholder="First Name"
              value={first_name}
              onChange={(e) => setfirst_name(e.target.value)}
            />
            <input
              className="input-field"
              type="text"
              placeholder="Last Name"
              value={last_name}
              onChange={(e) => setlast_name(e.target.value)}
            />
            <input
              className="input-field"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setemail(e.target.value)}
            />
            <input
              className="input-field"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button className="register-button" type="submit">Register</button>
            {error && <div className="error-message">{error}</div>}
          </form>
        </div>
      );
};
    
export default RegisterPage;
