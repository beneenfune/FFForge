// utils/navigation.js
import { useRouter } from 'next/navigation';

export const useNavigation = () => {
    const router = useRouter();

    const navigateToTextInput = () => {
        router.push('/text-input');
    };

    const navigateToFileInput = () => {
        router.push('/file-input');
    };

    const navigateToKetcher = () => {
        router.push('/edit');
    };

    const navigateToLanding = () => {
        router.push('/landing');
    };

    const navigateToVisualize = () => {
        router.push('/visualize');
    };


    return {
      navigateToTextInput,
      navigateToFileInput,
      navigateToKetcher, 
      navigateToLanding,
      navigateToVisualize,
    };
};
