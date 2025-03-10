'use client';

import { useEffect, useState } from 'react'
import { useNavigation } from '../../utils/navigation';
import styles from '../../styles/Landing.module.css'; 
// import MainComponent from '../../components/MainComponent'; 
import FileForm from './FileForm';
import WorkflowForm from './WorkflowForm';
import Layout from "../../components/Layout"; 


export default function FileInput() {
    const { navigateToFileInput } = useNavigation();
        
  return (
    <Layout>
      <div className={styles.body}>
        <div className={styles.content}>
          <h3 className={styles.heading3}>Begin generating your forcefield:</h3>
          <p>
            <button
              onClick={navigateToFileInput}
              className={styles.clickedLink}
            >
              Input a structure file (*.mol, *.bgf, *.cif, *.xyz, *.pdb)
            </button>
          </p>
          <WorkflowForm />
        </div>
      </div>
    </Layout>
  );
}
