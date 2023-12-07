import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {TextField, Button, Container, Typography, Link, CircularProgress} from '@mui/material';
import {useNavigate} from 'react-router-dom';

interface FormErrors {
    login?: string;
    password?: string;
}


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

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (validate()) {
            setLoading(true);
            let loginInput = {
                user_name: userName,
                password: password
            }
            axios.post<AccessTokenResponse>('/api/users/signin', loginInput).then((response) => {
                localStorage.setItem('accessToken', response.data.access_token);
                navigate(`/`);
            }).catch(() => {
                let tempErrors: FormErrors = {};
                tempErrors.login = "Nome de usuário ou seha inválidos.";
                tempErrors.password = " ";

                setErrors(tempErrors);
            }).finally(() => {
                setLoading(false);
            })
        }
    };

    // Validação
    const [errors, setErrors] = useState<FormErrors>({});

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.login = userName ? "" : "Login é obrigatório";
        tempErrors.password = password ? "" : "Senha é obrigatório";

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    return (
        <Container maxWidth="xs">
            <form onSubmit={handleSubmit}
            >
                <Typography variant="h6" style={{marginTop: '16px'}}>Login</Typography>
                <TextField
                    label="User Name"
                    variant="outlined"
                    fullWidth
                    margin="normal"
                    name="user_name"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    error={Boolean(errors.login)}
                    helperText={errors.login || ""}
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
                    error={Boolean(errors.password)}
                    helperText={errors.password || ""}
                />
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    style={{marginTop: '16px'}}
                >
                    {loading ? <CircularProgress size={24}/> : 'Login'}
                </Button>
                <Typography style={{marginTop: '16px', textAlign: 'center'}}>
                    Não tem uma conta?
                    <Link href="/signup" style={{marginLeft: '5px'}}>
                        Cadastre-se
                    </Link>
                </Typography>
            </form>
        </Container>
    );
};

export default LoginForm;
