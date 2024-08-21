/*
Form for Demo Generator
*/

import { useState } from "react";
import axios from "axios";

const DemoForm = () => {
  // Create states for form data
  const [structName, setStructName] = useState("");
  const [startTemp, setStartTemp] = useState("");
  const [stepTemp, setStepTemp] = useState("");
  const [endTemp, setEndTemp] = useState("");
  const [inFile, setInFile] = useState(null);
  const [dataFile, setDataFile] = useState(null);
  const [slurmFile, setSlurmFile] = useState(null);
  const [zipPath, setZipPath] = useState("");

<<<<<<< HEAD
  // Use axios to handle multiple objects including files
  function handleSubmit(event) {
    event.preventDefault();

    const url = process.env.NEXT_PUBLIC_BASE_URL + "/api/demo_gen";
    const formData = new FormData();
    formData.append("structname", structName);
    formData.append("starttemp", startTemp);
    formData.append("steptemp", stepTemp);
    formData.append("endtemp", endTemp);
    formData.append("infile", inFile);
    formData.append("datafile", dataFile);
    formData.append("slurmfile", slurmFile);

=======
  // Use axios to handlie multiple objects including files
  function handleSubmit(event) {
    event.preventDefault();
    const url = process.env.NEXT_PUBLIC_BASE_URL + "/api/demo_gen";
    const formData = new FormData();
    formData.append("structname", structName);
    formData.append("starttemp", startTemp);
    formData.append("steptemp", stepTemp);
    formData.append("endtemp", endTemp);
    formData.append("infile", inFile);
    formData.append("datafile", dataFile);
    formData.append("slurmfile", slurmFile);

>>>>>>> beneen-files-in-backend
    // Log the formData entries
    for (let pair of formData.entries()) {
      console.log(pair[0] + ": " + pair[1]);
    }

<<<<<<< HEAD
=======
    // https://www.filestack.com/fileschool/react/react-file-upload/
>>>>>>> beneen-files-in-backend
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };

    // Send request to API and handle response
    axios
      .post(url, formData, config)
      // Successful request
      .then((response) => {
        // Handle success
        if (response.status >= 200 && response.status < 300) {
          const zip_path = response.data.zPath;
          setZipPath(zip_path); // Set the zip path in the state
          console.log(response.data.zPath);
        } else {
          // Handle error if status code is not in the range of 2xx
          throw new Error(`HTTP error: ${response.status}`);
        }
      })
      // Fail to make request
      .catch((error) => {
        console.error("Error uploading files: ", error);
      });
  }

  // Function to handle file download
  const handleDownload = () => {
    axios({
      url: zipPath, // Use the zipPath from the state
      method: "GET",
      responseType: "blob", // important
    }).then((response) => {
      // create file link in browser's memory
      const href = URL.createObjectURL(response.data);

      // create "a" HTML element with href to file & click
      const link = document.createElement("a");
      link.href = href;
      link.setAttribute("download", "demo.zip"); // or any other extension
      document.body.appendChild(link);
      link.click();

      // clean up "a" element & remove ObjectURL
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
    });
  };

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
        required
      />

      {/* Input field for STEPS of temperture_range */}
      <label>Temperture Step for the Temperture Range</label>
      <input
        type="number"
        step="0.00001"
        placeholder="Float value"
        onChange={(e) => setStepTemp(e.target.value)}
        value={stepTemp}
        required
      />

      {/* Input field for END of temperture_range  */}
      <label>Ending Temperature for the Temperture Range</label>
      <input
        type="number"
        step="0.00001"
        placeholder="Float value"
        onChange={(e) => setEndTemp(e.target.value)}
        value={endTemp}
        required
      />

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
        <input type="submit" value="Submit"></input>
      </div>

      {/* Download button, shown only when zipPath is available */}
      {zipPath && (
        <div>
          <button type="button" onClick={handleDownload}>
            Download File
          </button>
        </div>
      )}
    </form>
  );
};

export default DemoForm;
