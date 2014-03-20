var zoomHandler = d3.behavior.zoom().on("zoom", redraw); // Save the Zoom object to use later in resetting the "camera"

function center() {
    var container = d3.select("#container");
    zoomHandler.translate([0, 0]);
    zoomHandler.scale(1);
    container.transition()
        .duration(750)
        .attr("transform", "translate(0, 0) scale(1)");
}

function hide(button) {
    var labels = d3.select("#labels");
    if (button.text == "Hide labels") {
        button.text = "Show labels";
        labels.attr("display", "none");
    } else {
        button.text = "Hide labels";
        labels.attr("display", "");
    }
}

var svgWidth = 0;
var svgHeight = 0;
var startX = 0;
var startY = 0;
var context; // array from json
var removedNodes = [];

// code ran on load
function init() {
    var svg = d3.select("#graph").append("svg").attr("id", "myGraph");
    d3.json("askscience.json",
        function (error, jsonData) {
            var data = jsonData[0];
            context = jsonData[1];

            var viewboxArray = data["viewBox"].split(" ");
            startX = viewboxArray[0];
            startY = viewboxArray[1];
            svgWidth = viewboxArray[2];
            svgHeight = viewboxArray[3];

            svg.attr("width", data["width"])
                .attr("height", data["height"])
                .attr("viewBox", data["viewBox"])
                .call(zoomHandler);

            // append container to hold all the sub-groups
            var container = svg.append("g").attr("id", "container");

            var edges = container.append("g").attr("id", "edges");
            edges.selectAll("path")
                .data(data["edges"])
                .enter()
                .append("path")
                .attr("fill", function (d) {return d["fill"];})
                .attr("stroke-width", function (d) {return d["stroke-width"];})
                .attr("d", function (d) {return d["d"]; })
                .attr("class", function (d) {return d["class"];})
                .attr("stroke", function (d) {return d["stroke"];})

            var arrows = container.append("g").attr("id", "arrows");
            arrows.selectAll("polyline")
                .data(data["arrows"])
                .enter()
                .append("polyline")
                .attr("fill", function (d) {return d["fill"];})
                .attr("class", function (d) {return d["class"];})
                .attr("points", function (d) {return d["points"];})
                .attr("stroke", function (d) {return d["stroke"];});

            var nodes = container.append("g").attr("id", "nodes");
            nodes.selectAll("circle")
                .data(data["nodes"])
                .enter()
                .append("circle")
                .attr("r", function (d) {return d["r"];})
                .attr("fill", function (d) {return d["fill"];})
                .attr("cx", function (d) {return d["cx"];})
                .attr("cy", function (d) {return d["cy"];})
                .attr("class", function (d) {return d["class"];})
                .attr("stroke", function (d) {return d["stroke"];})
                .attr("stroke-width", function (d) {return d["stroke-width"];})
                .on("click", function (d) {showInfo(d);})
                .on("contextmenu", function(d) {removeElement(d);} );

            var labels = container.append("g").attr("id", "labels");
            labels.selectAll("text")
                .data(data["labels"])
                .enter()
                .append("text")
                .attr("font-size", function (d) {return d["font-size"];})
                .attr("x", function (d) {return d["x"];})
                .attr("y", function (d) {return d["y"];})
                .attr("fill", function (d) {return d["fill"];})
                .attr("style", function (d) {return d["style"];})
                .attr("font-family", function (d) {return d["font-family"];})
                .attr("class", function (d) {return d["class"];})
                .text(function (d) {return d["text"];});
                
            
        });
        
    showControls();
}

function redraw() {
    d3.select("#container").attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
}

function helloWorld() {
    console.log("hello world!");
}

function showInfo(d) {
    var elementname = d["class"];
    console.log(elementname);
}

function removeElement (d) {
    d3.event.preventDefault();
    var elementname = d["class"];
    d3.selectAll("." + elementname).attr("display", "none");
    removedNodes.push(elementname);
    updateNodeList();
}



function restoreElement (d, i) {
    removedNodes.splice(i, 1);
    d3.selectAll("." + d).attr("display", "");
    updateNodeList();
}

function restoreElement_NoUpdate(d) {
    d3.selectAll("." + d).attr("display","");
}

function clearList() {
    for (var it = 0; it < removedNodes.length; it++) {
        restoreElement_NoUpdate(removedNodes[it]);
    }
    
    removedNodes.length = 0;
    updateNodeList();
}

function updateNodeList() {
    showNodes();
    var div = d3.select(".list");
    div.selectAll("*").remove();
    
    if (removedNodes.length > 0) {
        div.append("button").attr("type","button").on("click", clearList).html("Clear list");
        div.append("br");
    }
    
    div.append("div").attr("class","list").attr("id","nodeList");
    var list = d3.select("#nodeList");
    
    list.selectAll("a").data(removedNodes).enter()
      .append("a").attr("class", "javascriptlink").text(function(d) { return (d + "\n"); }).on("click", function(d, i) { restoreElement(d, i);} ).append("br");
}

function showControls() {
    d3.selectAll(".sidebar").selectAll("*").remove();
    var page = d3.select("#controls");
    page.append("button").attr("type","button").text("Hide labels").attr("onclick", "hide(this)");
    page.append("button").attr("type","button").text("Center").on("click", center);
}

function showNodes(buttoned) {
    if (buttoned == undefined) {
        buttoned = false;
    }
    
    d3.selectAll(".sidebar").selectAll("*").remove();
    var page = d3.select("#removedNodes");
    page.append("div").attr("class","list");
    if (buttoned) {
        updateNodeList();
    }
}

document.addEventListener("DOMContentLoaded", init);
