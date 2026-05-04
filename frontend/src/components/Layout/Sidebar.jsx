import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
    const { user } = useAuth();
    const [expanded, setExpanded] = useState({});

    const navLinkClass = ({ isActive }) => isActive ? 'active' : '';

    const toggleSection = (section) => {
        setExpanded(prev => ({ ...prev, [section]: !prev[section] }));
    };

    // Don't render sidebar if user is not authenticated
    if (!user) {
        return null;
    }

    const menuItems = [
        {
            title: 'Data Ingestion',
            key: 'ingestion',
            items: [
                { path: '/data-ingestion/file-upload', label: 'File Upload' },
                { path: '/data-ingestion/url-import', label: 'URL Import' },
            ]
        },
        {
            title: 'Data Exploration',
            key: 'exploration',
            items: [
                { path: '/data-exploration/summary-statistics', label: 'Summary Statistics' },
                { path: '/data-exploration/data-table', label: 'Data Table' },
                { path: '/data-exploration/correlation-matrix', label: 'Correlation Matrix' },
            ]
        },
        {
            title: 'Data Cleaning',
            key: 'cleaning',
            items: [
                { path: '/data-cleaning/imputation', label: 'Imputation' },
                { path: '/data-cleaning/outlier-detection', label: 'Outlier Detection' },
                { path: '/data-cleaning/preprocessing-history', label: 'History' },
            ]
        },
        {
            title: 'Modeling',
            key: 'modeling',
            items: [
                { path: '/modeling/model-selection', label: 'Model Selection' },
                { path: '/modeling/hyperparameter-tuning', label: 'Hyperparameter Tuning' },
                { path: '/modeling/feature-importance', label: 'Feature Importance' },
            ]
        },
        {
            title: 'Visualization',
            key: 'visualization',
            items: [
                { path: '/visualization/dashboard', label: 'Dashboard' },
                { path: '/visualization/chart-builder', label: 'Chart Builder' },
                { path: '/visualization/risk-gauge', label: 'Risk Gauge' },
            ]
        },
        {
            title: 'Reporting',
            key: 'reporting',
            items: [
                { path: '/reporting/report-generator', label: 'Generate Report' },
                { path: '/reporting/export-options', label: 'Export Options' },
            ]
        },
        {
            title: 'Pipeline',
            key: 'pipeline',
            items: [
                { path: '/pipeline/workflow-visualizer', label: 'Workflow' },
                { path: '/pipeline/pipeline-controls', label: 'Controls' },
            ]
        },
        {
            title: 'User Management',
            key: 'user',
            items: [
                { path: '/user-management/role-management', label: 'Role Management' },
            ]
        },
        {
            title: 'Help & Support',
            key: 'help',
            items: [
                { path: '/help', label: 'Documentation' },
            ]
        },
    ];

    return (
        <div className="sidebar">
            <nav>
                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {menuItems.map((menu) => (
                        <li key={menu.key} style={{ marginBottom: '5px' }}>
                            <div
                                onClick={() => toggleSection(menu.key)}
                                style={{
                                    padding: '10px 15px',
                                    cursor: 'pointer',
                                    fontWeight: 'bold',
                                    backgroundColor: expanded[menu.key] ? '#e6f7ff' : 'transparent',
                                    borderRadius: '4px',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center'
                                }}
                            >
                                {menu.title}
                                <span>{expanded[menu.key] ? '▼' : '▶'}</span>
                            </div>
                            {expanded[menu.key] && (
                                <ul style={{ listStyle: 'none', padding: '5px 0 5px 20px', margin: 0 }}>
                                    {menu.items.map((item) => (
                                        <li key={item.path} style={{ marginBottom: '5px' }}>
                                            <NavLink
                                                to={item.path}
                                                className={navLinkClass}
                                                style={({ isActive }) => ({
                                                    display: 'block',
                                                    padding: '8px 12px',
                                                    textDecoration: 'none',
                                                    color: isActive ? '#1890ff' : '#333',
                                                    backgroundColor: isActive ? '#e6f7ff' : 'transparent',
                                                    borderRadius: '4px',
                                                    fontSize: '14px'
                                                })}
                                            >
                                                {item.label}
                                            </NavLink>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </li>
                    ))}
                </ul>
            </nav>
        </div>
    );
};

export default Sidebar;