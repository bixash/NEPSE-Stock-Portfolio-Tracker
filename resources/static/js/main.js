const header_profile = document.getElementById("profile");
const profile_options = document.getElementById("profile-options");
const search = document.getElementById("search-box");
const search_list = document.getElementById("search-list");
const inputBox = search.querySelector("#company-search");
const resultsDiv = document.getElementById("search-list");


header_profile.addEventListener("click", function () {
  profile_options.style.display = "block";
});

document.addEventListener("click", (event) => {
  if (
    !profile_options.contains(event.target) &&
    !profile.contains(event.target)
  ) {
    profile_options.style.display = "none";
  }
  if (!search_list.contains(event.target) && !search.contains(event.target)) {
    search_list.style.display = "none";
  }
});

inputBox.onkeyup = (e) => {
  var userData = e.target.value;

  if (userData) {
    fetch("/get_company", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ scrip: userData }),
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
};
