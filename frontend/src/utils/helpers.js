// This file contains utility functions used throughout the frontend application.

export const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

export const calculatePercentage = (part, total) => {
    if (total === 0) return 0;
    return ((part / total) * 100).toFixed(2);
};

export const generateRandomId = () => {
    return '_' + Math.random().toString(36).substr(2, 9);
};

export const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
};

export const isValidURL = (string) => {
    const res = string.match(/(https?:\/\/[^\s]+)/g);
    return (res !== null);
};