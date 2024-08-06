'use client';

import { useEffect, useState } from 'react'
import styles from "./page.module.css";
import DemoDisplay from './DemoDisplay.js';
import DemoForm  from './DemoForm';

const Home = () => {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        structname: "",
        starttemp: "",
        steptemp: "",
        endtemp: "",
        infile: null,
        datafile: null,
        slurmfile: null
    });
    const [response, setResponse] = useState(null);

    // Fetch data from the API
    useEffect(() => {
        const fetchDemo = async () => {
            const response = await fetch(process.env.NEXT_PUBLIC_BASE_URL + '/api/demo_gen')
            const json = await response.json()

            if ( response.ok ){
                setFormData(json)
            }
        }
        fetchDemo()
    }, []);

    return (
        <div className={styles.container}>
            <h1 className={styles.header}>Demo Input Generator</h1>
            <p> {!loading ? message : "Loading.."}</p>

           <DemoForm/>
        </div>
    );
}

export default Home