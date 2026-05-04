import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Footer from './components/Layout/Footer';
import FileUpload from './components/DataIngestion/FileUpload';
import URLImport from './components/DataIngestion/URLImport';
import SummaryStatistics from './components/DataExploration/SummaryStatistics';
import DataTable from './components/DataExploration/DataTable';
import CorrelationMatrix from './components/DataExploration/CorrelationMatrix';
import ImputationPanel from './components/DataCleaning/ImputationPanel';
import OutlierDetection from './components/DataCleaning/OutlierDetection';
import PreprocessingHistory from './components/DataCleaning/PreprocessingHistory';
import ModelSelection from './components/Modeling/ModelSelection';
import HyperparameterTuning from './components/Modeling/HyperparameterTuning';
import FeatureImportance from './components/Modeling/FeatureImportance';
import ChartBuilder from './components/Visualization/ChartBuilder';
import Dashboard from './components/Visualization/Dashboard';
import RiskGauge from './components/Visualization/RiskGauge';
import ReportGenerator from './components/Reporting/ReportGenerator';
import ExportOptions from './components/Reporting/ExportOptions';
import WorkflowVisualizer from './components/Pipeline/WorkflowVisualizer';
import PipelineControls from './components/Pipeline/PipelineControls';
import Login from './components/UserManagement/Login';
import Register from './components/UserManagement/Register';
import RoleManagement from './components/UserManagement/RoleManagement';
import Help from './components/Help/Help';

const AppContent = () => {
  const { user } = useAuth();

  return (
    <>
      <Header />
      <Sidebar />
      <main style={{ marginLeft: user ? '220px' : '0' }}>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/help" element={<Help />} />

          {/* Protected routes */}
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/data-ingestion/file-upload" element={<ProtectedRoute><FileUpload /></ProtectedRoute>} />
          <Route path="/data-ingestion/url-import" element={<ProtectedRoute><URLImport /></ProtectedRoute>} />
          <Route path="/data-exploration/summary-statistics" element={<ProtectedRoute><SummaryStatistics /></ProtectedRoute>} />
          <Route path="/data-exploration/data-table" element={<ProtectedRoute><DataTable /></ProtectedRoute>} />
          <Route path="/data-exploration/correlation-matrix" element={<ProtectedRoute><CorrelationMatrix /></ProtectedRoute>} />
          <Route path="/data-cleaning/imputation" element={<ProtectedRoute><ImputationPanel /></ProtectedRoute>} />
          <Route path="/data-cleaning/outlier-detection" element={<ProtectedRoute><OutlierDetection /></ProtectedRoute>} />
          <Route path="/data-cleaning/preprocessing-history" element={<ProtectedRoute><PreprocessingHistory /></ProtectedRoute>} />
          <Route path="/modeling/model-selection" element={<ProtectedRoute><ModelSelection /></ProtectedRoute>} />
          <Route path="/modeling/hyperparameter-tuning" element={<ProtectedRoute><HyperparameterTuning /></ProtectedRoute>} />
          <Route path="/modeling/feature-importance" element={<ProtectedRoute><FeatureImportance /></ProtectedRoute>} />
          <Route path="/visualization/chart-builder" element={<ProtectedRoute><ChartBuilder /></ProtectedRoute>} />
          <Route path="/visualization/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/visualization/risk-gauge" element={<ProtectedRoute><RiskGauge /></ProtectedRoute>} />
          <Route path="/reporting/report-generator" element={<ProtectedRoute><ReportGenerator /></ProtectedRoute>} />
          <Route path="/reporting/export-options" element={<ProtectedRoute><ExportOptions /></ProtectedRoute>} />
          <Route path="/pipeline/workflow-visualizer" element={<ProtectedRoute><WorkflowVisualizer /></ProtectedRoute>} />
          <Route path="/pipeline/pipeline-controls" element={<ProtectedRoute><PipelineControls /></ProtectedRoute>} />
          <Route path="/user-management/role-management" element={<ProtectedRoute><RoleManagement /></ProtectedRoute>} />
        </Routes>
      </main>
      <Footer />
    </>
  );
};

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
};

export default App;
