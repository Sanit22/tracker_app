window.onload = function(){
    const fullDate = new Date();
    let [year, month, date] = [fullDate.getFullYear(), fullDate.getMonth() + 1, fullDate.getDate()];
    let time = fullDate.toLocaleTimeString();
    time = time.split(':')
    time = "" + time[0] + ":" + time[1];
    console.log(time);
    if(month < 10){
        month = "0" + month;
    }
    if(date < 10){
        date = "0" + date;
    }
    let datetime = "" + year + "-" + month + "-" + date + "T" + time;
    let datetimeElement = document.getElementById("datetime");
    datetimeElement.value = datetime;
}