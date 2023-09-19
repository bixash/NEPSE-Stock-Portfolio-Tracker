

  $("#company").keyup(function () {
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
        document.getElementById(
          "result"
        ).textContent = `${data.message}`;// handle response data
      })
      .catch((error) => {
        console.error(error);
      });
  });


$.ajax({
  url: "/get_company",
  method: "POST",
  data: { "company": company },
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
  },
  success: function (response) {
    $("#result").html(response);
  },
});

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

