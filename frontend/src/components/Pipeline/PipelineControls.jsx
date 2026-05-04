import React from 'react';

const PipelineControls = ({ onStart, onStop, onReset }) => {
    return (
        <div className="pipeline-controls">
            <h2>Pipeline Controls</h2>
            <button onClick={onStart} className="btn btn-primary">Start Pipeline</button>
            <button onClick={onStop} className="btn btn-danger">Stop Pipeline</button>
            <button onClick={onReset} className="btn btn-secondary">Reset Pipeline</button>
        </div>
    );
};

export default PipelineControls;