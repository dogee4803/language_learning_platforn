import { ref } from 'vue';

const isAuthenticated = ref(!!localStorage.getItem('token'));

export const useAuth = () => {
    const setAuthenticated = (value) => {
        isAuthenticated.value = value;
    };

    return {
        isAuthenticated,
        setAuthenticated
    };
};
