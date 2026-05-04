import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

const Header = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <header className="header">
            <div className="logo">
                <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
                    <h1>Telehealth Hypertension Analytics</h1>
                </Link>
            </div>
            <nav className="navigation">
                <ul>
                    <li><Link to="/">Home</Link></li>
                    {user ? (
                        <>
                            <li><Link to="/data-ingestion/file-upload">Data</Link></li>
                            <li><Link to="/modeling/model-selection">Models</Link></li>
                            <li><Link to="/reporting/report-generator">Reports</Link></li>
                            <li><Link to="/help">Help</Link></li>
                            <li>
                                <span style={{ marginRight: '10px' }}>Welcome, {user.username || 'User'}</span>
                                <button onClick={handleLogout} style={{
                                    background: 'transparent',
                                    border: '1px solid white',
                                    color: 'white',
                                    padding: '5px 10px',
                                    cursor: 'pointer',
                                    borderRadius: '4px'
                                }}>
                                    Logout
                                </button>
                            </li>
                        </>
                    ) : (
                        <>
                            <li><Link to="/help">Help</Link></li>
                            <li><Link to="/login">Login</Link></li>
                        </>
                    )}
                </ul>
            </nav>
        </header>
    );
};

export default Header;