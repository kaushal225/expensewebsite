

function show_chart(labels,data){//const ctx = document.getElementById('myChart');
    var ctx = document.querySelector('#myChart').getContext('2d'); // 2d context
    //ctx='mychart'
    console.log(ctx)
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: labels,
          data: data,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
        ,
        titles:{
            display:true,
            text:'income per category'
        }
      }
    });
  
}

fetch('/income/income-category-summary',{
  method:'POST'
}).then(data=>data.json()).then((result)=>{
        console.log(result);
        const category_data=result.income_category_data;
        [label,data]=[Object.keys(category_data),Object.values(category_data)]
        show_chart(label,data)
    }

    );


