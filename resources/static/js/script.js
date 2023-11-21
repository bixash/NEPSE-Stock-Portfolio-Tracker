$(document).ready(function () {
  $.get("/transactions/get_sector_stats", function (response, status) {
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
        },
      },
    });
  });
});




