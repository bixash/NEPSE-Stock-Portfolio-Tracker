var sector = document.getElementById("sector-select")
var instrument = document.getElementById("instrument-select")


// sector.onchange = function(){

//     fetch("/transactions/holdings/"+sector.value+"&"+instrument.value, {
//         method: "GET",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ scrip: inputValue }),
//       })
//         .then((response) => response.json()) // or, resp.text(), etc
//         .then((data) => {

//             `<tr class="table-row"> 
//             <td><span><a class="holdings-scrip" href="/company/{{row['scrip']}}">{{row['scrip']}}</a></span></td>
//             <td><span>{{row['balance_quantity']}}</span></td>
//             <td><span>{{row['previous_closing']}}</span></td>
//             <td><span>{{row['closing_price']}}</span></td>
//             {%if row['difference_rs'] > 0%}
//             <td><span class="text-green">{{row['difference_rs']}}</span></td>
//             {% else%}
//             <td><span class="text-red">{{row['difference_rs']}}</span></td>
//             {%endif%}
//             {%if row['percent_change'] > 0%}
//             <td><span class="text-green">{{row['percent_change']}}%</span></td>
//             {% else%}
//             <td><span class="text-red">{{row['percent_change']}}%</span></td>
//             </tr>`
          
//         })
//         .catch((error) => {
//           console.error(error);
//         });
   
// }

instrument.onchange = function(){
    //  alert("hello");
    location.replace("/holdings/"+`${sector.value}&${instrument.value}`)
    // location.href("/holdings/"+`${sector.value}&${instrument.value}`)
   

}

sector.onchange = function(){
    location.replace("/holdings/"+`${sector.value}&${instrument.value}`)
}