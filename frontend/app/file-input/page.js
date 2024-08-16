'use client';

import { useEffect, useState } from 'react'
import { useNavigation } from '../../utils/navigation';
import styles from '../../styles/Landing.module.css'; 
import MainComponent from '../../components/MainComponent'; 
import FileForm from './FileForm';

export default function FileInput() {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const { navigateToFileInput } = useNavigation();

    /*
    // Fetch data from the API
    useEffect(() => {
        const fetchFileInput = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL +'/api/file-input')
            const data = await response.json()

            if ( response.ok ){
                setMessage(data.file);
                setLoading(false);
                console.log("File Inputter Visiualized")
            }
        }
        fetchFileInput()
    }, []);
    */

        
    return (
        <div className={styles.body}>
        <MainComponent />
          
          <div className={styles.content}>
            <h3 className={styles.heading3}>Select a way to begin generating your forcefield:</h3>
            <p><button onClick={navigateToFileInput} className={styles.clickedLink}>Input a structure file (*.mol, *.bgf, *.cif, *.xyz, *.pdb)</button></p>
            <FileForm />

          </div>
        </div>
      );
}
