// src/pages/Home/Home.js
import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';

function Home() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      // If logged in, go to Dashboard.
      navigate('/dashboard', { replace: true });
    } else {
      // If not logged in, redirect to Login.
      navigate('/login', { replace: true });
    }
  }, [token, navigate]);

  // Optionally, return a loading indicator.
  return <div>Loading...</div>;
}

export default Home;
