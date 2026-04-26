// auth.js — FINAL stable version (localStorage-based auth)

// =====================
// REGISTER
// =====================
function registerUser({ name, email, password }) {
  if (!name || !email || !password) {
    return { success: false, message: "All fields are required." };
  }

  const users = JSON.parse(localStorage.getItem("wheatshield_users") || "{}");

  if (users[email]) {
    return { success: false, message: "Email already registered." };
  }

  const user = {
    id: Date.now(),
    name,
    email,
    password
  };

  users[email] = user;
  localStorage.setItem("wheatshield_users", JSON.stringify(users));

  return { success: true };
}

// =====================
// LOGIN
// =====================
function loginUser(email, password) {
  const users = JSON.parse(localStorage.getItem("wheatshield_users") || "{}");
  const user = users[email];

  if (!user || user.password !== password) {
    return { success: false, message: "Invalid email or password." };
  }

  localStorage.setItem("wheatshield_user", JSON.stringify(user));
  return { success: true };
}

// =====================
// LOGOUT
// =====================
function logout() {
  localStorage.removeItem("wheatshield_user");
  window.location.href = "login.html";
}

// =====================
// AUTH GUARD (PROTECTED PAGES ONLY)
// =====================
function requireAuth() {
  const raw = localStorage.getItem("wheatshield_user");
  if (!raw) {
    window.location.href = "login.html";
  }
}


