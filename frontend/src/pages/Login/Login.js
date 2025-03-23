import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, getUserData } from '../../services/api';
import { AuthContext } from '../../contexts/AuthContext';
import styles from './Login.module.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(username, password);
      const user_data = await getUserData(data.access_token);
      login(data.access_token, user_data);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className={styles.container}>
      <h2>Login</h2>
      {error && <p className={styles.error}>{error}</p>}
      <form onSubmit={handleLogin} className={styles.form}>
        <div className={styles.formGroup}>
          <label>Username:</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
          />
        </div>
        <div className={styles.formGroup}>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div>
        <div className={styles.buttonContainer}>
          <button type="submit" className={styles.button}>Login</button>
          <button 
            type="button" 
            onClick={() => navigate('/register')} 
            className={styles.button}
          >
            Register
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;
