'use client';

import { useEffect, useState } from 'react'
import styles from '../../styles/Landing.module.css'; 
import MainComponent from '../../components/MainComponent'; 


export default function FileInput() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    
    // Fetch data from the API
    useEffect(() => {
        const fetchFileInput = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/file-input')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.text);
                setLoading(false);
                console.log("File Inputter Visiualized")
            }
        }
        fetchFileInput()
    }, []);

        
    return (
        <div className={styles.body}>
        <MainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Select a way to begin generating your forcefield:</h3>
            <p><a href="https://www.yelp.com/" className={styles.link} target="_blank" rel="noopener noreferrer">Input a structure file (*.mol, *.bgf, *.cif, *.xyz, *.pdb)</a></p>
          </div>
        </div>
      );
}
