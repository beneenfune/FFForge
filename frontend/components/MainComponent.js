// components/MainHeaderComponent.js
import React from 'react';
import styles from '../styles/MainComponent.module.css'; 
import { useNavigation } from '../utils/navigation';


const MainComponent = () => {
  const { navigateToLanding } = useNavigation();

  return (
    <div className={styles.header}>
      <h1 className={styles.heading1} onClick={navigateToLanding} >FFForge</h1>
      <h2 className={styles.heading2}>Tfool to genrte forfields for poler strures</h2>
    </div>
  );
}

export default MainComponent;
