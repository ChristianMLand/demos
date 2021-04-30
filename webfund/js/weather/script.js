const convert= {
    "f" : c => (9/5 * c + 32).toPrecision(2),
    "c" : f => (5/9 * (f - 32)).toPrecision(3)
}

function toggleTemps(type){
    for(let temp of document.querySelectorAll(".high,.low")){
        temp.innerHTML = convert[type](parseFloat(temp.innerHTML))
    }
}

// function fahrenheit(temp){
//     return (9/5 * temp + 32).toPrecision(2)
// }

// function celsius(temp){
//     return (5/9 * (temp - 32)).toPrecision(3)
// }

// function toggleTemps(type){
//     for(let temp of document.querySelectorAll(".high,.low")){
//         if(type == 'f'){
//             temp.innerHTML = fahrenheit(parseFloat(temp.innerHTML))
//         } else if(type == 'c') {
//             temp.innerHTML = celsius(parseFloat(temp.innerHTML))
//         }
//     }
// }