var modal = document.getElementById("update-modal-block");
var modalTitle = document.getElementsByClassName("modal-head-title")[0];
var modalSubtitle = document.getElementsByClassName("modal-subtitle")[0];
var form = document.getElementById("update-form");
var formGroup = document.getElementsByClassName("form-group")[0];
var span = document.getElementById("close");
span.onclick = function () {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

function modalControl(value, title, subtitle, action, formInner) {}

function changeUsername(username) {
  modalTitle.innerText = "Change your username";
  modalSubtitle.innerText = "Enter a new username and your existing password.";
  form.action = "/profile/change-username";

  formGroup.innerHTML = `
    <div class="input-form">
        <span class="input-label">Username</span>
        <input type="text" class="form-control" id="username" name="username" value="${username}" required/>
    </div>
    <div class="input-form">
        <span class="input-label">Current Password</span>
        <input type="password" class="form-control" id="password" name="password" required/>
    </div>
  `;
  modal.style.display = "block";

  console.log(username);
}

function changeEmail(email) {
  modalTitle.innerText = "Change your email";
  modalSubtitle.innerText = "Enter a new email and your existing password.";
  form.action = "/profile/change-email";
  formGroup.innerHTML = `
    <div class="input-form">
        <span class="input-label">Email</span>
        <input type="email" class="form-control" id="email" name="email" value="${email}" required/>
    </div>
    <div class="input-form">
        <span class="input-label">Current Password</span>
        <input type="password" class="form-control" id="password" name="password" required/>
    </div>
  `;
  modal.style.display = "block";
}

function changePassword() {
  modalTitle.innerText = "Change your password";
  modalSubtitle.innerText = "Enter a new password and your existing password.";
  form.action = "/profile/change-password";
  formGroup.innerHTML = `
    <div class="input-form">
        <span class="input-label">Current Password</span>
        <input type="password" class="form-control" id="password" name="password" required/>
    </div>
    <div class="input-form">
        <span class="input-label">New Password</span>
        <input type="password" class="form-control" id="new_password" name="new_password" required/>
    </div>
   
  `;
  modal.style.display = "block";
}

function deleteData() {
  modalTitle.innerText = "Delete Data";
  modalSubtitle.innerText =
    "Are you sure that you want to delete your data? This will immediately delete your transactions data but you can upload anytime.";
  form.action = "/transactions/delete-data";
  formGroup.innerHTML = `
    <div class="input-form">
        <span class="input-label">Current Password</span>
        <input type="password" class="form-control" id="password" name="password" required/>
    </div>
  `;
  modal.style.display = "block";
}
function deleteAccount() {
  modalTitle.innerText = "Delete Account";
  modalSubtitle.innerText =
    "Are you sure that you want to delete your account? This will immediately log you out of your account and you will not be able to log in again.";

  form.action = "/profile/delete-account";
  formGroup.innerHTML = `
    <div class="input-form">
        <span class="input-label">Current Password</span>
        <input type="password" class="form-control" id="password" name="password" required/>
    </div>
  `;
  modal.style.display = "block";
}


// const urlParams = new URLSearchParams(window.location.search);
// const error = urlParams.get("msg");
// alert("Username updated!");

