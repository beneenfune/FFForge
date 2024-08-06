/*
Form for SMILE Submission
*/ 
import { useState } from "react";
import styles from '../../styles/Landing.module.css'; 
import axios from 'axios';

const SMILESForm = () => {
    // Create state
    const [smilesString, setSmilesString] = useState("")
    const [filePath, setFilePath] = useState('')

    // Use axios to handle multiple objects including files
    function handleSubmit(event) { 
        event.preventDefault();

        const url = process.env.NEXT_PUBLIC_BASE_URL + '/api/text-input'; 
        const formData = new FormData();
        formData.append('smilesString', smilesString);

        // Log the formData entries
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        const config = {
            headers: {
                'content-type': 'multipart/form-data',
            },
        };
        
        // Send request to API and handle response
        axios.post(url, formData, config)
            .then((response) => {

                // Handle success
                if (response.status >= 200 && response.status < 300) {
                    const file_path = response.data.filePath;
                    setFilePath(file_path);  // Set the file path in the state
                    console.log(response.data.filePath);
                } else {
                    // Handle error if status code is not in the range of 2xx
                    throw new Error(`HTTP error: ${response.status}`);
                }
            })
            .catch((error) => {
                console.error("Error uploading SMILES string: ", error);
            });
    }

    // Function to handle file download
    const handleDownload = () => {
        axios({
            url: filePath, // Use the zipPath from the state
            method: 'GET',
            responseType: 'blob', // important
        }).then((response) => {
            // create file link in browser's memory
            const href = URL.createObjectURL(response.data);

            // create "a" HTML element with href to file & click
            const link = document.createElement('a');
            link.href = href;
            link.setAttribute('download', 'file.txt'); // or any other extension
            document.body.appendChild(link);
            link.click();

            // clean up "a" element & remove ObjectURL
            if (document.body.contains(link)) {
                document.body.removeChild(link);
            }
            URL.revokeObjectURL(href);
        });
    };  

    return (
        <form className={styles.create} onSubmit={handleSubmit}>
            {/* Input field for SMILES string */}
            <input 
                type="text" 
                placeholder="Enter SMILES string"
                onChange={(e) => setSmilesString(e.target.value)}
                value={smilesString}
                required 
            />

            {/* Submit button */}
            <div>
                <input type="submit" value="Submit" />
            </div>

            {/* Download button, shown only when zipPath is available */}
            {filePath && (
                <div>
                    <button type="button" onClick={handleDownload}>
                        Download File
                    </button>
                </div>
            )}
        </form>
    );
}

export default SMILESForm;
