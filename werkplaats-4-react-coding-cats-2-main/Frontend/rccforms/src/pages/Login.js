import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL_LOGIN } from '../constants';
import {
  Form,
  FormGroup,
  Input,
  Label,
  Button,
  Col,
  Row,
  Container,
  Card,
  CardBody,
} from 'reactstrap';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const checkLoginStatus = () => {
    // Check if the username is stored in localStorage
    const username = localStorage.getItem('Username');
    setIsLoggedIn(!!username); // Update isLoggedIn state based on the username existence
  };

  useEffect(() => {
    const interval = setInterval(checkLoginStatus, 0); // Run checkLoginStatus every 0 second (realtime)

    return () => {
      clearInterval(interval); // Clean up the interval on component unmount
    };
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();

    axios
      .post(API_URL_LOGIN, { username, password })
      .then((response) => {
        if (response.data.success) {
          setSuccess(response.data.success);
          localStorage.setItem('Username', username);
          localStorage.setItem('Role', response.data.success);
          console.log(response.data.success)
        } else {
          setError(response.data.error);
        }
      })
      .catch((error) => {
        console.log(error);
        setError('An error occurred while logging in. Please try again.');
      });
  };

  return (
    <Container
        style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
    >
      <img
            src="https://www.dyflexis.com/nl/wp-content/uploads/2019/04/logo-dyflexis-2.svg"
            alt="Dyflexis logo"
            style={{
              marginBottom: '25px',
              marginLeft: '-20px',
              width: "220px"
            }}
            />
      <Row>
      <Col>
        {isLoggedIn ? (
          <>
            <h1>Welkom, {localStorage.getItem('Username')}!</h1>
            {/* Add your logged-in content here */}
          </>
        ) : (
          <>
            <Card
                      style={{
                        width: '30em',
                      }}
                  >
                    <CardBody
                        style={{
                          background: 'linear-gradient(146deg, rgba(28,94,173,1) 0%, rgba(75,162,28,1) 100%)'
                        }}
                    >
                      <div
                          style={{padding: '25px'}}
                      >
                      <h2
                          style={{
                            color: 'white',
                            textAlign: 'center',
                            marginBottom: '30px'
                          }}
                      >Login</h2>
            {error && <p>{error}</p>}
            {success && <p>{success}</p>}
            <Form onSubmit={handleSubmit}>
              <FormGroup floating>
                <Input
                              id="user"
                              type="text"
                              name="username"
                              placeholder="Gebruiker"
                              value={username}
                              onChange={handleUsernameChange}
                          />
                          <Label
                              for="user"
                          >Gebruiker</Label>
                        </FormGroup>
                        {' '}
                        <FormGroup
                            floating
                        >
                          <Input
                              type="password"
                              name="password"
                              placeholder="Wachtwoord"
                              value={password}
                              onChange={handlePasswordChange}
                          />
                          <Label
                              for="password"
                          >Wachtwoord</Label>
                        </FormGroup>
                        {' '}
                        <Button
                            type="submit"
                            outline
                            block
                            size="lg"
                            color="light"
                            >
                          Inloggen
                        </Button>
                      </Form>
                        </div>
                    </CardBody>
                  </Card>
                </>
            )}
          </Col>
        </Row>
      </Container>
  );
}

export default LoginPage;
