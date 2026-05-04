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

export const fetchCorrelationMatrix = async (datasetId) => {
  const response = await api.get(`/api/exploration/correlation/${datasetId}`);
  return response.data;
};

// Pipeline Management
export const fetchWorkflowData = async () => {
  const response = await api.get('/api/pipeline/pipeline/status');
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
export const cleanData = async (datasetId, options) => {
  const response = await api.post('/api/cleaning/clean', options);
  return response.data;
};

export const detectOutliers = async (data) => {
  const response = await api.post('/api/cleaning/clean', {
    data,
    outlier_detection: true
  });
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

export const tuneHyperparameters = async (modelConfig) => {
  const response = await api.post('/api/modeling/tune', modelConfig);
  return response.data;
};

// Reporting
export const generateReport = async (reportConfig) => {
  const response = await api.post('/api/reporting/reports/pdf', reportConfig);
  return response.data;
};

export const exportToCsv = async (data) => {
  const response = await api.post('/api/reporting/reports/csv', data);
  return response.data;
};

// User Management
export const getUserRoles = async () => {
  const response = await api.get('/api/auth/users/roles');
  return response.data;
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
