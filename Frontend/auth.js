/**
 * BOOK NEST - AUTHENTICATION JAVASCRIPT
 * Handles login, signup, form validation, and password strength
 */

// API Base URL
const API_URL = 'http://127.0.0.1:8000/api';

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

/**
 * Show error message
 */
function showError(message) {
  const errorDiv = document.getElementById('errorMessage');
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'flex';
    setTimeout(() => {
      errorDiv.style.display = 'none';
    }, 5000);
  }
}

/**
 * Show success message
 */
function showSuccess(message) {
  const successDiv = document.getElementById('successMessage');
  if (successDiv) {
    successDiv.textContent = message;
    successDiv.style.display = 'flex';
    setTimeout(() => {
      successDiv.style.display = 'none';
    }, 3000);
  }
}

/**
 * Show loading state on button
 */
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.classList.add('btn-loading');
    button.dataset.originalText = button.textContent;
    button.textContent = 'Yuklanmoqda...';
  } else {
    button.disabled = false;
    button.classList.remove('btn-loading');
    button.textContent = button.dataset.originalText || button.textContent;
  }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate username format
 */
function isValidUsername(username) {
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
  return usernameRegex.test(username);
}

// ==========================================
// PASSWORD TOGGLE
// ==========================================

function initPasswordToggles() {
  document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', function() {
      const input = this.parentElement.querySelector('input');
      const icon = this.querySelector('i');
      
      if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
    });
  });
}

// ==========================================
// PASSWORD STRENGTH CHECKER
// ==========================================

function checkPasswordStrength(password) {
  let strength = 0;
  
  // Check password length
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  
  // Check for lowercase
  if (/[a-z]/.test(password)) strength++;
  
  // Check for uppercase
  if (/[A-Z]/.test(password)) strength++;
  
  // Check for numbers
  if (/[0-9]/.test(password)) strength++;
  
  // Check for special characters
  if (/[^a-zA-Z0-9]/.test(password)) strength++;
  
  return strength;
}

function updatePasswordStrength(password) {
  const strengthBar = document.querySelector('.strength-bar');
  const strengthText = document.querySelector('.strength-text');
  
  if (!strengthBar || !strengthText) return;
  
  const strength = checkPasswordStrength(password);
  
  strengthBar.className = 'strength-bar';
  
  if (strength <= 2) {
    strengthBar.classList.add('weak');
    strengthText.textContent = 'Zaif';
  } else if (strength <= 4) {
    strengthBar.classList.add('medium');
    strengthText.textContent = "O'rta";
  } else {
    strengthBar.classList.add('strong');
    strengthText.textContent = 'Kuchli';
  }
}

function initPasswordStrength() {
  const passwordInput = document.getElementById('password');
  if (passwordInput) {
    passwordInput.addEventListener('input', function() {
      updatePasswordStrength(this.value);
    });
  }
}

// ==========================================
// LOGIN FUNCTIONALITY
// ==========================================

async function handleLogin(event) {
  event.preventDefault();
  
  const form = event.target;
  const username = form.username.value.trim();
  const password = form.password.value;
  const rememberMe = form.remember?.checked || false;
  const submitBtn = form.querySelector('button[type="submit"]');
  
  // Validation
  if (!username || !password) {
    showError("Iltimos, barcha maydonlarni to'ldiring!");
    return;
  }
  
  setButtonLoading(submitBtn, true);
  
  try {
    const response = await fetch(`${API_URL}/users/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.token) {
      // Store token
      if (rememberMe) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userId', data.user_id);
        localStorage.setItem('username', data.username);
      } else {
        sessionStorage.setItem('authToken', data.token);
        sessionStorage.setItem('userId', data.user_id);
        sessionStorage.setItem('username', data.username);
      }
      
      showSuccess("Muvaffaqiyatli kirdingiz! Bosh sahifaga yo'naltirilmoqda...");
      
      // Redirect to home page after 1.5 seconds
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1500);
    } else {
      showError(data.error || "Login yoki parol noto'g'ri!");
    }
  } catch (error) {
    console.error('Login error:', error);
    showError('Serverga ulanishda xatolik yuz berdi!');
  } finally {
    setButtonLoading(submitBtn, false);
  }
}

// ==========================================
// SIGNUP FUNCTIONALITY
// ==========================================

async function handleSignup(event) {
  event.preventDefault();
  
  const form = event.target;
  const username = form.username.value.trim();
  const email = form.email.value.trim();
  const firstName = form.firstName?.value.trim() || '';
  const lastName = form.lastName?.value.trim() || '';
  const password = form.password.value;
  const confirmPassword = form.passwordConfirm.value;
  const agreeTerms = form.agreeTerms?.checked || false;
  const newsletter = form.newsletter?.checked || false;
  const submitBtn = form.querySelector('button[type="submit"]');
  
  console.log('Signup form submitted:', { username, email, firstName, lastName, agreeTerms, newsletter });
  
  // Validation
  if (!username || !email || !password || !confirmPassword) {
    showError("Iltimos, barcha majburiy maydonlarni to'ldiring!");
    return;
  }
  
  if (!isValidUsername(username)) {
    showError("Username 3-20 ta belgidan iborat bo'lishi kerak va faqat harf, raqam va _ belgilarini o'z ichiga olishi mumkin!");
    return;
  }
  
  if (!isValidEmail(email)) {
    showError("Iltimos, to'g'ri email manzilini kiriting!");
    return;
  }
  
  if (password.length < 8) {
    showError("Parol kamida 8 ta belgidan iborat bo'lishi kerak!");
    return;
  }
  
  if (password !== confirmPassword) {
    showError("Parollar bir-biriga mos emas!");
    return;
  }
  
  if (!agreeTerms) {
    showError("Ro'yxatdan o'tish uchun shartlarga rozilik berishingiz kerak!");
    return;
  }
  
  setButtonLoading(submitBtn, true);
  
  try {
    const response = await fetch(`${API_URL}/users/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        email: email,
        first_name: firstName,
        last_name: lastName,
        password: password,
        newsletter: newsletter
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.token) {
      // Store token
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('userId', data.user_id);
      localStorage.setItem('username', data.username);
      
      showSuccess("Ro'yxatdan muvaffaqiyatli o'tdingiz! Bosh sahifaga yo'naltirilmoqda...");
      
      // Redirect to home page after 1.5 seconds
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1500);
    } else {
      // Handle specific error messages
      if (data.username) {
        showError("Bu username allaqachon band!");
      } else if (data.email) {
        showError("Bu email allaqachon ro'yxatdan o'tgan!");
      } else {
        showError(data.error || "Ro'yxatdan o'tishda xatolik yuz berdi!");
      }
    }
  } catch (error) {
    console.error('Signup error:', error);
    showError('Serverga ulanishda xatolik yuz berdi!');
  } finally {
    setButtonLoading(submitBtn, false);
  }
}

// ==========================================
// LOGOUT FUNCTIONALITY
// ==========================================

async function logout() {
  const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
  
  if (!token) {
    window.location.href = 'login.html';
    return;
  }
  
  try {
    await fetch(`${API_URL}/users/logout/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      }
    });
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    // Clear storage regardless of API response
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    sessionStorage.removeItem('authToken');
    sessionStorage.removeItem('userId');
    sessionStorage.removeItem('username');
    
    window.location.href = 'login.html';
  }
}

// ==========================================
// CHECK AUTH STATUS
// ==========================================

function isAuthenticated() {
  return !!(localStorage.getItem('authToken') || sessionStorage.getItem('authToken'));
}

function getAuthToken() {
  return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
}

function getCurrentUser() {
  return {
    id: localStorage.getItem('userId') || sessionStorage.getItem('userId'),
    username: localStorage.getItem('username') || sessionStorage.getItem('username'),
    token: getAuthToken()
  };
}

// ==========================================
// SOCIAL LOGIN HANDLERS
// ==========================================

function handleGoogleLogin() {
  showError("Google orqali kirish hozircha mavjud emas!");
  // TODO: Implement Google OAuth
}

function handleFacebookLogin() {
  showError("Facebook orqali kirish hozircha mavjud emas!");
  // TODO: Implement Facebook OAuth
}

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
  // Initialize password toggles
  initPasswordToggles();
  
  // Initialize password strength checker
  initPasswordStrength();
  
  // Login form handler
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  // Signup form handler
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', handleSignup);
  }
  
  // Social login buttons
  const googleBtn = document.querySelector('.btn-google');
  if (googleBtn) {
    googleBtn.addEventListener('click', handleGoogleLogin);
  }
  
  const facebookBtn = document.querySelector('.btn-facebook');
  if (facebookBtn) {
    facebookBtn.addEventListener('click', handleFacebookLogin);
  }
  
  // Redirect if already logged in
  if (isAuthenticated() && (window.location.pathname.includes('login.html') || window.location.pathname.includes('signup.html'))) {
    window.location.href = 'index.html';
  }
});

// Export functions for use in other scripts
window.auth = {
  logout,
  isAuthenticated,
  getAuthToken,
  getCurrentUser
};
