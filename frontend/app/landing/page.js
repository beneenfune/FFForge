'use client';

import { useEffect, useState } from 'react'
import React from 'react';
import styles from './page.module.css';
import MainComponent from '../../components/MainComponent'; 


export default function Home() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    
    // Fetch data from the API
    useEffect(() => {
        const fetchLanding = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/landing')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.land);
                setLoading(false);
                console.log("Text Inputter Visiualized")
            }
        }
        fetchLanding()
    }, []);

        
    return (
        <div className={styles.body}>
        <MainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Select a way to begin generating your forcefield:</h3>
            <p><a href="https://www.google.com/" className={styles.link} target="_blank" rel="noopener noreferrer">Input a SMILES Structure Text</a></p>
            <p><a href="https://www.yelp.com/" className={styles.link} target="_blank" rel="noopener noreferrer">Input a structure file (*.mol, *.bgf, *.cif, *.xyz, *.pdb)</a></p>
            <p><a href="https://www.youtube.com/" className={styles.link} target="_blank" rel="noopener noreferrer">Design a structure with GUI</a></p>
          </div>
        </div>
      );
}
