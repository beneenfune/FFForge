import React from 'react';

const DemoDisplay = ({ response }) => {

  if (!response) {
    return null; // Return null if response is not defined
  }
  
  return (
    <div>
      <h2>Response from Server:</h2>
      <p><strong>Structure Name:</strong> {response.structname}</p>
      <p><strong>Starting Temperature:</strong> {response.starttemp}</p>
      <p><strong>Temperature Step:</strong> {response.steptemp}</p>
      <p><strong>Ending Temperature:</strong> {response.endtemp}</p>
      <p><strong>Message:</strong> {response.message}</p>
    </div>
  );
};

export default DemoDisplay;
