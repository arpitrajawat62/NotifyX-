document.addEventListener("DOMContentLoaded", function () {

  // Get elements
  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");

  const loginBtns = document.querySelectorAll(".open-login");
  const registerBtns = document.querySelectorAll(".open-register");

  const closeLogin = document.getElementById("closeModal");
  const closeRegister = document.getElementById("closeRegister");

  // ---- OPEN MODALS ----
  loginBtns.forEach(btn => {
    btn.onclick = function (e) {
      e.preventDefault();
      loginModal.classList.remove("hidden");
    };
  });

  registerBtns.forEach(btn => {
    btn.onclick = function (e) {
      e.preventDefault();
      registerModal.classList.remove("hidden");
    };
  });

  // ---- CLOSE MODALS ----
  closeLogin.onclick = () => loginModal.classList.add("hidden");
  closeRegister.onclick = () => registerModal.classList.add("hidden");

  // ---- CLICK OUTSIDE ----
  window.onclick = function (e) {
    if (e.target === loginModal) {
      loginModal.classList.add("hidden");
    }
    if (e.target === registerModal) {
      registerModal.classList.add("hidden");
    }
  };

  // ---- LOGIN ----
  const loginForm = document.getElementById("loginForm");

  loginForm.onsubmit = async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const data = await loginUser(username, password);
      localStorage.setItem("token", data.access_token);
      window.location.href = "dashboard.html";
    } catch (err) {
      alert("Login failed");
    }
  };

  // ---- REGISTER ----
  const registerForm = document.getElementById("registerForm");

  registerForm.onsubmit = async function (e) {
    e.preventDefault();

    const user = {
      username: document.getElementById("reg_username").value,
      first_name: document.getElementById("reg_first_name").value,
      last_name: document.getElementById("reg_last_name").value,
      email: document.getElementById("reg_email").value,
      password: document.getElementById("reg_password").value
    };

    try {
      await registerUser(user);
      alert("Account created");

      registerModal.classList.add("hidden");
      loginModal.classList.remove("hidden");

    } catch (err) {
      alert("Register failed");
    }
  };

});