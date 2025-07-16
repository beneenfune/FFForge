'use client';

import { useEffect, useState } from 'react'
import { useNavigation } from '../../utils/navigation';
import styles from '../../styles/Landing.module.css'; 
import DMAxForm from './DMAxForm.js';
import Layout from "../../components/Layout"; 

export default function TextInput() {
    
  // Create states
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [structureText, setStructureText] = useState("")
    const { navigateToDMAx } = useNavigation();

    
    // Fetch data from the API
    useEffect(() => {
        const fetchTextInput = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/text-input')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.text);
                setLoading(false);
                console.log("Text Inputter Visiualized")
            }
        }
        fetchTextInput()
    }, []);

        
  return (
    <Layout>
      <div className={styles.body}>
        <div className={styles.content}>
          <h3 className={styles.heading3}>
            Submit a DMAx Workflow
          </h3>
          <p>
            <button
              onClick={navigateToDMAx}
              className={styles.clickedLink}
            >
              Input DMAx Workflow Parameters
            </button>
          </p>
          <DMAxForm />
        </div>
      </div>
    </Layout>
  );
}
