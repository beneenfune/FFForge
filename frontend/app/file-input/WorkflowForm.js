/*
Form for File Submission
*/
import { useState } from "react";
import styles from "../../styles/Landing.module.css";
import axios from "axios";

const WorkflowForm = () => {
  // Create file state
  const [structureFile, setStructureFile] = useState(null);
  const [primaryPurpose, setPrimaryPurpose] = useState(""); 
  const [structureType, setStructureType] = useState(""); 
  const [useActiveLearning, setUseActiveLearning] = useState("");
  const [prefix, setPrefix] = useState("");
  const [maxStructures, setMaxStructures] =  useState(0);
  const [filePath, setFilePath] = useState("");
  const [successMessage, setSuccessMessage] = useState(""); 

  // Use axios to handle multiple objects including files
  function handleSubmit(event) {
    event.preventDefault();
    const url = process.env.NEXT_PUBLIC_BASE_URL + "/api/v1/workflow/submit";
    const formData = new FormData();
    formData.append("structure_file", structureFile);
    formData.append("purpose", primaryPurpose);
    formData.append("structure_type", structureType);
    formData.append("use_active_learning", useActiveLearning);
    formData.append("max_structures", maxStructures);
    formData.append("prefix", prefix);

    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };

    // Send request to API and handle response
    axios
      .post(url, formData, config)
      .then((response) => {
        // Handle success
        if (response.status >= 200 && response.status < 300) {
        //   const file_path = response.data.structure_path;
        //   setFilePath(file_path); // Set the file path in the state
          setSuccessMessage(response.data.message); // Set the success message in the state
        } else {
          // Handle error if status code is not in the range of 2xx
          throw new Error(`HTTP error: ${response.status}`);
        }
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  }

//   // Function to handle file download
//   const handleDownload = () => {
//     axios({
//       url: filePath, // Use the filePath from the state
//       method: "GET",
//       responseType: "blob", // Important
//     })
//       .then((response) => {
//         // Extract the file name from the file path
//         const contentDisposition = response.headers["content-disposition"];
//         let filename = "downloaded_file"; // Default filename

//         if (contentDisposition) {
//           const fileNameMatch = contentDisposition.match(/filename="?(.+)"?/);
//           if (fileNameMatch.length === 2) {
//             filename = fileNameMatch[1];
//           }
//         } else {
//           // Fallback to extracting filename from filePath if content-disposition header is missing
//           const filePathParts = filePath.split("/");
//           filename = filePathParts[filePathParts.length - 1];
//         }

//         // create file link in browser's memory
//         const href = URL.createObjectURL(response.data);

//         // create "a" HTML element with href to file & click
//         const link = document.createElement("a");
//         link.href = href;
//         link.setAttribute("download", filename); // Set the download attribute to the original filename
//         document.body.appendChild(link);
//         link.click();

//         // clean up "a" element & remove ObjectURL
//         if (document.body.contains(link)) {
//           document.body.removeChild(link);
//         }
//         URL.revokeObjectURL(href);
//       })
//       .catch((error) => {
//         console.error("Error downloading file: ", error);
//       });
//   };

  return (
    <form className={styles.create} onSubmit={handleSubmit}>
      {/* STRUCTURE FILE */}
      <label className={styles.label}>
        Upload a Structure File for your MLFF <span style={{ color: "red" }}>*</span>
      </label>
      <input
        type="file"
        onChange={(e) => setStructureFile(e.target.files[0])}
        required
      />

      
      {/* PREFIX */}
      <div>
        <label className={styles.label}>
          What prefix would describe your structure file?
          <span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="text"
          value={prefix}
          onChange={(e) => setPrefix(e.target.value)}
          placeholder="Enter a prefix"
          required
        />
      </div>

      {/* PURPOSE */}
      <div>
        <label className={styles.label}>
          Which of the following is the primary purpose of the MLFF?
          <span style={{ color: "red" }}>*</span>
        </label>
        <select
          value={primaryPurpose}
          onChange={(e) => setPrimaryPurpose(e.target.value)}
          required
        >
          <option value="">Select an option</option>
          <option value="Simple Equilibration">Simple Equilibration</option>
          <option value="DMA">DMA</option>
          <option value="Anode depletion">Anode depletion</option>
          <option value="Electrolyte chemical environment">
            Electrolyte chemical environment
          </option>
          <option value="Adsorption analysis">Adsorption analysis</option>
        </select>
      </div>

      {/* STRUCTURE TYPE */}
      <div>
        <label className={styles.label}>
          Which structure type would you like to use?
          <span style={{ color: "red" }}>*</span>
        </label>
        <select
          value={structureType}
          onChange={(e) => setStructureType(e.target.value)}
          required
        >
          <option value="">Select an option</option>
          <option value="Crystalline">Crystalline</option>
          <option value="Amorphous">Amorphous</option>
          <option value="Molecular">Molecular</option>
        </select>
      </div>

      {/* MAX STRUCTURES */}
      <div>
        <label className={styles.label}>
          How many structures would you want to use to train your MLFF?
          <span style={{ color: "red" }}>*</span>
        </label>
        <input
          type="number"
          value={maxStructures}
          onChange={(e) => setMaxStructures(e.target.value)}
          placeholder="Enter an integer ≤300"
          required
        />
      </div>


        {/* ACTIVE LEARNING */}
        <div>
        <label className={styles.label}>
          Would you like to use active learning, RECOMMENDED? 
          <span style={{ color: "red" }}>*</span>
        </label>
        <select
          value={useActiveLearning}
          onChange={(e) => setUseActiveLearning(e.target.value)}
          required
        >
          <option value="">Select an option</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>
      </div>

      {/* Submit button */}
      <div>
        <input type="submit" value="Submit" className={styles.button}/>
      </div>

      {/* Display success message if available */}
      {successMessage && (
        <div>
          <p className={styles.successMessage}>{successMessage}</p>
        </div>
      )}

      {/* Download button, shown only when filePath is available
      {filePath && (
        <div>
          <button type="button" className={styles.button} onClick={handleDownload}>
            Download File
          </button>
        </div>
      )} */}
    </form>
  );
};

export default WorkflowForm;
