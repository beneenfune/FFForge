'use client';

import { useEffect, useState } from 'react'
import { useNavigation } from '../../utils/navigation';
import styles from '../../styles/Landing.module.css'; 
import MainComponent from '../../components/MainComponent'; 
import SMILESForm from './SMILEForm';


export default function TextInput() {
    
  // Create states
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [structureText, setStructureText] = useState("")
    const { navigateToTextInput } = useNavigation();

    
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
        <div className={styles.body}>
        <MainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Select a way to begin generating your forcefield:</h3>
            <p><button onClick={navigateToTextInput} className={styles.clickedLink}>Input a SMILES Structure Text</button></p>
            <SMILESForm />
          
          </div>
        </div>
      );
}
