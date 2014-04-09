function init() {
    getSubreddit();
    console.log(SUBREDDIT);
    d3.select("body").append("div").attr("id","log");
    refreshtext();
}

function getSubreddit() {
var SUBREDDIT = window.location.href.split("/");
SUBREDDIT = SUBREDDIT[SUBREDDIT.length-1]; // Get the current URL's final part and set it as the subreddit! It's a hack, but it probably works.
}

function refreshtext() {    
    d3.text("http://localhost:8080/logs/" + SUBREDDIT + ".lock", "text/plain", function(error, text) {
        var lines = text.split("\n");
        if (lines[lines.length-1] == "Done.") {
            window.location.replace("http://localhost:8080/grapher/" + SUBREDDIT);
        }
        d3.select("#log").selectAll("p").data(lines).enter().append("p").text(function(d) { return d } );
        setTimeout(refreshtext, 1000);
    });
}

var SUBREDDIT = window.location.href.split("/");
SUBREDDIT = SUBREDDIT[SUBREDDIT.length -1];
document.addEventListener("DOMContentLoaded", init);
