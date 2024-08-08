'use client';

function handleMolData() {
  try {
    window.ketcher.getMolfile('v2000').then((molfile) => {
      // Send the molfile to the Flask API and retrieve the output after computation
      fetch(process.env.NEXT_PUBLIC_BASE_URL + '/api/visualize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'molfile': molfile }),
      }).then((response) => {
        return response.json();
      }).then((data) => {
        // Received the data from the Flask API
        window.alert("Received the data from the Flask API");
        console.log(data.output);
        return data.output; // Return the molecule data
      })
    });
    return new Promise((resolve) => setTimeout(resolve, 1000));
  } catch (error) {
    console.error('Error fetching molecule data:', error);
    throw error;
  }
}

export default handleMolData;