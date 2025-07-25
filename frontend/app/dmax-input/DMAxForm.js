/*
Form for DMAx Workflow Submission
*/ 
import { useState } from "react";
import styles from '../../styles/Landing.module.css'; 
import axios from 'axios';

const DMAxForm = () => {
    // Create string state
    const [name, setName] = useState("");
    const [smileStringInput, setSmileString] = useState("");
    const [leftCap, setLeftCap] = useState("");
    const [rightCap, setRightCap] = useState("");
    const [polyLength, setPolyLength] = useState("");
    const [numMol, setNumMol] = useState("");
    const [density, setDensity] = useState("");

    const [filePath, setFilePath] = useState('')
    const [successMessage, setSuccessMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Use axios to handle multiple objects including files
    function handleSubmit(event) { 
        event.preventDefault();

        // disables button if submitting (prevent 2x submissions)
        if (isSubmitting) return;

        setIsSubmitting(true);
        setSuccessMessage("");
        setErrorMessage("");

        // checks for integers/floats
        const polyNum = parseFloat(polyLength);
        if (isNaN(polyNum) || !Number.isInteger(polyNum) || polyNum < 0) {
            setErrorMessage("Please enter a valid integer polymer length.");
            setIsSubmitting(false);
            return;
        }
        const molNum = parseFloat(numMol);
        if (isNaN(molNum) || !Number.isInteger(molNum) || molNum < 0) {
            setErrorMessage("Please enter a valid number of molecules.");
            setIsSubmitting(false);
            return;
        }
        const densityNum = parseFloat(density);
        if (isNaN(densityNum) || densityNum < 0) {
            setErrorMessage("Please enter a valid float density.");
            setIsSubmitting(false);
            return;
        }


        // create form data
        const url = process.env.NEXT_PUBLIC_BASE_URL + '/api/dmax-input'; 
        const formData = new FormData();
        formData.append("smilesString", smileStringInput);
        formData.append("name", name);
        formData.append("leftCap", leftCap);
        formData.append("rightCap", rightCap);
        formData.append("polymerLength", polyLength);
        formData.append("numberMolecules", numMol);
        formData.append("density", density);

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
                    setLeftCap("");
                    setRightCap("");
                    setPolyLength("");
                    setNumMol("");
                    setDensity("")


                } else {
                    // Handle error if status code is not in the range of 2xx
                    throw new Error(`HTTP error: ${response.status}`);
                }
            })
            .catch((error) => {
                setErrorMessage("Submission failed, please try again.")
                console.error("Error uploading DMAx workflow: ", error);
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
                What is the name of your workflow?
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter a workflow name"
                required
            />
            </div>

            {/* SMILESTRINGINPUT */}
            <div>
            <label className={styles.label}>
                What SMILES string correlates with your workflow?
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={smileStringInput}
                onChange={(e) => setSmileString(e.target.value)}
                placeholder="Enter a SMILES string"
                required
            />
            </div>

            {/* LEFT CAP */}
            <div>
            <label className={styles.label}>
                What left cap correlates with your SMILES string?
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={leftCap}
                onChange={(e) => setLeftCap(e.target.value)}
                placeholder="Enter a left cap"
                required
            />
            </div>

            {/* RIGHT CAP */}
            <div>
            <label className={styles.label}>
                What right cap correlates with your SMILES string?
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="text"
                value={rightCap}
                onChange={(e) => setRightCap(e.target.value)}
                placeholder="Enter a right cap"
                required
            />
            </div>


            {/* POLYMER CHAIN LENGTH */}
            <div>
            <label className={styles.label}>
                Enter a polymer chain length:
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="number"
                value={polyLength}
                onChange={(e) => setPolyLength(e.target.value)}
                placeholder="Enter a polymer chain length"
                required
                step = "1"
            />
            </div>

            {/* NUMBER OF MOLECULES */}
            <div>
            <label className={styles.label}>
                Enter the number of molecules:
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="number"
                value={numMol}
                onChange={(e) => setNumMol(e.target.value)}
                placeholder="Enter the number of molecules"
                required
                step = "1"
            />
            </div>

            {/* DENSITY */}
            <div>
            <label className={styles.label}>
                Enter the density:
                <span style={{ color: "red" }}>*</span>
            </label>
            <input
                type="number"
                value={density}
                onChange={(e) => setDensity(e.target.value)}
                placeholder="Enter the density"
                required
                step = "any"
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

export default DMAxForm;