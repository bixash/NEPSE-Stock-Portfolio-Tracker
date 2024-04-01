document.addEventListener("DOMContentLoaded", function () {
  fetch("/transactions/sector-stats")
    .then(response => response.json())
    .then(data => {
      const xValues = data.result.xValues;
      const yValues = data.result.yValues;

      const barColors = [
        "rgba(0, 0, 255, 1.0)",
        "rgba(0, 0, 255, 0.8)",
        "rgba(0, 0, 255, 0.6)",
        "rgba(0, 0, 255, 0.4)",
        "rgba(0, 0, 255, 0.2)",
        "rgba(50, 0, 255, 1.0)",
        "rgba(50, 0, 255, 0.8)",
        "rgba(50, 0, 255, 0.6)",
        "rgba(50, 0, 255, 0.4)",
        "rgba(50, 0, 255, 0.2)",
        "rgba(100, 0, 255, 1.0)",
        "rgba(100, 0, 255, 0.6)",
        "rgba(100, 0, 255, 0.4)",
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
    })
    .catch(error => {
      console.error("Error fetching data:", error);
    });
});
