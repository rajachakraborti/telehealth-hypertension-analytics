import React from 'react';
import { useEffect, useState } from 'react';
import { fetchWorkflowData } from '../../services/api';

const WorkflowVisualizer = () => {
    const [workflowSteps, setWorkflowSteps] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadWorkflowData = async () => {
            try {
                const data = await fetchWorkflowData();
                setWorkflowSteps(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        loadWorkflowData();
    }, []);

    if (loading) {
        return <div>Loading workflow...</div>;
    }

    if (error) {
        return <div>Error loading workflow: {error}</div>;
    }

    return (
        <div>
            <h2>Workflow Visualizer</h2>
            <ul>
                {workflowSteps.map((step, index) => (
                    <li key={index}>
                        <strong>{step.name}</strong>: {step.description}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default WorkflowVisualizer;