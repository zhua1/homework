var sample = d3.select("#selDataset").property('value');

function buildMetadata(sample) {
  var selec = d3.select("#sample-metadata");
  selec.html("");
  d3.json("/metadata/"+sample).then((dataMeta) => {
    Object.entries(dataMeta).forEach(([key, value]) => {
       var cell = selec.append("h6");
       var txt = key+':'+'\xa0'+value;
       cell.text(txt);
     });
  });
}

function buildCharts(sample) {
  let selec = d3.select("#pie");
  selec.html("");
  d3.json("/plots/"+sample).then((dataSample) => {
    var data = [dataSample];
    var layout = {autosize: true, legend:{x:1, y:.5}};
    Plotly.newPlot("pie", data, layout);
    });
  let selec2 = d3.select("#bubble");
  selec2.html("");
  d3.json("/bubble/"+sample).then((dataSample) => {
    var data2 = [dataSample];
    var layout2 = {autosize: true, showlegend: false};
    Plotly.newPlot("bubble", data2, layout2);
    });
}

function init() {
  // Grab a reference to the dropdown select element
  let selector = d3.select("#selDataset");
  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample) 
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
