// components/MainHeaderComponent.js
import React from 'react';
import styles from '../styles/MinMainComponent.module.css'; 

const MinMainComponent = () => {
  return (
    <div className={styles.header}>
      <h1 className={styles.heading1}>FFForge - Tool to generate forcefields for polymer structures</h1>
    </div>
  );
}

export default MinMainComponent;