// components/MainHeaderComponent.js
import React from 'react';
import styles from '../styles/MainComponent.module.css'; 

const MainComponent = () => {
  return (
    <div className={styles.header}>
      <h1 className={styles.heading1}>FFForge</h1>
      <h2 className={styles.heading2}>Tool to generate forcefields for polymer structures</h2>
    </div>
  );
}

export default MainComponent;
