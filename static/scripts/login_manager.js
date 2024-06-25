document.addEventListener("DOMContentLoaded", function () {
  const logoutBtn = document.getElementById('logout-button');

  logoutBtn.addEventListener('click', function () {
    window.location.href = '/logout';
  })
})

// LOGIN BUTTON LISTENER
document.addEventListener('DOMContentLoaded', function () {
  const loginBtn = document.getElementById('login-button');
  const popup = document.getElementById('login-popup');
  const loginForm = document.getElementById('login-form');

  loginBtn.addEventListener('click', function () {
    popup.classList.remove('hidden');
  });

  loginForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const password = document.getElementById('login-input-pass').value;

    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ password: password }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          popup.classList.add('hidden');
          location.reload()
        } else if (data.status === 'invalid_pass') {
          const errorBox = document.getElementById("error-box");
          errorBox.textContent = data.message
        } else {
          const errorBox = document.getElementById("error-box");
          errorBox.textContent = data.message
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });
});