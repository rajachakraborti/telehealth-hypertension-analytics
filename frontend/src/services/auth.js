import axios from 'axios';

const API_URL = 'http://localhost:8000/api/auth'; // Update with your backend API URL

// Function to handle user login
export const login = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}/login`, credentials);
        if (response.data.token) {
            localStorage.setItem('token', response.data.token); // Store token in local storage
        }
        return response.data;
    } catch (error) {
        throw new Error('Login failed: ' + error.response.data.message);
    }
};

// Function to handle user logout
export const logout = () => {
    localStorage.removeItem('token'); // Remove token from local storage
};

// Function to check if user is authenticated
export const isAuthenticated = () => {
    return localStorage.getItem('token') !== null; // Check if token exists
};

// Function to get the current user's information
export const getCurrentUser = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_URL}/me`, {
            headers: {
                Authorization: `Bearer ${token}`, // Include token in the request header
            },
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to fetch user information: ' + error.response.data.message);
    }
};