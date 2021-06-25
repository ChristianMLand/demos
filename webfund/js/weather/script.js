const convert= {
    "C" : f => (5/9 * (f - 32)).toPrecision(3),
    "F" : c => (9/5 * c + 32).toPrecision(2),
}
function toggleTemps(type){
    for(let el of document.querySelectorAll(".high,.low")){
        el.innerHTML = convert[type](parseFloat(el.innerHTML))
    }
}

// function fahrenheit(temp){
//     return (9/5 * temp + 32).toPrecision(2)
// }

// function celsius(temp){
//     return (5/9 * (temp - 32)).toPrecision(3)
// }

// function toggleTemps(type){
//     for(let el of document.querySelectorAll(".high,.low")){
//         if(type == 'f'){
//             el.innerHTML = fahrenheit(parseFloat(el.innerHTML))
//         } else if(type == 'c') {
//             el.innerHTML = celsius(parseFloat(el.innerHTML))
//         }
//     }
// }