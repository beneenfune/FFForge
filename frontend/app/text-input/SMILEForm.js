/*
Form for SMILE string Submission
*/ 
import { useState } from "react";
import styles from '../../styles/Landing.module.css'; 
import axios from 'axios';

const SMILESForm = () => {
    // Create string state
    const [smileStringInput, setSmileString] = useState("");
    const [filePath, setFilePath] = useState('')
    const [successMessage, setSuccessMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [name, setName] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Use axios to handle multiple objects including files
    function handleSubmit(event) { 
        event.preventDefault();

        //disables button if submitting (prevent 2x submissions)
        if (isSubmitting) return;

        setIsSubmitting(true);
        setSuccessMessage("");
        setErrorMessage("");

        const url = process.env.NEXT_PUBLIC_BASE_URL + '/api/text-input'; 
        const formData = new FormData();
        formData.append("smilesString", smileStringInput);
        formData.append("name", name);

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
                    setSuccessMessage("Form Submitted!");
                    setTimeout(() => {
                        setSuccessMessage("");
                    }, 3000); 
                    const file_path = response.data.filePath;
                    setFilePath(file_path);  // Set the file path in the state
                    console.log(response.data.filePath);

                    // clear the entry boxes
                    setSmileString("");
                    setName("");
                } else {
                    // Handle error if status code is not in the range of 2xx
                    throw new Error(`HTTP error: ${response.status}`);
                }
            })
            .catch((error) => {
                setErrorMessage("Submission failed, please try again.")
                console.error("Error uploading SMILES string: ", error);
            })
            // re-enable button
            .finally(() => {
                setIsSubmitting(false); 
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
            
            {/* NAME */}
            <div>
            <label className={styles.label}>
                What is the name of your structure? 
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter a structure name"
                required
            />
            </div>

            {/* SMILESTRINGINPUT */}
            <div>
            <label className={styles.label}>
                What SMILE string correlates with your structure?
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={smileStringInput}
                onChange={(e) => setSmileString(e.target.value)}
                placeholder="Enter a SMILE STRING"
                required
            />
            </div>

            {/* Submit button */}
            <div>
                <input
                    type="submit"
                    value={isSubmitting ? "Submitting..." : "Submit"}
                    disabled={isSubmitting}
                />
            </div>

            {/* Success Message */}
            {successMessage && (
                <p style={{ color: 'green' , textAlign: 'center'}}>{successMessage}</p>
            )}

            {/* Failed Message */}
            {errorMessage && (
                <p style = {{ color: 'red', textAlign: 'center'}}>{errorMessage}</p>
            )}

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
