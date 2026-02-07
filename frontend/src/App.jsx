import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Home from './pages/Home';
import TrendDetails from './pages/TrendDetails';
import ChatAnalyst from './pages/ChatAnalyst';
import WhatIfSimulator from './pages/WhatIfSimulator';
import Login from './pages/Login';
import Signup from './pages/Signup';
import './App.css';

// Simple Route Protection Wrapper
const RequireAuth = ({ children }) => {
  const auth = localStorage.getItem('auth');
  const location = useLocation();

  if (!auth) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected Routes */}
        <Route path="/" element={
          <RequireAuth>
            <MainLayout />
          </RequireAuth>
        }>
          <Route index element={<Home />} />
          <Route path="details" element={<TrendDetails />} />
          <Route path="details/:trendId" element={<TrendDetails />} />
          <Route path="chat" element={<ChatAnalyst />} />
          <Route path="simulator" element={<WhatIfSimulator />} />
        </Route>

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
