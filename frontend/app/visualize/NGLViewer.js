'use client';

import { useEffect, useRef } from 'react';

const NGLViewer = () => {
    const viewportRef = useRef(null);
    const molfile = 

    useEffect(() =>{
        const loadScript = (src) => {
            return new Promise((resolve, reject) => {
              const script = document.createElement('script');
              script.src = src;
              script.onload = resolve;
              script.onerror = reject;
              document.body.appendChild(script);
            });
          }; 
        
          const loadAndVisualizeMolecule = async () => {
            try {
              // Load NGL library
              await loadScript('../../public/ngl.js');  
      
              // Ensure the viewport exists before initializing NGL
              if (viewportRef.current) {
                const stage = new window.NGL.Stage(viewportRef.current);

                try {
                    const response = await fetch("/api/getfile/LCO_pristine.mol2");
                    if (response.ok) {
                      const resp = await response.json();
                      setHtmlContent(resp.content);
                    } else {
                      console.error("Failed to fetch HTML content");
                    }
                  } catch (error) {
                    console.error("Error fetching HTML content:", error);
                  }
                };
            
                // Load the molecule file and visualize it
                stage.loadFile('/temp/LCO_pristine.mol2').then(function (component) {
                  component.addRepresentation('cartoon');
                  component.autoView();
                });
              }
            } catch (error) {
              console.error('Failed to load NGL script:', error);
            }
          };
    })
}