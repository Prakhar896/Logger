const axios = require('axios');

class Logger {
    // Make two static functions
    static log(message, type='normal') {
        console.log(message);

        axios({
            method: 'post',
            url: `${process.env.LOGGER_URL}/newLog`,
            headers: {
                "Content-Type": "application/json",
                "LogsAccessCode": process.env.LOGGER_ACCESS_CODE
            },
            data: {
                "message": message,
                "type": type,
                "clientName": `${process.env.LOGGER_CLIENT_NAME}`
            }
        })
        .then((response) => {
            if (response.status != 200) {
                console.log("Failed to connect to the Logger service. Could not send log message.")
            } else if (response.data != "Log added successfully!") {
                console.log("Failed to add a log successfully! Err: " + response.data)
            }
        })
        .catch(err => {
            console.log("Failed to connect to the Logger service. Err: " + err)
        })
    }
}

// Logger.log("This is a normal log message", "normal");
// Logger.log("This is an error log message", "error");

/* Requirements:
    - Logger service should be active
    - .env file has the following variables:
        - LOGGER_URL
        - LOGGER_ACCESS_CODE
        - LOGGER_CLIENT_NAME
*/