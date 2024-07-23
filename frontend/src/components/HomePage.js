import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css_files/HomePage.css';

const HomePage = () => {
  const [menu, setMenu] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await fetch('http://localhost:5000/get_menu', {
          method: 'GET',
          credentials: 'include',  // Include credentials (cookies) in the request
        });

        if (response.status === 401) {
          navigate('/login');  // Redirect to login if unauthorized
          return;
        }

        const data = await response.json();

        if (response.ok) {
          setMenu(data);
        } else {
          setError(data.error);
        }
      } catch (error) {
        setError('Failed to fetch menu. Error = ' + error);
      }
    };

    fetchMenu();
  }, [navigate]);

  const handleOrderClick = () => {
    console.log('Order button clicked!');
    // Implement your order handling logic here
    // For example, navigate to an order page or show a modal
    // navigate('/order');
  };

  return (
    <div className="menu-container">
      <h2>Seifu's Sizzle Menu</h2>
      {error && <p className="error-message">{error}</p>}
      <table className="menu-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          {menu.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.description}</td>
              <td>${item.price}</td>
              <td>{item.available ? "Available" : "Unavailable"}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="order-button" onClick={handleOrderClick}>
        Place an Order
      </button>
    </div>
  );
};

export default HomePage;
