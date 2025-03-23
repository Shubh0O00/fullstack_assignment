import React from 'react';
import Home from './Home/Home';
import Login from './Login/Login';
import Register from './Register/Register';
import Dashboard from './Dashboard/Dashboard';

const routes = {
  '/': <Home />,
  '/login': <Login />,
  '/register': <Register />,
  '/dashboard': <Dashboard />,
};

export default routes;
