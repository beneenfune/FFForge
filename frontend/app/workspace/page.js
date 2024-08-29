'use client';

import { useEffect, useState } from 'react'
import styles from '../../styles/Landing.module.css'; 
import MinMainComponent from '../../components/MinMainComponent'; 


export default function Workspace() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    
    
    // Fetch data from the API
    useEffect(() => {
        const fetchWorkspace = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/workspace')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.land);
                setLoading(false);
                console.log("Navigation to Workspace Successful")
            }
        }
        fetchWorkspace()
    }, []);

    return (
        <div className={styles.body}>
        <MinMainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Welcome to the Workspace Page</h3>
          </div>

        </div>
      );
}
