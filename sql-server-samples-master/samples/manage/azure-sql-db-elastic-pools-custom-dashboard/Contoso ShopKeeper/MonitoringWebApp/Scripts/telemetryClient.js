var socket;
$(document).ready(function () {


    if (!Modernizr.websockets) {
        alert("This browser doesn't support HTML5 Web Sockets!");
        return;
    }

    openConnection();

    function openConnection() {
        //Connnect websocket over SSL if host webpage loaded over SSL
        var socketProtocol = location.protocol == "https:" ? "wss:" : "ws:";
        socket = new WebSocket(socketProtocol + "//" + location.host + "/ws");

        socket.addEventListener("open", function (evt) {
            $("#divStatus").append('Connected to the telemetry service...');
        }, false);

        socket.addEventListener("close", function (evt) {
            $("#divStatus").append('Connection to the telemetry service was closed. ' + evt.reason);
        }, false);

        socket.addEventListener("message", function (evt) {
            receiveMessage(evt.data);
        }, false);

        socket.addEventListener("error", function (evt) {
            alert('Error : ' + evt.message);
        }, false);
    }

    function receiveMessage(jsonMessage) {
        var message = JSON.parse(jsonMessage);

        if (message.type == "dm_db_resource_stats")
        {
            updateSelectedDatabaseCharts(message.telemetry);
        } else if (message.type == "resource_stats")
        {
            updateAllDatabasesTable(message.telemetry);
        } else if (message.type == "elastic_pool_resource_stats")
        {
            updatePoolChart(message.telemetry);
        } else if (message.type == "error")
        {
            alert(message.error);
        }


    }

    function updateSelectedDatabaseCharts(telemetry)
    {
        for (var databaseName in telemetry)
        {
            updateDatabaseGauge(databaseName, telemetry[databaseName].EDTUPercent, telemetry[databaseName].EndTime, telemetry[databaseName].EDTULimit);
        }
    }

    function updateAllDatabasesChart(telemetry)
    {
        updateAllDatabasesTable(telemetry);
    }
});