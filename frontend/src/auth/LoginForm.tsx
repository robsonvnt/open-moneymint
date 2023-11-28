import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Link, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';


interface AccessTokenResponse {
  access_token: string;
}

const LoginForm: React.FC = () => {
  const [userName, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    let token = localStorage.getItem('accessToken');
    if (token) {
      navigate(`/finances`);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      let loginInput = {
        user_name: userName,
        password: password
      }
      const response = await axios.post<AccessTokenResponse>('/api/users/signin', loginInput)
      localStorage.setItem('accessToken', response.data.access_token);

      setTimeout(() => {
        if (localStorage.getItem('accessToken')) {
          setLoading(false);
          navigate(`/finances`);
        }
      }, 1500);


    } catch (error) {
      console.error(error);
      // Tratar o erro aqui (ex.: mostrar uma mensagem ao usuário)
    }
  };

  return (
    <Container maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <Typography variant="h6" style={{ marginTop: '16px' }}>Login</Typography>
        <TextField
          label="User Name"
          variant="outlined"
          fullWidth
          margin="normal"
          name="user_name"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          style={{ marginTop: '16px' }}
        >
          {loading ? <CircularProgress size={24} /> : 'Login'}
        </Button>
        <Typography style={{ marginTop: '16px', textAlign: 'center' }}>
          Não tem uma conta?
          <Link href="/signup" style={{ marginLeft: '5px' }}>
            Cadastre-se
          </Link>
        </Typography>
      </form>
    </Container>
  );
};

export default LoginForm;
