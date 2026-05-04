import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout, getCurrentUser } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const userData = await getCurrentUser();
                    setUser(userData);
                } catch (error) {
                    console.error('Failed to get current user:', error);
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        };

        initAuth();
    }, []);

    const login = async (username, password) => {
        const response = await apiLogin({ username, password });
        if (response.access_token) {
            try {
                const userData = await getCurrentUser();
                setUser(userData);
            } catch {
                setUser({ username });
            }
        }
        return response;
    };

    const logout = () => {
        apiLogout();
        setUser(null);
    };

    if (loading) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                fontSize: '18px'
            }}>
                Loading...
            </div>
        );
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export default AuthContext;
