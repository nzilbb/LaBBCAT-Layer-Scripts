import re
# regular expression for identifying overlaps
overlapPattern = re.compile("[<>]")

# for each turn in the transcript
for turn in transcript.list("turns"):
  if annotator.cancelling: break # cancelled by the user
    
  # there's no immediately preceding segment yet
  lastSegment = None 
  
  # for each word in the turn 
  for word in turn.list("transcript"):
    if annotator.cancelling: break # cancelled by the user   
    
    # if the word is not an overlap
    if overlapPattern.search(word.label) is None:
      # for each phone in the word
      for segment in word.list("segments"):
        # if there's a previous segment
        if lastSegment is not None:
          # tag it
          tag = lastSegment.createTag(thisLayer.id, segment.label)
          log("Tagged segment " + lastSegment.label + " with " + segment.label)
        # remember the immediately preceding segment
        lastSegment = segment
          
    # if the word is an overlap...
    else:
      # ...don't remember the immediately preceding segment
      lastSegment = None
      log("Did not tag segments in word " + word.label)
