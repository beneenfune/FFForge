/*
Form for File Submission
*/
import { useState } from "react";
import styles from "../../styles/Landing.module.css";
import axios from "axios";

const FileForm = () => {
  // Create states for form data
  const [structureFile, setStructureFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState("");

  // Use axios to handle file object
  function handleSubmit(event) {
    event.preventDefault();

    const url = process.env.NEXT_PUBLIC_BASE_URL + "/api/file-input";
    const formData = new FormData();
    formData.append("structureFile", structureFile);

    // Log the formData entries
    for (let pair of formData.entries()) {
      console.log(pair[0] + ": " + pair[1]);
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
          const message = response.data.message;
          const file_name = response.data.fileName;
          setMessage(message);
          setFileName(file_name);

          // Show success message and name of file on console
          console.log(response.data.message);
          console.log(response.data.fileName);
        } else {
          // Handle error if status code is not in the range of 2xx
          throw new Error(`HTTP error: ${response.status}`);
        }
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  }
  // TODO: change the downloaded file as the fileName in the state
  // Function to handle file download
  const handleDownload = () => {
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/api/file-input?filename=${fileName}`;

    axios({
      url: url, // Use the filePath from the state
      method: "GET",
      responseType: "blob", // important to represent file
    })
      .then((response) => {
        // Create file link in browser's memory
        const href = URL.createObjectURL(response.data);

        // Create "a" HTML element with href to file & click
        const link = document.createElement("a");
        link.href = href;
        link.setAttribute("download", fileName);
        document.body.appendChild(link);
        link.click();

        // Clean up "a" element & remove ObjectURL
        if (document.body.contains(link)) {
          document.body.removeChild(link);
        }
        URL.revokeObjectURL(href);
      })
      .catch((error) => {
        console.error("Error downloading file: ", error);
      });
  };

  return (
    <form className={styles.create} onSubmit={handleSubmit}>
      {/* Input button for structure file */}
      <input
        type="file"
        name="structureFile"
        onChange={(e) => setStructureFile(e.target.files[0])}
        required
      />

      {/* Submit button */}
      <div>
        <input type="submit" value="Submit" />
      </div>

      {/* Display the message */}
      {message && <p>{message}</p>}

      {/* Download button, shown only when fileName is available */}
      {fileName && (
        <div>
          <button type="button" onClick={handleDownload}>
            Download File
          </button>
        </div>
      )}
    </form>
  );
};

export default FileForm;
