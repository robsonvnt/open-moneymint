import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';


interface AccessTokenResponse {
  access_token: string;
}

interface FormErrors {
  userName?: string;
  login?: string;
  password?: string;
  confirPassword?: string;
}

const SignupForm: React.FC = () => {
  const [userName, setUserName] = useState<string>("");
  const [login, setLogin] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirPassword, setConfirPassword] = useState<string>("");
  const navigate = useNavigate();


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      let signupInput = {
        name: userName,
        user_name: login,
        password: password
      }
      if (validate()) {
        console.log("Validou!");
        const response = await axios.post<AccessTokenResponse>('/api/users/signup', signupInput);
        console.log(response);
        navigate(`/login`);
      }else{
        console.log("Erro teste!");
      }

    } catch (error) {
      console.error(error);
      // Tratar o erro aqui (ex.: mostrar uma mensagem ao usuário)
    }
  };

  const [errors, setErrors] = useState<FormErrors>({});

  const validate = (): boolean => {
    let tempErrors: FormErrors = {};
    tempErrors.userName = userName ? "" : "Nome é obrigatório";
    tempErrors.login = login ? "" : "Login é obrigatório";
    tempErrors.password = password ? "" : "Senha é obrigatório";
    tempErrors.confirPassword = confirPassword ? "" : "Confirmação de senha é obrigatório";
    tempErrors.confirPassword = confirPassword == password ? "" : "Confirmação de senha não bate com a senha digitada";

    setErrors(tempErrors);
    return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
  }

  return (
    <Container maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <Typography variant="h6" style={{ marginTop: '16px' }}>Login</Typography>
        <TextField
          label="Nome"
          variant="outlined"
          fullWidth
          margin="normal"
          name="user_name"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          error={Boolean(errors.userName)}
          helperText={errors.userName || ""}
        />
        <TextField
          label="Login"
          variant="outlined"
          fullWidth
          margin="normal"
          name="login"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          error={Boolean(errors.login)}
          helperText={errors.login || ""}
        />
        <TextField
          label="Senha"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={Boolean(errors.password)}
          helperText={errors.password || ""}
        />
        <TextField
          label="Confirme sua senha"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          name="confirm-password"
          value={confirPassword}
          onChange={(e) => setConfirPassword(e.target.value)}
          error={Boolean(errors.confirPassword)}
          helperText={errors.confirPassword || ""}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          style={{ marginTop: '16px' }}
        >
          Criar usuário
        </Button>
      </form>
    </Container>
  );
};

export default SignupForm;
