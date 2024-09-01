import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css_files/HomePage.css';
import MenuPopup from './MenuPopup';

const HomePage = () => {
  const [menu, setMenu] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await fetch('http://localhost:5000/get_menu', {
          method: 'GET',
          credentials: 'include',
        });

        if (response.status === 401) {
          navigate('/login');
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

  return (
    <div className="menu-container">
      <h2>Seifu's Sizzle Menu</h2>
      {error && <p className="error-message">{error}</p>}
      <div className="popups-container">
        {menu.map((item) => (
          <MenuPopup key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
