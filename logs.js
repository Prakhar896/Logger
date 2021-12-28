axios({
    method: 'post',
    url: `${location.origin}/getLogs`,
    headers: {
        "LogsAccessCode": "prA6h@Log!21"
    },
    data: {}
})
.then(logsArray => {
    if (logsArray.status == 200) {
        var loopIndex = 0
        logsArray.data.forEach(log => {
            const rawJSONDataOfLog = log[loopIndex]

            const paraElem = document.createElement("p");
            paraElem.innerHTML = `${rawJSONDataOfLog.text}, Type: ${rawJSONDataOfLog.type}, Client: ${rawJSONDataOfLog.clientName}`;
            document.getElementById("logsList").appendChild(paraElem);
            loopIndex++
        })
    } else {
        console.log("Error in getting logs: " + logsArray.data)
    }
})
.catch(err => {
    console.log("Error in getting logs: " + err)
})