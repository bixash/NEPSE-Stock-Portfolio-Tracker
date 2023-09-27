const profile = document.getElementById("profile");
const profile_options = document.getElementById("profile-options");
const search = document.getElementById("search-box");
const search_list = document.getElementById("search-list");

search.addEventListener("click", function () {
  search_list.style.display = "block";
});
profile.addEventListener("click", function () {
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

function search_result(data) {
  for (item in data) {
    return item;
  }
}
$("#company-search").keyup(function () {
  var company = $(this).val();
  fetch("/get_company", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ scrip: company }),
  })
    .then((response) => response.json()) // or, resp.text(), etc
    .then((data) => {
      
      document.getElementById("search-list").innerHTML = `
      <a href="#" class="search-item">${data.message[1]}</a>
      <a href="#" class="search-item">${data.message[2]}</a>
      <a href="#" class="search-item">${data.message[3]}</a>
      <a href="#" class="search-item">${data.message[4]}</a>
      `; // handle response data
    })
    .catch((error) => {
      console.error(error);
    });
});
