'use client'

// import Visualization from './Visualization';
import Container from 'react-bootstrap/Container';
import { useEffect, useState, useRef } from 'react';
// import * as NGL from 'ngl';
import handleMolData from '../edit/handleMolData';
import MinMainComponent from '../../components/MinMainComponent'; 

const Visualize = () => {
    const viewportRef = useRef(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
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
                setLoading(true);
                console.log("loadAndVisualize is ran")
                await loadScript('https://unpkg.com/ngl@latest/dist/ngl.js');   
                const NGL = window.NGL; // Access the NGL library from the window object

                const molData = await handleMolData(); // Get molecule data from API

                if (viewportRef.current && NGL) {
                    const stage = new NGL.Stage(viewportRef.current);
                    
                    // Assuming molData contains a URL or path to the molecule file
                    stage.loadFile('./LCO_pristine.mol2', { defaultRepresentation: true }).then(component => {
                        component.addRepresentation("cartoon"); // Add a representation
                        component.autoView(); // Automatically adjust the view
                    });
                }
            } catch (error) {
                console.error('Failed to load NGL library:', error);
            } finally {
                setLoading(false);
            }
        };

        loadAndVisualizeMolecule();
    }, []);

// TODO: make Download File Button and Submit Stucture Button
    return (
        <>
            <MinMainComponent />
            <Container style={{ padding: '0', height: '100vh' }}>
                {loading ? (
                    <div style={{ textAlign: 'center', marginTop: '20%' }}>
                        <h1>Processing Structure...</h1>
                    </div>
                ) : (
                    <div ref={viewportRef} style={{ width: '90%', height: '90%' }}></div>
                )}
            </Container>
        </>
    )
  }
  
  export default Visualize;