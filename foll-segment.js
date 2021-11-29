// Author: Dan Villarreal, d.vill@pitt.edu
// Date: 29 Nov 2021
// LaBB-CAT Version: 20210601.1528
// Layer Scope: segment
// Layer Type: phonological
// Layer Alignment: none
// Assumes Existing Layers: turns, transcript, segments
// 
// Tags the segment with the following segment, unless interrupted by an overlap marked by angle brackets. Does not tag across turn boundaries

// regular expression for identifying overlaps
let overlapPattern = /[<>]/;

// for each turn in the transcript
for each (turn in transcript.list("turns")) {
  if (annotator.cancelling) break; // cancelled by the user
    
  // there's no immediately preceding segment yet
  var lastSegment = null;
  
  // for each word in the turn 
  for each (word in turn.list("transcript")) {
    if (annotator.cancelling) break; // cancelled by the user   
    
    // if the word is not an overlap
	if (word.label.match(overlapPattern) == null) {
      // for each phone in the word
      for each (segment in word.list("segments")) {
        // if there's a previous segment...
        if (lastSegment != null) {
          // ...tag the previous segment with the current segment label
          var tag = lastSegment.createTag(thisLayer.id, segment.label);
          log("Tagged segment " + lastSegment.label + " with " + segment.label);
		}
		
        // remember the immediately preceding segment
        var lastSegment = segment;
	  }
    // if the word is an overlap...
    } else {
      // ...don't remember the immediately preceding segment
      var lastSegment = null;
      log("Did not tag segments in word " + word.label);
	}
  }
}