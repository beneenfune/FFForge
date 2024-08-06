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
        router.push('/ketcher');
    };

    return {
        navigateToTextInput,
        navigateToFileInput,
        navigateToKetcher
    };
};
