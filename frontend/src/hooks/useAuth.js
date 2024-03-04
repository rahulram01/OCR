// useAuth.js
import { useEffect, useContext } from "react";
import AuthContext from "../context/auth-context";

const useAuth = () => {
  const authContext = useContext(AuthContext);

  useEffect(() => {
    // Check local storage for authentication status
    const isAuthenticated = localStorage.getItem("isAuthenticated");

    if (isAuthenticated) {
      authContext.login();
    }
  }, [authContext]);

  return authContext;
};

export default useAuth;
