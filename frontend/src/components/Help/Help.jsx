import React, { useState } from 'react';

const Help = () => {
    const [activeSection, setActiveSection] = useState('overview');

    const sections = [
        { id: 'overview', title: 'Overview' },
        { id: 'getting-started', title: 'Getting Started' },
        { id: 'data-ingestion', title: 'Data Ingestion' },
        { id: 'data-exploration', title: 'Data Exploration' },
        { id: 'data-cleaning', title: 'Data Cleaning' },
        { id: 'modeling', title: 'Modeling' },
        { id: 'visualization', title: 'Visualization' },
        { id: 'reporting', title: 'Reporting' },
        { id: 'pipeline', title: 'Pipeline Management' },
        { id: 'faq', title: 'FAQ' },
    ];

    const renderContent = () => {
        switch (activeSection) {
            case 'overview':
                return (
                    <div>
                        <h2>Welcome to Telehealth Hypertension Analytics</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            This application is a comprehensive platform for analyzing hypertension data
                            collected through telehealth services. It provides tools for data ingestion,
                            exploration, cleaning, predictive modeling, and reporting.
                        </p>

                        <h3>Key Features</h3>
                        <ul style={{ lineHeight: '2', marginLeft: '20px' }}>
                            <li><strong>Data Ingestion:</strong> Upload CSV, Excel, or JSON files containing patient data</li>
                            <li><strong>Data Exploration:</strong> View statistics, correlations, and data distributions</li>
                            <li><strong>Data Cleaning:</strong> Handle missing values and detect outliers</li>
                            <li><strong>Predictive Modeling:</strong> Train machine learning models to predict hypertension risk</li>
                            <li><strong>Visualization:</strong> Create charts and dashboards for data insights</li>
                            <li><strong>Reporting:</strong> Generate PDF and CSV reports for stakeholders</li>
                        </ul>

                        <div style={{
                            marginTop: '30px',
                            padding: '20px',
                            backgroundColor: '#e6f7ff',
                            borderRadius: '8px',
                            border: '1px solid #91d5ff'
                        }}>
                            <h4 style={{ marginBottom: '10px' }}>💡 Quick Tip</h4>
                            <p>Follow the workflow from left to right in the sidebar: Start with Data Ingestion,
                            then explore, clean, model, visualize, and finally generate reports.</p>
                        </div>
                    </div>
                );

            case 'getting-started':
                return (
                    <div>
                        <h2>Getting Started</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Follow these steps to analyze your hypertension data:
                        </p>

                        <div style={{ marginBottom: '30px' }}>
                            <h3>Step 1: Prepare Your Data</h3>
                            <p>Ensure your data file contains the following recommended columns:</p>
                            <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                                <li>Patient ID</li>
                                <li>Age</li>
                                <li>Systolic Blood Pressure</li>
                                <li>Diastolic Blood Pressure</li>
                                <li>Heart Rate</li>
                                <li>BMI (Body Mass Index)</li>
                                <li>Cholesterol Levels</li>
                                <li>Smoking Status</li>
                                <li>Physical Activity Level</li>
                                <li>Hypertension Diagnosis (target variable)</li>
                            </ul>
                        </div>

                        <div style={{ marginBottom: '30px' }}>
                            <h3>Step 2: Upload Your Data</h3>
                            <p>Navigate to <strong>Data Ingestion → File Upload</strong> and upload your CSV, Excel, or JSON file.</p>
                        </div>

                        <div style={{ marginBottom: '30px' }}>
                            <h3>Step 3: Explore & Clean</h3>
                            <p>Use the Data Exploration tools to understand your data, then clean it using imputation and outlier detection.</p>
                        </div>

                        <div style={{ marginBottom: '30px' }}>
                            <h3>Step 4: Build Models</h3>
                            <p>Select a machine learning algorithm, tune hyperparameters, and train your predictive model.</p>
                        </div>

                        <div style={{ marginBottom: '30px' }}>
                            <h3>Step 5: Generate Reports</h3>
                            <p>Create visualizations and export comprehensive reports for your analysis.</p>
                        </div>
                    </div>
                );

            case 'data-ingestion':
                return (
                    <div>
                        <h2>Data Ingestion</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            The Data Ingestion module allows you to import your hypertension data into the system.
                        </p>

                        <h3>File Upload</h3>
                        <p style={{ marginBottom: '15px' }}>Upload data files directly from your computer.</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li><strong>Supported formats:</strong> CSV, Excel (.xlsx, .xls), JSON</li>
                            <li><strong>Maximum file size:</strong> 50MB</li>
                            <li><strong>Encoding:</strong> UTF-8 recommended</li>
                        </ul>

                        <h3>URL Import</h3>
                        <p style={{ marginBottom: '15px' }}>Import data from a remote URL.</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li>Enter a direct link to a CSV or JSON file</li>
                            <li>Supports public URLs and authenticated endpoints</li>
                        </ul>

                        <div style={{
                            marginTop: '20px',
                            padding: '15px',
                            backgroundColor: '#fff7e6',
                            borderRadius: '8px',
                            border: '1px solid #ffd591'
                        }}>
                            <h4 style={{ marginBottom: '10px' }}>⚠️ Data Privacy Notice</h4>
                            <p>Ensure all patient data is de-identified before uploading.
                            Do not upload data containing personally identifiable information (PII).</p>
                        </div>
                    </div>
                );

            case 'data-exploration':
                return (
                    <div>
                        <h2>Data Exploration</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Explore and understand your dataset before analysis.
                        </p>

                        <h3>Summary Statistics</h3>
                        <p style={{ marginBottom: '15px' }}>View key statistical measures:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li>Mean, Median, Mode</li>
                            <li>Standard Deviation</li>
                            <li>Min/Max values</li>
                            <li>Quartiles (25%, 50%, 75%)</li>
                            <li>Missing value counts</li>
                        </ul>

                        <h3>Data Table</h3>
                        <p style={{ marginBottom: '15px' }}>Browse your data in a paginated table view with sorting and filtering capabilities.</p>

                        <h3>Correlation Matrix</h3>
                        <p style={{ marginBottom: '15px' }}>Visualize relationships between variables:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li>Identify strongly correlated features</li>
                            <li>Detect multicollinearity issues</li>
                            <li>Understand feature relationships</li>
                        </ul>
                    </div>
                );

            case 'data-cleaning':
                return (
                    <div>
                        <h2>Data Cleaning</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Prepare your data for analysis by handling missing values and outliers.
                        </p>

                        <h3>Imputation Methods</h3>
                        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
                            <thead>
                                <tr style={{ backgroundColor: '#fafafa' }}>
                                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Method</th>
                                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Best For</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>Mean</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Normally distributed numerical data</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>Median</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Skewed numerical data with outliers</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>MICE</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Complex patterns with multiple missing variables</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>KNN</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Data with similar observations nearby</td>
                                </tr>
                            </tbody>
                        </table>

                        <h3>Outlier Detection</h3>
                        <p style={{ marginBottom: '15px' }}>Identify and handle outliers using:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li><strong>IQR Method:</strong> Flags values outside 1.5× interquartile range</li>
                            <li><strong>Z-Score:</strong> Identifies values more than 3 standard deviations from mean</li>
                            <li><strong>Isolation Forest:</strong> Machine learning-based anomaly detection</li>
                        </ul>
                    </div>
                );

            case 'modeling':
                return (
                    <div>
                        <h2>Predictive Modeling</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Build machine learning models to predict hypertension risk.
                        </p>

                        <h3>Available Algorithms</h3>
                        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
                            <thead>
                                <tr style={{ backgroundColor: '#fafafa' }}>
                                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Algorithm</th>
                                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #e8e8e8' }}>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>Logistic Regression</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Simple, interpretable baseline model</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>Random Forest</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>Ensemble method, handles non-linear relationships</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>Gradient Boosting</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>High accuracy, good for complex patterns</td>
                                </tr>
                                <tr>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}><strong>XGBoost</strong></td>
                                    <td style={{ padding: '12px', borderBottom: '1px solid #e8e8e8' }}>State-of-the-art performance, handles missing data</td>
                                </tr>
                            </tbody>
                        </table>

                        <h3>Hyperparameter Tuning</h3>
                        <p style={{ marginBottom: '15px' }}>Optimize model performance by adjusting:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li>Number of estimators</li>
                            <li>Learning rate</li>
                            <li>Maximum depth</li>
                            <li>Regularization parameters</li>
                        </ul>

                        <h3>Feature Importance</h3>
                        <p>After training, view which features contribute most to predictions. This helps in:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li>Understanding risk factors</li>
                            <li>Identifying key health indicators</li>
                            <li>Simplifying models by removing unimportant features</li>
                        </ul>
                    </div>
                );

            case 'visualization':
                return (
                    <div>
                        <h2>Visualization</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Create visual representations of your data and model results.
                        </p>

                        <h3>Dashboard</h3>
                        <p style={{ marginBottom: '15px' }}>A comprehensive overview showing:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li>Key metrics at a glance</li>
                            <li>Risk distribution</li>
                            <li>Trend analysis</li>
                        </ul>

                        <h3>Chart Builder</h3>
                        <p style={{ marginBottom: '15px' }}>Create custom visualizations:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li><strong>Bar Charts:</strong> Compare categories</li>
                            <li><strong>Line Charts:</strong> Show trends over time</li>
                            <li><strong>Scatter Plots:</strong> Explore relationships</li>
                            <li><strong>Histograms:</strong> View distributions</li>
                            <li><strong>Pie Charts:</strong> Show proportions</li>
                        </ul>

                        <h3>Risk Gauge</h3>
                        <p>Visual indicator showing predicted hypertension risk level from 0-100%.</p>
                    </div>
                );

            case 'reporting':
                return (
                    <div>
                        <h2>Reporting</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Generate comprehensive reports for stakeholders and documentation.
                        </p>

                        <h3>PDF Reports</h3>
                        <p style={{ marginBottom: '15px' }}>Professional reports including:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li>Executive summary</li>
                            <li>Data overview and statistics</li>
                            <li>Model performance metrics</li>
                            <li>Visualizations and charts</li>
                            <li>Recommendations</li>
                        </ul>

                        <h3>CSV Export</h3>
                        <p style={{ marginBottom: '15px' }}>Export data for further analysis:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li>Cleaned datasets</li>
                            <li>Prediction results</li>
                            <li>Feature importance scores</li>
                            <li>Statistical summaries</li>
                        </ul>
                    </div>
                );

            case 'pipeline':
                return (
                    <div>
                        <h2>Pipeline Management</h2>
                        <p style={{ marginBottom: '20px', lineHeight: '1.8' }}>
                            Create and manage automated analysis workflows.
                        </p>

                        <h3>Workflow Visualizer</h3>
                        <p style={{ marginBottom: '15px' }}>View your analysis pipeline as a flowchart showing:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8', marginBottom: '20px' }}>
                            <li>Data flow between stages</li>
                            <li>Processing status</li>
                            <li>Dependencies between steps</li>
                        </ul>

                        <h3>Pipeline Controls</h3>
                        <p style={{ marginBottom: '15px' }}>Manage your pipelines:</p>
                        <ul style={{ marginLeft: '20px', lineHeight: '1.8' }}>
                            <li><strong>Start/Stop:</strong> Control pipeline execution</li>
                            <li><strong>Schedule:</strong> Set up recurring analyses</li>
                            <li><strong>Monitor:</strong> Track progress and errors</li>
                            <li><strong>Rollback:</strong> Revert to previous states</li>
                        </ul>
                    </div>
                );

            case 'faq':
                return (
                    <div>
                        <h2>Frequently Asked Questions</h2>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: What file formats are supported?</h4>
                            <p>A: CSV, Excel (.xlsx, .xls), and JSON files are supported. CSV is recommended for best compatibility.</p>
                        </div>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: How large can my dataset be?</h4>
                            <p>A: The system supports datasets up to 50MB. For larger datasets, consider sampling or splitting your data.</p>
                        </div>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: Which model should I choose?</h4>
                            <p>A: Start with Logistic Regression for interpretability. For better accuracy, try Random Forest or XGBoost.</p>
                        </div>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: How do I interpret the risk score?</h4>
                            <p>A: The risk score (0-100%) indicates the predicted probability of hypertension. Higher scores suggest greater risk.</p>
                        </div>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: Can I save my analysis?</h4>
                            <p>A: Yes, use the Export Options to save your results as PDF or CSV files.</p>
                        </div>

                        <div style={{ marginBottom: '25px' }}>
                            <h4 style={{ color: '#1890ff' }}>Q: Is my data secure?</h4>
                            <p>A: Data is processed securely and not shared. However, always de-identify patient data before uploading.</p>
                        </div>

                        <div style={{
                            marginTop: '30px',
                            padding: '20px',
                            backgroundColor: '#f6ffed',
                            borderRadius: '8px',
                            border: '1px solid #b7eb8f'
                        }}>
                            <h4 style={{ marginBottom: '10px' }}>📧 Need More Help?</h4>
                            <p>Contact support at <strong>support@telehealth-analytics.com</strong> or visit our documentation portal.</p>
                        </div>
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <h1 style={{ marginBottom: '30px', borderBottom: '2px solid #1890ff', paddingBottom: '10px' }}>
                Help & Documentation
            </h1>

            <div style={{ display: 'flex', gap: '30px' }}>
                {/* Sidebar Navigation */}
                <nav style={{
                    minWidth: '200px',
                    backgroundColor: 'white',
                    padding: '20px',
                    borderRadius: '8px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                    height: 'fit-content',
                    position: 'sticky',
                    top: '84px'
                }}>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                        {sections.map((section) => (
                            <li key={section.id} style={{ marginBottom: '8px' }}>
                                <button
                                    onClick={() => setActiveSection(section.id)}
                                    style={{
                                        width: '100%',
                                        padding: '10px 15px',
                                        textAlign: 'left',
                                        border: 'none',
                                        borderRadius: '4px',
                                        backgroundColor: activeSection === section.id ? '#e6f7ff' : 'transparent',
                                        color: activeSection === section.id ? '#1890ff' : '#333',
                                        fontWeight: activeSection === section.id ? 'bold' : 'normal',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                >
                                    {section.title}
                                </button>
                            </li>
                        ))}
                    </ul>
                </nav>

                {/* Main Content */}
                <main style={{
                    flex: 1,
                    backgroundColor: 'white',
                    padding: '30px',
                    borderRadius: '8px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}>
                    {renderContent()}
                </main>
            </div>
        </div>
    );
};

export default Help;
