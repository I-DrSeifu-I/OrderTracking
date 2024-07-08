import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  const getCurrentDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const orderDate = getCurrentDate();
    const data = {
      first_name: firstName,
      last_name: lastName,
      order_date: orderDate,
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/customer_orders', data, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log(response.data);
      alert('Customer order added successfully!');
    } catch (error) {
      console.error('There was an error adding the customer order!', error);
      alert('Failed to add customer order.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Customer Order Form</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>First Name:</label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Last Name:</label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
