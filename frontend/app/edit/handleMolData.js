// function handleMolData() {
//   try {
//     return window.ketcher.getMolfile('v2000').then((molfile) => {
//       return fetch(process.env.NEXT_PUBLIC_BASE_URL + '/api/visualize', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ 'molfile': molfile }),
//       }).then((response) => {
//         return response.json();
//       }).then((data) => {
//         console.log(data.output);
//         return data.output; // Return the molecule data
//       });
//     });
//   } catch (error) {
//     console.error('Error fetching molecule data:', error);
//     throw error;
//   }
// }
