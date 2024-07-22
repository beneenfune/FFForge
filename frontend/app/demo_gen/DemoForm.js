/*
Form for Demo Generator

INPUTS:


*/ 

import { useState } from "react";
import axios from 'axios';

const DemoForm = () => {

    // Create states for form data
    const [structName, setStructName] = useState('')
    const [startTemp, setStartTemp] = useState('')
    const [stepTemp, setStepTemp] = useState('')
    const [endTemp, setEndTemp] = useState('')
    const [inFile, setInFile] = useState(null)
    const [dataFile, setDataFile] = useState(null)
    const [slurmFile, setSlurmFile] = useState(null)

    // Use axios to handlie multiple objects including files
    function handleSubmit(event) {
        event.preventDefault();
        const url = process.env.NEXT_PUBLIC_BASE_URL + '/api/demo_gen'; // TODO: potentially add back local host if doesnt work
        const formData = new FormData();
        formData.append('structname', structName);
        formData.append('starttemp', startTemp);
        formData.append('steptemp', stepTemp);
        formData.append('endtemp', endTemp);
        formData.append('infile', inFile);
        formData.append('datafile', dataFile);
        formData.append('slurmfile', slurmFile);

          // Log the formData entries
        for (let pair of formData.entries()) {
            console.log(pair[0]+ ': ' + pair[1]);
        }
        
        // https://www.filestack.com/fileschool/react/react-file-upload/
        const config = {
          headers: {
            'content-type': 'multipart/form-data',
          },
        };
        
        // Send request to api and handle retrieved response
        axios.post(url, formData, config)
            // If request was successful
            .then((response) => {
            
                // Handle success
                if (response.status >= 200 && response.status < 300) {
                    console.log(response.data);
                } else {
                    // Handle error if status code is not in the range of 2xx
                    throw new Error(`HTTP error: ${response.status}`);
                }

                // https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Fetching_data
                // Otherwise (if the response succeeded), our handler fetches the response
                // as text by calling response.text(), and immediately returns the promise
                // returned by `response.text()`.
            
                // TODO (implement): After processing on serverside, response.data should be  
                // looked up: how to output a file from axios to client side
                // try: https://stackoverflow.com/questions/41938718/how-to-download-files-using-axios
            })
            // Else, it will print error
            .catch((error) => {
                console.error("Error uploading files: ", error);
            });
      }

    return (
        <form className="create" onSubmit={handleSubmit}>
            <h3>Demo Generator</h3>

            {/*Input field for structure_name */}
            <label>Name of Structure</label>
            <input 
                type="text" 
                placeholder="None"
                onChange={(e) => setStructName(e.target.value)}
                value={structName}
                required 
            />
                    
            {/* Input field for START of temperture_range */}
            <label>Starting Temperature for the Temperture Range</label>
            <input 
                type="number"   
                step="0.00001" 
                placeholder="Float value"
                onChange={(e) => setStartTemp(e.target.value)}
                value={startTemp}
                required />

            {/* Input field for STEPS of temperture_range */}
            <label>Temperture Step for the Temperture Range</label>
            <input 
                type="number" 
                step="0.00001" 
                placeholder="Float value" 
                onChange={(e) => setStepTemp(e.target.value)}
                value={stepTemp}
                required />


            {/* Input field for END of temperture_range  */}
            <label>Ending Temperature for the Temperture Range</label>
            <input 
                type="number" 
                step="0.00001" 
                placeholder="Float value" 
                onChange={(e) => setEndTemp(e.target.value)}
                value={endTemp}
                required />


            {/* Input button for IN file  */}
            <label htmlFor="infile">Choose a in.* file</label>
            <input 
                type="file" 
                name="infile" 
                onChange={(e) => setInFile(e.target.files[0])}
            />
            
            {/* Input button for DATA file */}
            <label htmlFor="datafile">Upload data.* file</label>
            <input 
                type="file" 
                name="datafile" 
                onChange={(e) => setDataFile(e.target.files[0])}
            />
            
            {/* Input button for SLURM file */}
            <label htmlFor="slurmfile">Upload *.slurm file</label>
            <input 
                type="file" 
                name="slurmfile" 
                onChange={(e) => setSlurmFile(e.target.files[0])}
            />

            {/*  Submit button */}
            <div>
                <input type="submit"
                value="Submit"></input>
            </div>
        </form>

    )
}

export default DemoForm