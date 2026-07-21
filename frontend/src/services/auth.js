export const DEMO_EMAIL = "admin@enterpriseiam.local";
export const DEMO_PASSWORD = "Admin123!";
export const SESSION_KEY = "enterprise-iam-demo-session";

export function getStoredSession() {
  const raw = localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function createDemoSession(remember) {
  const session = {
    email: DEMO_EMAIL,
    name: "Abdulaziz Abdi",
    role: "Administrator",
    environment: "Demo Environment",
    createdAt: new Date().toISOString(),
  };
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(SESSION_KEY, JSON.stringify(session));
  return session;
}

export function clearDemoSession() {
  localStorage.removeItem(SESSION_KEY);
  sessionStorage.removeItem(SESSION_KEY);
}
