import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const { login, user } = useAuth();

    const from = location.state?.from?.pathname || '/';

    // Navigate when user state is set (handles async state update after login)
    useEffect(() => {
        if (user) {
            navigate(from, { replace: true });
        }
    }, [user, from, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await login(username, password);
            // Navigation handled by useEffect above when user state updates
        } catch (err) {
            setError('Invalid username or password. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container" style={{
            maxWidth: '400px',
            margin: '50px auto',
            padding: '30px',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}>
            <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>Login</h2>
            {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        style={{
                            width: '100%',
                            padding: '10px',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            fontSize: '14px'
                        }}
                    />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{
                            width: '100%',
                            padding: '10px',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            fontSize: '14px'
                        }}
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        width: '100%',
                        padding: '12px',
                        backgroundColor: '#1890ff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        fontSize: '16px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        opacity: loading ? 0.7 : 1
                    }}
                >
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
            <p style={{ marginTop: '20px', textAlign: 'center' }}>
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </div>
    );
};

export default Login;