/*
* D3 LineChart Control.
* Encapsulated example from: https://bl.ocks.org/mbostock/3883245
* Licence: GNU General Public License, version 3
* Authors: Mike Bostock, Jovan Popovic
**************************************************************************/

var LineChart = function(target, options) {

    options = options || {};
    this.options = options;


var svg = d3.select(target),
    margin = options.margin || {top: 20, right: 20, bottom: 30, left: 50},
    width = (options.width||0)+svg.attr("width") - margin.left - margin.right,
    height = (options.height||0)+svg.attr("height") - margin.top - margin.bottom;

    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%d-%b-%y");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.x); })
    .y(function(d) { return y(d.y); });



this.Data = function(data) {
  x.domain(d3.extent(data, function(d) { return d.x; }));
  y.domain(d3.extent(data, function(d) { return d.y; }));

  g.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
    .select(".domain")
      .remove();

  g.append("g")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Price ($)");

  g.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1.5)
      .attr("d", line);
}

};