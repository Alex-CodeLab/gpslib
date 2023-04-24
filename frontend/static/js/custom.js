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
  colors: ['#44dd66'],

  plotOptions: {
    radialBar: {
    hollow: {
        margin: 5,
        size: "60%"
      },

      startAngle: -135,
      endAngle: 135,
      track: {
        background: '#000099',
        startAngle: -135,
        endAngle: 135,
      },
      track: {
          show: true,
          startAngle: undefined,
          endAngle: undefined,
          background: '#aaa',
          strokeWidth: '17%',
          opacity: .1,
          margin: 5,
          dropShadow: {
              enabled: true,
              top: 0,
              left: 0,
              blur: 10,
              opacity: 8
          }
      },
      dataLabels: {
        name: {
          show: true,
          fontSize: '16px',
          color: '#ddd',
          offsetY: 80
        },
        value: {
          fontSize: "40px",
          color: "#eee",
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
