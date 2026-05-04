import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            await register({
                username: formData.username,
                email: formData.email,
                password: formData.password
            });
            navigate('/login', { state: { message: 'Registration successful! Please login.' } });
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container" style={{
            maxWidth: '400px',
            margin: '50px auto',
            padding: '30px',
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}>
            <h2 style={{ marginBottom: '20px', textAlign: 'center' }}>Register</h2>
            {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Username:</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
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
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
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
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                        minLength={6}
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
                    <label style={{ display: 'block', marginBottom: '5px' }}>Confirm Password:</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
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
                    {loading ? 'Registering...' : 'Register'}
                </button>
            </form>
            <p style={{ marginTop: '20px', textAlign: 'center' }}>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
};

export default Register;
