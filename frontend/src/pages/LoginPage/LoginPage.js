import { useState } from "react";
import { useNavigate } from "react-router-dom";

import CssBaseline from "@mui/material/CssBaseline";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { FadeLoader } from "react-spinners";
import { useSnackbar } from "notistack";

import { useStyles } from "./styles";
import StyledTextField from "../../components/StyledComponents/StyledTextField";
import ButtonContained from "../../components/StyledComponents/ButtonContained";
import httpRequest from "../../httpRequest";

const LoginPage = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const [loading, setLoading] = useState(false);

  const submitHandler = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const email = data.get("email");
    const password = data.get("password");
    setLoading(true);

    try {
      await httpRequest.post("http://localhost:5000/login", {
        email,
        password,
      });

      // If the request is successful, navigate to the home page
      window.location.href = "/";
    } catch (error) {
      setLoading(false);

      // Display an error message
      enqueueSnackbar("Redirecting to the home page", {
        variant: "error",
      });

      // Navigate to the home page
      navigate("/");
    }
  };

  return (
    <Container component="main" maxWidth="xs" className={classes.rootContainer}>
      {loading ? (
        <FadeLoader
          color="#854de0"
          size={50}
          style={{ position: "absolute", top: "40%", left: "50%" }}
        />
      ) : (
        <>
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Typography
              component="h1"
              variant="h4"
              sx={{ fontFamily: "Oxanium, cursive", fontWeight: 600 }}
            >
              LOGIN
            </Typography>
            <Box component="form" onSubmit={submitHandler} sx={{ mt: 1 }}>
              <StyledTextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="off"
                autoFocus
              />
              <StyledTextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="off"
              />
              <ButtonContained
                type="submit"
                fullWidth
                style={{
                  marginTop: 25,
                  marginBottom: 20,
                  fontWeight: 1000,
                }}
              >
                Login
              </ButtonContained>
              <Grid container>
                <Grid item>
                  <Link
                    href="#"
                    variant="body2"
                    sx={{
                      fontFamily: "Oxanium, cursive",
                      fontWeight: 600,
                      color: "#854de0",
                    }}
                    onClick={() => navigate("/register")}
                  >
                    {"Don't have an account? Register"}
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </>
      )}
    </Container>
  );
};

export default LoginPage;
