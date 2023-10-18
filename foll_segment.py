#
# foll_segment
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 18 Oct 2023
# LaBB-CAT Version: 20231002.1520
# Layer Scope: segment
# Layer Type: phonological
# Layer Alignment: intervals
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Annotate segment with the segment that follows it (defined to include
#     following segment across word boundaries, but not across turn boundaries
#     or pauses)
#
# inputLayer: turn
# inputLayer: word
# inputLayer: segment
# outputLayer: foll_segment

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    log("In word " + word.label + " (" + '%.3f' % word.getStart().getOffset() + "-" + '%.3f' % word.getEnd().getOffset() + "s):")
    
    ##For each segment in the word
    for segment in word.list("segment"):
      if annotator.cancelling: break # cancelled by the user
      
      ##If non-word-final...
      if word.end != segment.end:
        ##Tag with following segment, if it exists
        nextSeg = segment.next
        if nextSeg is not None:
          nextSegLabel = nextSeg.label
          tag = segment.createTag("foll_segment", nextSegLabel)
          log("  Tagged word-internal segment " + segment.label + " with " + nextSegLabel)
      
      ##If word final...
      else:
        ##Determine if next word exists in turn
        nextWord = word.next
        if nextWord is not None:
          ##Only proceed if no pause
          if word.end == nextWord.start:
            ##Determine if next word has a first segment
            nextSegment = nextWord.list("segment")[0]
            if nextSegment is not None:
              ##Tag with following segment
              nextSegLabel = nextSegment.label
              tag = segment.createTag("foll_segment", nextSegLabel)
              log("  Tagged word-final segment " + segment.label + " with " + nextSegLabel)
