"use strict";
var $ = require('jQuery');

var chart_dom;
function formatData(chartData) {
    var labels = [];
    var dataPoints = [];
    for (var i=0; i<chartData.potential_answers.length; i++) {
        labels.push(chartData.potential_answers[i][0]);
        dataPoints.push(chartData.potential_answers[i][1]);
    }
    var data = {
        labels: labels,
        datasets: [
            {data: dataPoints,
            fillColor: '#3389B7'}
        ]
    };
    return data;
}

function updateData() {
    $.get('/question/data/'+questionId, {}, function(chartData) {
        if (window.chartData == chartData) {
            return;
        }
        window.chartData = chartData;

        var numResponses = 0;
        for (var i=0; i<chartData.potential_answers.length; i++) {
            chart_dom.datasets[0].bars[i].value = chartData.potential_answers[i][1];
            numResponses += chartData.potential_answers[i][1];
        }
        $('#num_responses').html(''+numResponses);
        chart_dom.update();
    });
}

function chartDisplay(show) {
    var chartData = window.chartData;
    if (show) {
        $('#show-results').show();
        $('#hide-results').hide();
        for (var i=0; i<chartData.potential_answers.length; i++) {
            chart_dom.datasets[0].bars[i].value = chartData.potential_answers[i][1];
        }
        chart_dom.update()
    } else {
        for (var i=0; i<chartData.potential_answers.length; i++) {
            chart_dom.datasets[0].bars[i].value = 0;
        }
        chart_dom.update()
        $('#show-results').hide();
        $('#hide-results').show();
    }
}


function setupChart() {
    var canvas = document.getElementById('results-chart').getContext('2d');
    chart_dom = new Chart(canvas).Bar(formatData(chartData), {});
    updateData();
    setInterval(updateData, 5000);
    chartDisplay(false);
}
module.exports = {
    setupChart: setupChart,
    chartDisplay: chartDisplay
};
