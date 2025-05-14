// components/MainHeaderComponent.js
import React from 'react';
import styles from '../styles/MinMainComponent.module.css'; 
import { useNavigation } from '../utils/navigation';


const MinMainComponent = () => {
  const { navigateToLanding } = useNavigation();

  return (
    <div className={styles.header}>
      <h1 className={styles.heading1} onClick={navigateToLanding} >FFForge - Tol for forfilds for polymer structes</h1>
    </div>
  );
}

export default MinMainComponent;