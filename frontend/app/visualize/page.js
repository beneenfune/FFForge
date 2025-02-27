"use client";

// import Visualization from "./Visualization";
// import Container from "react-bootstrap/Container";
// import { useEffect, useState, useRef } from "react";
// // import * as NGL from 'ngl';
// import handleMolData from "../edit/handleMolData";
import MinMainComponent from "../../components/MinMainComponent";

const Visualize = () => {
//   const [molContent, setMolContent] = useState("");
//   const [isLoading, setLoading] = useState(false);
//   const viewportRef = useRef(null);

//   useEffect(() => {
//     // Load the NGL script dynamically
//     const loadScript = (src) => {
//       return new Promise((resolve, reject) => {
//         const script = document.createElement("script");
//         script.src = src;
//         script.onload = resolve;
//         script.onerror = reject;
//         document.body.appendChild(script);
//       });
//     };

//     const loadAndVisualizeMolecule = async () => {
//       try {
//         // Load NGL library
//         await loadScript("https://unpkg.com/ngl@0.10.4-1");
//         // Handle mol data here, attempt to visualize it with ngl.js script

//         if (isLoading) {
//           // When Button is clicked
//           handleMolData()
//             .then((output) => {
//               // use output data here
//               setMolContent(output);
//               setLoading(false);

//               // Ensure the viewport exists before initializing NGL
//               if (viewportRef.current && (typeof window !== "undefined")) {
//                 const stage = new window.NGL.Stage(viewportRef.current);
//                 // Load the molecule file and visualize it
//                 stage.loadFile(molContent).then(function (component) {
//                   component.addRepresentation("cartoon");
//                   component.autoView();
//                 });
//               }
//             })
//             .catch((error) => {
//               console.error("Error during molecule data handling:", error);
//               setLoading(false);
//             });
//         }
//       } catch (error) {
//         console.error("Failed to load NGL script:", error);
//       }
//     };

//     // Call the function to load and visualize the molecule
//     loadAndVisualizeMolecule();
//   }, []);

//   // Send mol file data fine, not visualizing it
//   //   const fetchHtml = async () => {
//   //     try {
//   //       const response = await fetch("/api/getfile/index.html");
//   //       if (response.ok) {
//   //         const resp = await response.json();
//   //         setHtmlContent(resp.content);
//   //       } else {
//   //         console.error("Failed to fetch HTML content");
//   //       }
//   //     } catch (error) {
//   //       console.error("Error fetching HTML content:", error);
//   //     }
//   //   };

//   //   fetchHtml();
//   // }, []);

//   // TODO: make Download File Button and Submit Stucture Button
  return (
    <>
      <MinMainComponent />
      {/* <div
        ref={viewportRef}
        style={{ width: "400px", height: "300px" }}
        id="viewport"
      ></div> */}
      <div>Page Under Construction. Please try again later.</div>
    </>
  );
};

export default Visualize;
