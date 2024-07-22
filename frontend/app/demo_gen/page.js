'use client';

import { useEffect, useState } from 'react'
import styles from "./page.module.css";
import DemoDisplay from './DemoDisplay.js';

export default function Home() {
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
            const response = await fetch('http://127.0.0.1:8000/api/demo_gen')
            const json = await response.json()

            if ( response.ok ){
                setFormData(json)
            }
        }
        fetchDemo()
    }, []);

    // Event handler for input changes
    const handleInputChange = (e) => {
        const { name, value, type, files } = e.target; // Destructure the relevant properties from the event target
        // Update the formData state with the new input values
        setFormData(prevState => ({
            ...prevState, // Keep the existing state
            [name]: type === "file" ? files[0] : value // If the input type is file, set the value to the first file, otherwise set the value to the input value
        }));
    };

    // Event handler for form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent the default form submission behavior
        setLoading(true);

        try {
            const formPayload = new FormData();
            formPayload.append('structname', formData.structname);
            formPayload.append('starttemp', formData.starttemp);
            formPayload.append('steptemp', formData.steptemp);
            formPayload.append('endtemp', formData.endtemp);
            formPayload.append('infile', formData.infile);
            formPayload.append('datafile', formData.datafile);
            formPayload.append('slurmfile', formData.slurmfile);

            const response = await fetch('http://127.0.0.1:8000/api/demo_gen', {
                method: 'POST',
                body: formPayload
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const responseData = await response.json();
            setResponse(responseData);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className={styles.container}>
            <h1 className={styles.header}>Demo Input Generator</h1>
            <p> {!loading ? message : "Loading.."}</p>

            <form onSubmit={handleSubmit} method="post" encType="multipart/form-data" action="form-processed/">
                <div>

                    {/*Input field for structure_name */}
                    <div>
                        <label htmlFor="structname">Name of Structure</label>
                        <input 
                            type="text" 
                            name="structname" 
                            placeholder="None"
                            value={formData.structname}
                            onChange={handleInputChange} 
                            required />
                    </div>
                    
                    {/* Input field for START of temperture_range */}
                    <div>
                        <label htmlFor="starttemp">Starting Temperature for the Temperture Range</label>
                        <input 
                            type="number"   
                            step="0.00001" 
                            name="starttemp" 
                            //TODO: if chatgpt doesnt work use id="" 
                            placeholder="Float value" 
                            value={formData.starttemp}
                            onChange={handleInputChange}
                            required />
                    </div>

                    {/* Input field for STEPS of temperture_range */}
                    <div>
                        <label htmlFor="steptemp">Temperture Step for the Temperture Range</label>
                        <input 
                            type="number" 
                            step="0.00001" 
                            name="steptemp" 
                            placeholder="Float value" 
                            value={formData.steptemp}
                            onChange={handleInputChange}
                            required />
                    </div>

                     {/* Input field for END of temperture_range  */}
                    <div>
                        <label htmlFor="endtemp">Ending Temperature for the Temperture Range</label>
                        <input 
                            type="number" 
                            step="0.00001" 
                            name="endtemp" 
                            placeholder="Float value" 
                            value={formData.endtemp}
                            onChange={handleInputChange}
                            required />
                    </div>

                     {/* Input button for IN file  */}
                    <div>
                        <label htmlFor="infile">Choose a in.* file</label>
                        <input 
                            type="file" 
                            name="infile" 
                            onChange={handleInputChange}
                            //</div>id="infile"
                            />
                    </div>
                    
                    {/* Input button for DATA file */}
                    <div>
                        <label htmlFor="datafile">Upload data.* file</label>
                        <input 
                            type="file" 
                            name="datafile" 
                            onChange={handleInputChange}
                            //id="datafile"
                            />
                    </div>
                    
                    {/* Input button for SLURM file */}
                    <div>
                        <label htmlFor="slurmfile">Upload *.slurm file</label>
                        <input 
                            type="file" 
                            name="slurmfile" 
                            onChange={handleInputChange}
                            //id="slurmfile" 
                        />
                    </div>

                </div>

                {/*  Submit button */}
                <div>
                    <input type="submit"
                    value="Submit"></input>
                </div>
            </form>

            {/* Render DemoDisplay if response is defined */}
            {response && <DemoDisplay response={response} />}
        </div>
    );
}
