/*
* D3 BarChart Control.
* Encapsulated example from: https://bl.ocks.org/mbostock/3885304
* Licence: GNU General Public License, version 3
* Authors: Mike Bostock, Jovan Popovic
**************************************************************************/

var BarChart = function(target, options) {

    options = options || {};
    this.options = options;

var svg = d3.select(target),
    margin = options.margin || {top: 20, right: 20, bottom: 30, left: 40},
    width = (options.width||0)+svg.attr("width") - margin.left - margin.right,
    height = (options.height||0)+svg.attr("height") - margin.top - margin.bottom;

var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().rangeRound([height, 0]);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


this.Data = function(data) {

  x.domain(data.map(function(d) { return d.x; }));
  y.domain([0, d3.max(data, function(d) { return d.y; })]);

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).ticks(10, "%"))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Frequency");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.y); });
}

};




