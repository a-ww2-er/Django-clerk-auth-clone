import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import React from "react";
import "../styles/formStyle.css";

function Form({ route, method }) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loginPhase, setLoginPhase] = useState(1);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    try {
      const res = await api.post(route, { username: email, password });
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleContinueWithEmail = (e) => {
    e.preventDefault();
    if (method === "login") {
      setLoginPhase(2);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>{method === "login" ? "Sign in" : "Create your account"}</h1>
        <p className="subtitle">
          {method === "login"
            ? "to continue to the app"
            : "to continue to the app"}
        </p>

        {(method === "register" || loginPhase === 1) && (
          <>
            <button className="social-button github">
              <img
                src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                alt="GitHub"
              />
              Continue with GitHub
            </button>
            <button className="social-button google">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"
                alt="Google"
              />
              Continue with Google
            </button>

            <div className="divider">
              <span>or</span>
            </div>
          </>
        )}

        <form
          onSubmit={
            method === "login" && loginPhase === 1
              ? handleContinueWithEmail
              : handleSubmit
          }
        >
          {method === "register" && (
            <div className="name-fields">
              <div className="form-group">
                <label>First name</label>
                <input
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Last name</label>
                <input
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          {(method === "register" || loginPhase === 1) && (
            <div className="form-group">
              <label>Email address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}

          {(method === "register" || loginPhase === 2) && (
            <div className="form-group">
              <label>Password</label>
              <div className="password-input">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={togglePasswordVisibility}
                >
                  {showPassword ? "👁️" : "👁️‍🗨️"}
                </button>
              </div>
            </div>
          )}

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? "Loading..." : "Continue"}
          </button>
        </form>

        <div className="auth-footer">
          {method === "login" ? (
            <p>
              No account? <a href="/register">Sign up</a>
            </p>
          ) : (
            <p>
              Have an account? <a href="/login">Sign in</a>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Form;
