async function handleLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorMsg = document.getElementById("errorMsg");
  errorMsg.classList.add("d-none");
  errorMsg.textContent = "";

  try {
    const token = await loginUser(username, password);
    localStorage.setItem("countries_token", token);
    alert("Login successful! Token saved.");
    // Optionally redirect
    window.location.href = "countries.html";
  } catch (error) {
    errorMsg.textContent = error.message;
    errorMsg.classList.remove("d-none");
  }
}

async function loginUser(username, password) {
  const response = await fetch("http://localhost:8000/api/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error("Invalid credentials");
  }

  const data = await response.json();
  return data.access;
}

async function handleSignup() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const msgBox = document.getElementById("msg");
  msgBox.classList.add("d-none");
  msgBox.textContent = "";

  try {
    const response = await fetch("http://localhost:8000/api/sign-up", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "Sign-up failed. Try a different username."
      );
    }

    msgBox.textContent = "Sign-up successful! You can now log in.";
    msgBox.classList.remove("d-none");
    msgBox.classList.remove("text-danger");
    msgBox.classList.add("text-success");

    window.location.href = "/Client/login.html";
  } catch (error) {
    msgBox.textContent = error.message;
    msgBox.classList.remove("d-none");
    msgBox.classList.add("text-danger");
  }
}
