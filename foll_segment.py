#
# foll_segment
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 25 Oct 2024
# LaBB-CAT Version: 20240920.1237
# Layer Scope: segment
# Layer Type: phonological
# Layer Alignment: intervals
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Annotate segment with the segment that follows it within-participant and
#   across-utterance. If followed by a pause (a nonzero foll_pause 
#   annotation), annotate as `.`
#
# inputLayer: participant
# inputLayer: word
# inputLayer: segment
# inputLayer: foll_pause
# outputLayer: foll_segment

def node_string(node, label = True):
  startEnd = '%.3f' % node.getStart().getOffset() + "-" + '%.3f' % node.getEnd().getOffset()
  if label:
    return node.getLabel() + " (" + startEnd + ")"
  else:
    return startEnd

##For each participant in the transcript
for participant in transcript.all("participant"):
  if annotator.cancelling: break # cancelled by the user
  
  ##Get each word in the participant, sorted by start offset
  wordList = participant.all("word")
  wordList = sorted(wordList, key=lambda d: d.getStart().getOffset())
  
  ##For each word
  for idx, word in enumerate(wordList):
    if annotator.cancelling: break # cancelled by the user
    
    log("In word " + node_string(word) + ":")
    
    ##For each segment in the word
    for segment in word.all("segment"):
      if annotator.cancelling: break # cancelled by the user
      
      ##If non-word-final...
      if word.getEnd() != segment.getEnd():
        
        ##Tag with following segment, if it exists
        nextSeg = segment.getNext()
        if nextSeg is not None:
          nextSegLabel = nextSeg.getLabel()
          tag = segment.createTag("foll_segment", nextSegLabel)
          log("  Tagged word-internal segment " + segment.getLabel() + " with " + nextSegLabel)
      
      ##If word-final...
      else:
        
        ##If following pause is 0
        follPause = word.first("foll_pause")
        if follPause is not None:
          
          if follPause.getLabel() == "0.0" or follPause.getLabel() == "0":
            
            ##If next word exists
            nextWord = wordList[idx+1]
            if nextWord is not None:
              
              ##If next word has a first segment, tag with following segment
              nextSegments = nextWord.all("segment")
              if len(nextSegments) > 0:
                nextSegLabel = nextSegments[0].getLabel()
                tag = segment.createTag("foll_segment", nextSegLabel)
                log("  Tagged word-final segment " + segment.getLabel() + " with " + nextSegLabel)
                
              ##If no first segment, log and don't tag
              else:
                log("  Did not tag word-final segment " + segment.getLabel() + "; next word - " + node_string(nextWord) + " - has no segments")
            
            ##If next word does not exist (unexpectedly), log and don't tag
            else:
              
              ##Get word ordinal and end-anchor ID
              wordOrdinal = word.getOrdinal()
              wordEndId = wordEnd.getId()
              
              ##Log
              log("  Did not tag word-final segment " + segment.getLabel() + " in word with id " + wordEndId + " (corpus ordinal: " + str(wordOrdinal) + "; sort order: " + str(idx) + "); next word does not exist in participant")
              
          ##If following pause is nonzero, tag with pause
          else:
            nextSegLabel = "."
            tag = segment.createTag("foll_segment", nextSegLabel)
            log("  Tagged word-final segment " + segment.getLabel() + " with " + nextSegLabel)
        
        ##If following pause does not exist, log and don't tag
        else:
          log("  Did not tag word-final segment " + segment.getLabel() + "; following pause does not exist")
