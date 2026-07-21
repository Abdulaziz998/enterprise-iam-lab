import { useMemo, useState } from "react";
import { Eye, EyeOff, LockKeyhole, ShieldCheck } from "lucide-react";
import { DEMO_EMAIL, DEMO_PASSWORD, createDemoSession } from "../services/auth";

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState(DEMO_EMAIL);
  const [password, setPassword] = useState(DEMO_PASSWORD);
  const [remember, setRemember] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const errors = useMemo(() => ({
    email: /\S+@\S+\.\S+/.test(email) ? "" : "Enter a valid email address.",
    password: password.length >= 8 ? "" : "Password must be at least 8 characters.",
  }), [email, password]);
  const invalid = errors.email || errors.password;

  const submit = (event) => {
    event.preventDefault();
    if (invalid) return;
    setLoading(true);
    setError("");
    window.setTimeout(() => {
      if (email === DEMO_EMAIL && password === DEMO_PASSWORD) {
        onLogin(createDemoSession(remember));
      } else {
        setError("The demo credentials did not match. Use the demo account shown on this page.");
        setLoading(false);
      }
    }, 450);
  };

  return (
    <main className="login-shell">
      <section className="login-card" aria-labelledby="login-title">
        <div className="login-brand"><span><ShieldCheck size={22} /></span><div><p className="panel-label">Demo Administrator Access</p><h1 id="login-title">Enterprise IAM</h1></div></div>
        <p className="security-notice">This is a portfolio demo login. Production deployments should use Microsoft Entra ID, Okta, OIDC, or SAML with centralized policy controls.</p>
        <form className="login-form" onSubmit={submit}>
          {error ? <div className="inline-error" role="alert">{error}</div> : null}
          <label className="form-field"><span>Email</span><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} aria-invalid={Boolean(errors.email)} />{errors.email ? <small className="field-error">{errors.email}</small> : null}</label>
          <label className="form-field"><span>Password</span><div className="password-field"><input type={showPassword ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} aria-invalid={Boolean(errors.password)} /><button type="button" aria-label={showPassword ? "Hide password" : "Show password"} onClick={() => setShowPassword((value) => !value)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>{errors.password ? <small className="field-error">{errors.password}</small> : null}</label>
          <label className="checkbox-field"><input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} /> Remember session</label>
          <button type="submit" className="primary-button login-submit" disabled={Boolean(invalid) || loading}><LockKeyhole size={16} /> {loading ? "Signing in..." : "Sign in to demo console"}</button>
        </form>
      </section>
      <aside className="demo-account-panel">
        <p className="panel-label">Demo Account</p>
        <h2>Reviewer credentials</h2>
        <div className="credential-row"><span>Email</span><strong>{DEMO_EMAIL}</strong></div>
        <div className="credential-row"><span>Password</span><strong>{DEMO_PASSWORD}</strong></div>
      </aside>
    </main>
  );
}

export default LoginPage;
