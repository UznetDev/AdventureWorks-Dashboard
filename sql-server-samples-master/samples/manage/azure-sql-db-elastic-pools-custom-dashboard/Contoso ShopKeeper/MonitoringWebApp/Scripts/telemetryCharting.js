google.charts.load('current', { packages: ['corechart', 'gauge', 'line', 'table'] });
google.charts.setOnLoadCallback(drawCharts);

function drawCharts() {

    drawPoolChart();

    drawLatestPoolTable();

    drawDatabaseGauges();

    drawAllDatabasesTable();
}

var poolChartOptions = {
    hAxis: {
        title: 'Day'
    },
    vAxis: {
        title: 'eDTU'
    },
    legend: {
        position: 'none'
    },
    colors: ['navy'],
    crosshair: {
        color: '#000',
        trigger: 'selection'
    }
};

var poolChart;
function drawPoolChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'datetime');
    data.addColumn('number', 'eDTU');

    poolChart = new google.visualization.LineChart(document.getElementById('pool_linechart'));
    poolChart.draw(data, poolChartOptions);
}

function updatePoolChart(telemetry) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'datetime');
    data.addColumn('number', 'eDTU');

    var sample;
    var rows = [];
    for (var i = 0; i < telemetry.length; i++) {
        sample = telemetry[i];

        var eDTUValue = sample.EDTUPercent / 100.0 * sample.EDTULimit
        rows.push([sample.EndTime, eDTUValue])
    }

    data.addRows(rows);
    poolChart.draw(data, poolChartOptions);

    $('#pool_time').text(sample.EndTime);

    updateLatestPoolTable(sample.EDTUPercent, sample.EDTUPercent / 100.0 * sample.EDTULimit)
}

function drawDatabaseGauges() {

    drawDatabaseGauge('db1', 'soladventureworkscycles', 60);

    drawDatabaseGauge('db2', 'soladventureworkscycles2', 30);

    drawDatabaseGauge('db3', 'soladventureworkscycles3', 55);

    drawDatabaseGauge('db4', 'soladventureworkscycles4', 70);
}

var dbgaugecharts = {};
var dbgaugeoptions = {
    width: 400, height: 120,
    redFrom: 90, redTo: 100,
    yellowFrom: 75, yellowTo: 90,
    minorTicks: 5
};
function drawDatabaseGauge(prefix, databaseName, eDTUPercentValue) {

    var data = google.visualization.arrayToDataTable([
      ['Label', 'Value'],
      ['eDTU %', eDTUPercentValue]
    ]);


    var chart = new google.visualization.Gauge(document.getElementById(prefix + '_gauge'));
    chart.draw(data, dbgaugeoptions);
    $('#' + prefix + '_label').text(databaseName);
    dbgaugecharts[databaseName] = { prefix: prefix, chart: chart };
}

function updateDatabaseGauge(databaseName, eDTUPercentValue, endTime, eDTULimit) {
    var data = google.visualization.arrayToDataTable([
      ['Label', 'Value'],
      ['eDTU %', eDTUPercentValue]
    ]);

    var target = dbgaugecharts[databaseName];
    var chart = target.chart;
    var prefix = target.prefix;
    chart.draw(data, dbgaugeoptions);
    $('#' + prefix + '_time').text(endTime);
    $('#' + prefix + '_eDTU').text(eDTUPercentValue / 100.0 * eDTULimit);
}

var allDatabasesTable;
function drawAllDatabasesTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Database');
    data.addColumn('number', 'eDTU Utilization');

    allDatabasesTable = new google.visualization.Table(document.getElementById('all_databases'));
    allDatabasesTable.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
}

function updateAllDatabasesTable(telemetry) {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Database');
    data.addColumn('number', 'eDTU Utilization');

    for (var databaseName in telemetry) {
        data.addRow([databaseName, telemetry[databaseName].EDTUPercent / 100.0 * telemetry[databaseName].EDTULimit]);
        $('#all_databases_time').text(telemetry[databaseName].EndTime);
    }

    allDatabasesTable.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
}


var latestPoolTable;
function drawLatestPoolTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Metric');
    data.addColumn('number', 'Value');

    latestPoolTable = new google.visualization.Table(document.getElementById('latest_pool'));
    latestPoolTable.draw(data, { showRowNumber: false, width: '100%', height: '100%' });
}

function updateLatestPoolTable(eDTUPercent, eDTU) {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Metric');
    data.addColumn('number', 'Value');

    data.addRows([
        ['eDTU Utilized', eDTU],
        ['eDTU % of pool max', eDTUPercent]
    ]);

    latestPoolTable.draw(data, { showRowNumber: false, width: '100%', height: '100%' });
}