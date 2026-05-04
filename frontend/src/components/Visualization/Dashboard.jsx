import React from 'react';
import { Card, CardHeader, CardContent, Grid } from '@mui/material';
import RiskGauge from './RiskGauge';

const Dashboard = () => {
    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Card>
                    <CardHeader title="Welcome to Telehealth Hypertension Analytics" />
                    <CardContent>
                        <p>Use the sidebar to navigate through different features:</p>
                        <ul>
                            <li><strong>Data Ingestion</strong> - Upload or import your data</li>
                            <li><strong>Data Exploration</strong> - View statistics and correlations</li>
                            <li><strong>Data Cleaning</strong> - Handle missing values and outliers</li>
                            <li><strong>Modeling</strong> - Train and tune predictive models</li>
                            <li><strong>Visualization</strong> - Create charts and dashboards</li>
                            <li><strong>Reporting</strong> - Generate and export reports</li>
                        </ul>
                    </CardContent>
                </Card>
            </Grid>
            <Grid item xs={12} md={6}>
                <Card>
                    <CardHeader title="Risk Assessment" />
                    <CardContent>
                        <RiskGauge riskScore={0} />
                        <p style={{ textAlign: 'center', marginTop: '10px' }}>
                            Upload data to see risk assessment
                        </p>
                    </CardContent>
                </Card>
            </Grid>
            <Grid item xs={12} md={6}>
                <Card>
                    <CardHeader title="Quick Stats" />
                    <CardContent>
                        <p>No data loaded yet. Upload a dataset to get started.</p>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default Dashboard;