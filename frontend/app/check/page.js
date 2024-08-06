'use client';

import { useEffect, useState } from 'react'
import styles from '../../styles/Landing.module.css'; 
import MinMainComponent from '../../components/MinMainComponent'; 


export default function Check() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);

    
    // Fetch data from the API
    useEffect(() => {
        const fetchLanding = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/check')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.land);
                setLoading(false);
                console.log("Verification Page Navigation Successful")
            }
        }
        fetchLanding()
    }, []);

    return (
        <div className={styles.body}>
        <MinMainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Welcome to Structure Verification Page</h3>
          </div>

        </div>
      );
}
