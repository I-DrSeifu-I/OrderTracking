import React from 'react';
import './css_files/MenuPopup.css';

const MenuPopup = ({ item }) => {
  return (
    <div className="popup">
      <div className="popup-content">
        <span role="img" aria-label="food" className="food-icon">{item.emoji}</span>
        <h3>{item.name}</h3>
        <p>{item.description}</p>
        <p>Price: ${item.price}</p>
        <p>Status: {item.available ? "Available" : "Unavailable"}</p>
      </div>
    </div>
  );
};

export default MenuPopup;
