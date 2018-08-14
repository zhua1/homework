// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);

// When the browser loads, makeResponsive() is called.
makeResponsive();

// The code for the chart is wrapped inside a function that
// automatically resizes the chart
function makeResponsive() {

  // if the SVG area isn't empty when the browser loads,
  // remove it and replace it with a resized version of the chart
  var svgArea = d3.select("body").select("svg");

  // clear svg if not empty
  if (!svgArea.empty()) {
    svgArea.remove();
  }

  // Get SVG height and width in current browser
  var svgWidth = window.innerWidth;
  var svgHeight = window.innerHeight;

  // Manage picture size
  var margin = {top: 40, right: 200, bottom: 70, left: 60};
  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;

  // Append SVG
  var svg = d3
    .select("#scatter")
    .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWidth);

  // Append group element
  var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Read in csv 
  d3.csv("assets/data/data.csv", function(error, graphData) {

    //if (error) throw error;

    // Parse numeric data
    graphData.forEach((d) => {
      d.poverty = +d.poverty;
      d.healthcare = +d.healthcare;
    });

    // Create scales
    var xLinearScale = d3.scaleLinear()
      .domain(d3.extent(graphData, d => d.poverty))
      .range([0, width]);

    var yLinearScale = d3.scaleLinear()
      .domain([0, d3.max(graphData, d => d.healthcare)])
      .range([height, 0]);

    // Create axes
    var xAxis = d3.axisBottom(xLinearScale);
    var yAxis = d3.axisLeft(yLinearScale);

    // Append axes
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis);

    chartGroup.append("g")
      .call(yAxis);

    // Make circles
    var circlesGroup = chartGroup.selectAll("circle")
      .data(graphData)
      .enter()
      .append("circle")
      .attr("cx", d => xLinearScale(d.poverty))
      .attr("cy", d => yLinearScale(d.healthcare))
      .attr("r", "10")
      .attr("fill", "blue")
      .attr("opacity", ".8")
      .attr("stroke-width", "1")
      .attr("stroke", "black");      

    // Append X Axis Name 
    chartGroup.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 15})`)
      .attr("class", "aText")
      .text("In Poverty (%)");

    // Append Y Axis Name
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 12)
      .attr("x", 0 - (height / 2))
      .attr("class", "aText")
      .text("Lacks Healthcare (%)");

    // Put annotation on
    chartGroup.selectAll('text.stateText').data(graphData).enter()
      .append("text")
      .text(d => d.abbr)
      .attr("class", "stateText")
      .attr("x", d => xLinearScale(d.poverty))  
      .attr("y", d => yLinearScale(d.healthcare-.15));  

    // Step 1: Initialize Tooltip
    var toolTip = d3.tip()
      .attr("class", "d3-tip")
      .html(function(d) {
        return (`<strong>${d.state}</strong><br>Poverty %: <strong>${d.poverty}</strong><br>Healthcare %: <strong>${d.healthcare}</strong>`);
      })

    // Step 2: Create the tooltip in chartGroup.
    chartGroup.call(toolTip);

    // Step 3: Create "mouseover" event listener to display tooltip
    circlesGroup.on("mouseover", function(d) {
      toolTip.show(d);
    })

    // Step 4: Create "mouseout" event listener to hide tooltip
      .on("mouseout", function(d) {
      toolTip.hide(d);
    });

  });
};
