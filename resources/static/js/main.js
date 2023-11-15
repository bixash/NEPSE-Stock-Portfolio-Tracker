const header_profile = document.getElementById("profile");
const profile_options = document.getElementById("profile-options");
const search = document.getElementById("search-box");
const search_list = document.getElementById("search-list");
const inputBox = search.querySelector("#company-search");
const resultsDiv = document.getElementById("search-list");



// function validateInput(){
//   var input_email = document.getElementById('email').value;
//   var input_password = document.getElementById('password').value;
//   var input_username = document.getElementById('username').value;
//   var email = input_email.trim();

// }


header_profile.addEventListener("click", function () {
  profile_options.style.display = "block";
});

document.addEventListener("click", (event) => {
  if (
    !profile_options.contains(event.target) && !header_profile.contains(event.target)
  ) {
    profile_options.style.display = "none";
  }
  if (!search_list.contains(event.target) && !search.contains(event.target)) {
    search_list.style.display = "none";
  } else {
    search_list.style.display = "block";
  }
});

function search_company(inputValue){

  if (inputValue) {
    fetch("/search_company", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ scrip: inputValue }),
    })
      .then((response) => response.json()) // or, resp.text(), etc
      .then((data) => {
        $("#search-list").empty();
  
        if(data.companyList.length > 0){
  
          for (let i = 0; i < data.companyList.length; i++) {
            var symbol = data.companyList[i][0];
            var company_name = data.companyList[i][1];
    
            $("#search-list").append(
              `<a href="/company/${symbol}">${symbol} - ${company_name}</a>`
            );
          }
          search_list.classList.add("active"); //show autocomplete box
        } else {
          search_list.innerHTML = "";
          search_list.classList.remove("active"); //hide autocomplete box
        }
        
      })
      .catch((error) => {
        console.error(error);
      });
    
  } else {
    search_list.innerHTML = "";
    search_list.classList.remove("active"); //hide autocomplete box
  }

}
inputBox.onkeyup = (e) => {
  var userData = e.target.value;
  search_company(userData)
};



