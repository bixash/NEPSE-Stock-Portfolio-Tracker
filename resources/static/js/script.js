
$(document).ready(function () {
  google.charts.load("current", { packages: ["corechart"] });

  google.charts.setOnLoadCallback(drawSectorChart);
  // google.charts.setOnLoadCallback(drawInstrumentChart);

  google.charts.load("current", { packages: ["bar"] });
  google.charts.setOnLoadCallback(drawHoldingsChart);

  // $.get("/get_holdings_stats", function (data, status) {
  //   document.getElementById(
  //     "result"
  //   ).innerText = `${data.result["invest_value"]}`;
  // });

  function drawSectorChart() {
    $.get("/get_sector_stats", function (response, status) {
      array = response.result;
      const data = google.visualization.arrayToDataTable(array);
      var options = {
        pieHole: 0.5,
      };
      const chart = new google.visualization.PieChart(
        document.getElementById("sectorChart")
      );
      chart.draw(data, options);
    });
  }

  function drawInstrumentChart() {
    $.get("/get_sector_stats", function (response, status) {
      array = response.instrument_stats;
      alert(array);
      const data = google.visualization.arrayToDataTable(array);
      var options = {
        title: "Instrumentwise summary",
        pieHole: 0.5,
      };
      const chart = new google.visualization.PieChart(
        document.getElementById("instrumentChart")
      );
      chart.draw(data, options);
    });
  }

  function drawHoldingsChart() {
    var data = google.visualization.arrayToDataTable([
      ["Year", "Sales", "Expenses", "Profit"],
      ["2014", 1000, 400, 200],
      ["2015", 1170, 460, 250],
      ["2016", 660, 1120, 300],
      ["2017", 1030, 540, 350],
    ]);

    var options = {
      chart: {
        title: "Company Performance",
        subtitle: "Sales, Expenses, and Profit: 2014-2017",
      },
    };

    var chart = new google.charts.Bar(
      document.getElementById("columnchart_material")
    );

    chart.draw(data, google.charts.Bar.convertOptions(options));
  }
});



$.ajax({
  url: "/get_company",
  method: "POST",
  data: { company: company },
  headers: {
    Accept: "application/json",
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
