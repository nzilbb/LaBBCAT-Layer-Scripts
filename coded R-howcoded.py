# Author: Dan Villarreal, daniel.j.villarreal@gmail.com
# Date: 18 Jan 2019
# LaBB-CAT Version: 20190109.1225 
# Layer Scope: segment
# Layer Type: text
# Layer Alignment: none
# Assumes Existing Layers: turns, transcript, segments, coded R-hand, coded R-classifier
#
# Tags rhotic tokens with coding method (by hand vs. by the classifier), to facilitate finding both hand-coded and classifier-coded tokens with a single search.

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
    
    # for each phone in the word
    for segment in word.list("segments"):
      
      # get the "coded R-hand" and "coded R-classifier" tags, if any
      hand = segment.my("coded R-hand")
      auto = segment.my("coded R-classifier")
      
      # if there's a tag on the "coded R-hand" layer
      if hand is not None:
        # and there's a tag on the "coded R-classifier" layer
        if auto is not None:
          # tag as "both"
          tag = segment.createTag(thisLayer.id, "both")
          log("Tagged segment " + segment.label + " with " + tag.label)
        
        # if there's no tag on the "coded R-classifier" layer
        else:
          # tag as "hand"
          tag = segment.createTag(thisLayer.id, "hand")
          log("Tagged segment " + segment.label + " with " + tag.label)
      
      # if there's no tag on the "coded R-hand" layer
      else:
        # if there's a tag on the "coded R-classifier" layer
        if auto is not None:
          # tag as "classifier"
          tag = segment.createTag(thisLayer.id, "classifier")
          log("Tagged segment " + segment.label + " with " + tag.label)
