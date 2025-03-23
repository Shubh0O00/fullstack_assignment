// src/App.js
import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import routes from './pages';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthContext } from './contexts/AuthContext';

function App() {
  const { token } = useContext(AuthContext);

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={routes["/login"]} />
        <Route path="/register" element={routes["/register"]} />
        
        {/* Root Route: redirect based on authentication */}
        <Route 
          path="/" 
          element={ token ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace /> }
        />

        {/* Protected Dashboard Route */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              {routes["/dashboard"]}
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
