new Chart(document.getElementById("chart"), 
        {
          type: 'line',
          data: 
          {
            labels :{{timestamps|safe}},
            datasets: 
            [
              {
              data : {{data|safe}}, 
              label : '{{val|safe}}',
              borderColor: "#3e95cd",
              fill: true
              }
            ]
          },
          options: 
          {
            title: 
            {
              display: true,
              text: 'Stock Prices over the past 1 day'
            },
            hover: 
            {
            mode: 'index',
            intersect: true
            },
          }
        });