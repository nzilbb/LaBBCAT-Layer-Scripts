#
# foll_segment
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 12 Jul 2024
# LaBB-CAT Version: 20240702.1253
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
#   across turn boundaries). If followed by a pause, annotate with `.`
#
# inputLayer: turn
# inputLayer: word
# inputLayer: foll_pause
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
        ##If following pause is 0
        follPause = word.first("foll_pause")
        if follPause is not None:
          if follPause.label == "0.0" or follPause.label = "0":
            ##Determine if next word exists in turn
            nextWord = word.next
            if nextWord is not None:
              ##Determine if next word has a first segment
              nextSegments = nextWord.list("segment")
              if len(nextSegments) > 0:
                ##Tag with following segment
                nextSegLabel = nextSegments[0].label
                tag = segment.createTag("foll_segment", nextSegLabel)
                log("  Tagged word-final segment " + segment.label + " with " + nextSegLabel)
              ##If no first segment, log but don't tag
              else:
                log("  Did not tag word-final segment; next word (" + nextWord.label + " at " + '%.3f' % nextWord.getStart().getOffset() + "-" + '%.3f' % nextWord.getEnd().getOffset() + ") has no segments")
            ##If next word does not exist in turn, get first word in next turn
            else:
              ##Determine if next turn exists in transcript
              nextTurn = turn.next
              if nextTurn is not None:
                ##Determine if next turn has a first word
                nextWord = nextTurn.first("word")
                if nextWord is not None:
                  ##Determine if next word has a first segment
                  nextSegments = nextWord.list("segment")
                  if len(nextSegments) > 0:
                    ##Tag with following segment
                    nextSegLabel = nextSegments[0].label
                    tag = segment.createTag("foll_segment", nextSegLabel)
                    log("  Tagged word-final segment " + segment.label + " with " + nextSegLabel)
                  ##If no first segment, log but don't tag
                  else:
                    log("  Did not tag word-final segment; next word (" + nextWord.label + " at " + '%.3f' % nextWord.getStart().getOffset() + "-" + '%.3f' % nextWord.getEnd().getOffset() + ") has no segments")
              ##If next turn does not exist in transcript, log it
              else:
                log("  Next turn does not exist in transcript")
          ##If following pause is nonzero
          else:
            ##Tag with pause
            nextSegLabel = "."
            tag = segment.createTag("foll_segment", nextSegLabel)
            log("  Tagged word-final segment " + segment.label + " with " + nextSegLabel)
