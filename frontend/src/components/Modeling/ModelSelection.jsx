import React, { useState, useEffect } from 'react';
import { fetchModels, trainModel } from '../../services/api';

const ModelSelection = () => {
    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState(null);
    const [trainingStatus, setTrainingStatus] = useState('');

    useEffect(() => {
        const loadModels = async () => {
            try {
                const response = await fetchModels();
                setModels(response.data);
            } catch (error) {
                console.error('Error fetching models:', error);
            }
        };

        loadModels();
    }, []);

    const handleModelSelection = (event) => {
        setSelectedModel(event.target.value);
    };

    const handleTrainModel = async () => {
        if (!selectedModel) {
            alert('Please select a model to train.');
            return;
        }

        setTrainingStatus('Training in progress...');
        try {
            await trainModel(selectedModel);
            setTrainingStatus('Model trained successfully!');
        } catch (error) {
            console.error('Error training model:', error);
            setTrainingStatus('Error training model. Please try again.');
        }
    };

    return (
        <div>
            <h2>Select a Model for Training</h2>
            <select onChange={handleModelSelection} value={selectedModel}>
                <option value="" disabled>Select a model</option>
                {models.map((model) => (
                    <option key={model.id} value={model.name}>
                        {model.name}
                    </option>
                ))}
            </select>
            <button onClick={handleTrainModel}>Train Model</button>
            {trainingStatus && <p>{trainingStatus}</p>}
        </div>
    );
};

export default ModelSelection;