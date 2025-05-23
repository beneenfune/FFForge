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
  const [name, setName] = useState("");
  const [prefix, setPrefix] = useState("");
  const [maxStructures, setMaxStructures] =  useState(0);
  const [successMessage, setSuccessMessage] = useState("");
  const [atomToRemove, setAtomToRemove] = useState("");
  const [electrolyteAtoms, setElectrolyteAtoms] = useState("");
  const [adsorbateMolecules, setAdsorbateMolecules] = useState("");

  // Use axios to handle multiple objects including files
  function handleSubmit(event) {
    event.preventDefault();
    const url = process.env.NEXT_PUBLIC_BASE_URL + "/api/v1/workflow/submit";
    const formData = new FormData();
    formData.append("purpose", primaryPurpose);
    formData.append("use_active_learning", useActiveLearning);
    formData.append("max_structures", maxStructures);
    formData.append("prefix", prefix);

    // Conditionally append fields based on primaryPurpose
    if (primaryPurpose === "DMA") {
      formData.append("structure_type", structureType);
    } else if (primaryPurpose === "Electrode depletion") {
      formData.append("atom_to_remove", atomToRemove);
    } else if (primaryPurpose === "Electrolyte analysis") {
      formData.append("electrolyte_atoms", electrolyteAtoms);
    } else if (primaryPurpose === "Adsorption analysis") {
      formData.append("adsorbate_molecules", adsorbateMolecules);
    }

    // Ensure file is uploaded if required
    if (structureFile) {
      formData.append("structure_file", structureFile);
    }

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

  return (
    <form className={styles.create} onSubmit={handleSubmit}>
      {/* STRUCTURE FILE */}
      <label className={styles.label}>
        Upload a Structure File for your MLFF{" "}
        <span style={{ color: "red" }}>*</span>
      </label>
      <input
        type="file"
        onChange={(e) => setStructureFile(e.target.files[0])}
        required
      />

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
          <option value="Simple equilibration">Simple equilibration</option>
          <option value="DMA">DMA</option>
          <option value="Electrode depletion">Electrode depletion</option>
          <option value="Electrolyte analysis">Electrolyte analysis</option>
          <option value="Adsorption analysis">Adsorption analysis</option>
        </select>
      </div>

      {/* STRUCTURE TYPE (only for DMA) */}
      {primaryPurpose === "DMA" && (
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
            <option value="Semi-crystalline">Semi-crystalline</option>
          </select>
        </div>
      )}

      {/* Electrode Depletion - Select Atom to Remove */}
      {primaryPurpose === "Electrode depletion" && (
        <div>
          <label className={styles.label}>
            Which atom would you like to remove? (e.g. Li, Na)
            <span style={{ color: "red" }}>*</span>
          </label>
          <input
            type="text"
            value={atomToRemove}
            onChange={(e) => setAtomToRemove(e.target.value)}
            placeholder="Enter the atom symbol"
            required
          />
        </div>
      )}

      {/* Electrolyte Analysis - Enter Electrolyte Atoms */}
      {primaryPurpose === "Electrolyte analysis" && (
        <div>
          <label className={styles.label}>
            What are your electrolyte atoms? (e.g. [Li, OH])
            <span style={{ color: "red" }}>*</span>
          </label>
          <input
            type="text"
            value={electrolyteAtoms}
            onChange={(e) => setElectrolyteAtoms(e.target.value)}
            placeholder="Enter a list of atom symbols" // TODO: replace with better logic than text input for a list
            required
          />
        </div>
      )}

      {/* Adsorption Analysis - Enter Adsorbate Molecules */}
      {primaryPurpose === "Adsorption analysis" && (
        <div>
          <label className={styles.label}>
            What are your adsorbate molecules? (e.g. [H, CO, CO2])
            <span style={{ color: "red" }}>*</span>
          </label>
          <input
            type="text"
            value={adsorbateMolecules}
            onChange={(e) => setAdsorbateMolecules(e.target.value)}
            placeholder="Enter a list of molecules" // TODO: replace with better logic than text input for a list
            required
          />
        </div>
      )}

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
          Would you like to use active learning? (RECOMMENDED)?
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
        <input type="submit" value="Submit" className={styles.button} />
      </div>

      {/* Display success message if available */}
      {successMessage && (
        <div>
          <p className={styles.successMessage}>{successMessage}</p>
        </div>
      )}
    </form>
  );
};

export default WorkflowForm;
