// import { useEffect, useState } from 'react';
// import Button from 'react-bootstrap/Button';
// import { useNavigation } from '../../utils/navigation';

// function LoadingButton() {
//   const [isLoading, setLoading] = useState(false);
//   const { navigateToVisualize } = useNavigation();

//   useEffect(() => {
//     if (isLoading) {
//       // When Button is clicked
//       navigateToVisualize(); // Navigate to visualization page
//       setLoading(false);
//     }
//   }, [isLoading]);

//   const handleClick = () => setLoading(true);

//   return (
//     <Button
//       className="loadingButton"
//       variant="primary"
//       disabled={isLoading}
//       onClick={!isLoading ? handleClick : null}
//     >
//       {isLoading ? 'Loading…' : 'View Visualization'}
//     </Button>
//   );
// }

// export default LoadingButton;