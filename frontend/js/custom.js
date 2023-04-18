const max = 25
function valueToPercent (value) {
  return (value * 100) / max
}
var options1 = {
  chart: {
    height: 280,
    type: "radialBar",
  },
  series: [valueToPercent(20)],
  colors: ['#00ff00'],

  plotOptions: {
    radialBar: {
      startAngle: -135,
      endAngle: 135,
      track: {
        background: '#000',
        startAngle: -135,
        endAngle: 135,
      },
      track: {
          show: true,
          startAngle: undefined,
          endAngle: undefined,
          background: '#f2f2f2',
          strokeWidth: '27%',
          opacity: 1,
          margin: 5,
          dropShadow: {
              enabled: true,
              top: 0,
              left: 0,
              blur: 1,
              opacity: .1
          }
      },
      dataLabels: {
        name: {
          show: true,
          fontSize: '16px',
          color: undefined,
          offsetY: 80
        },
        value: {
          fontSize: "40px",
          show: true,
          formatter: function (val) {
            return val/4
          }
        }
      }
    }
  },
  fill: {

  },
    stroke: {
      dashArray: 2
    },
  labels: ["Kmh"]
};

new ApexCharts(document.querySelector("#chart1"), options1).render();
