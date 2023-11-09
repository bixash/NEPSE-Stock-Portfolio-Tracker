$(document).ready(function () {
  $.get("/get_sector_stats", function (response, status) {
    array = response.result;
    

    var xValues = array.xValues;
    var yValues = array.yValues;

    var barColors = [
      "rgba(0,0,255,1.0)",
      "rgba(0,0,255,0.8)",
      "rgba(0,0,255,0.6)",
      "rgba(0,0,255,0.4)",
      "rgba(0,0,255,0.2)",
      "rgba(50,0,255,1.0)",
      "rgba(50,0,255,0.8",
      "rgba(50,0,255,0.6)",
      "rgba(50,0,255,0.4)",
      "rgba(50,0,255,0.2)",
      "rgba(100,0,255,1.0)", 
      "rgba(100,0,255,0.6)", 
      "rgba(100,0,255,0.4)",
      
   
     
    ];

    new Chart("sectorChart", {
      type: "doughnut",
      data: {
        labels: xValues,
        datasets: [
          {
            backgroundColor: barColors,
            data: yValues,
          },
        ],
      },
      options: {
        title: {
          display: false,
          // text: "World Wide Wine Production"
        },
      },
    });
  });

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




