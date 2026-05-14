import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Data Exploration
export const fetchSummaryStatistics = async (datasetId) => {
  const response = await api.post('/api/exploration/statistics', { dataset_id: datasetId });
  return response.data;
};

export const fetchDashboard = async (datasetId) => {
  const response = await api.post('/api/exploration/dashboard', { dataset_id: datasetId });
  return response.data;
};

export const fetchDataPreview = async (datasetId) => {
  const response = await api.post('/api/exploration/preview', { dataset_id: datasetId });
  return response.data;
};

export const fetchCorrelationMatrix = async (datasetId) => {
  const response = await api.post('/api/exploration/correlation', { dataset_id: datasetId });
  return response.data;
};

// Pipeline Management
export const fetchWorkflowData = async () => {
  const response = await api.get('/api/pipeline/workflow');
  return response.data;
};

export const startPipeline = async () => {
  const response = await api.post('/api/pipeline/start');
  return response.data;
};

export const stopPipeline = async () => {
  const response = await api.post('/api/pipeline/stop');
  return response.data;
};

export const resetPipeline = async () => {
  const response = await api.post('/api/pipeline/reset');
  return response.data;
};

export const advancePipeline = async () => {
  const response = await api.post('/api/pipeline/advance');
  return response.data;
};

export const fetchPipelineStatus = async () => {
  const response = await api.get('/api/pipeline/status');
  return response.data;
};

// Data Ingestion
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/api/data-ingestion/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const importFromUrl = async (url) => {
  const response = await api.post('/api/data-ingestion/url', { url });
  return response.data;
};

// Data Cleaning
export const imputeData = async (datasetId, method) => {
  const response = await api.post('/api/cleaning/impute', { dataset_id: datasetId, imputation_method: method });
  return response.data;
};

export const cleanData = async (datasetId, options) => {
  const response = await api.post('/api/cleaning/clean', options);
  return response.data;
};

export const detectOutliers = async (datasetId, method = 'iqr') => {
  const response = await api.post('/api/cleaning/detect-outliers', { dataset_id: datasetId, method });
  return response.data;
};

// Modeling
export const fetchModels = async () => {
  const response = await api.get('/api/modeling/models');
  return response.data;
};

export const trainModel = async (modelConfig) => {
  const response = await api.post('/api/modeling/train', modelConfig);
  return response.data;
};

export const fetchAvailableModels = async () => {
  const response = await api.get('/api/modeling/models');
  return response.data;
};

export const getModelPredictions = async (modelId, data) => {
  const response = await api.post(`/api/modeling/${modelId}/predict`, data);
  return response.data;
};

export const fetchHyperparameterOptions = async (modelType) => {
  // Return default hyperparameter options based on model type
  const options = {
    random_forest: {
      n_estimators: [50, 100, 200],
      max_depth: [5, 10, 20, null],
      min_samples_split: [2, 5, 10]
    },
    gradient_boosting: {
      n_estimators: [50, 100, 200],
      learning_rate: [0.01, 0.1, 0.2],
      max_depth: [3, 5, 7]
    },
    logistic_regression: {
      C: [0.1, 1.0, 10.0],
      penalty: ['l1', 'l2']
    },
    xgboost: {
      n_estimators: [50, 100, 200],
      learning_rate: [0.01, 0.1, 0.2],
      max_depth: [3, 5, 7]
    }
  };
  return options[modelType] || {};
};

export const tuneHyperparameters = async (tuningConfig) => {
  const response = await api.post('/api/modeling/tune', tuningConfig);
  return response.data;
};

// Reporting
const downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

export const generateReport = async (datasetId, title) => {
  const response = await api.post(
    '/api/reporting/reports/pdf',
    { dataset_id: datasetId, title },
    { responseType: 'blob' }
  );
  downloadBlob(response.data, 'hypertension_report.pdf');
};

export const exportToCsv = async (datasetId) => {
  const response = await api.post(
    '/api/reporting/reports/csv',
    { dataset_id: datasetId },
    { responseType: 'blob' }
  );
  downloadBlob(response.data, 'hypertension_data.csv');
};

// User Management
export const getUserRoles = async () => {
  const response = await api.get('/api/auth/users/roles');
  return response.data.users;
};

export const updateUserRole = async (userId, role) => {
  const response = await api.put(`/api/auth/users/${userId}/role`, { role });
  return response.data;
};

// Authentication
export const login = async (credentials) => {
  const params = new URLSearchParams();
  params.append('username', credentials.username);
  params.append('password', credentials.password);
  const response = await api.post('/api/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getCurrentUser = async () => {
  const response = await api.get('/api/auth/users/me');
  return response.data;
};

export default api;
