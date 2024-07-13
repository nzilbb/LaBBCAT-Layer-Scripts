#
# foll_pause
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 12 Jul 2024
# LaBB-CAT Version: 20240702.1253
# Layer Scope: word
# Layer Type: text
# Layer Alignment: none
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Annotate word with the following pause within-speaker and across-turn.
#   Only applies to words whose end-anchors have confidence at least 50 (i.e.,
#   are either force-aligned or set manually). If the word is not turn-final, 
#   the following word's start-anchor must also have confidence at least 50. 
#   If the word is turn-final, it will be compared against (a) the first
#   word in the following turn if that word's start-anchor has confidence 
#   at least 50, or (b) the start of the following turn otherwise
#
# inputLayer: turn
# inputLayer: word
# outputLayer: foll_pause

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get word end-anchor and end-time
    wordEnd = word.getEnd()
    wordEndTime = wordEnd.getOffset()
    
    ##Get formatted word string for logging
    wordString = word.label + " (" + '%.3f' % word.getStart().getOffset() + "-" + '%.3f' % wordEndTime + ")"
    
    ##Only proceed if confidence is at least 50
    wordEndConf = wordEnd.getConfidence()
    if wordEndConf >= 50:
      
      ##If next word exists in turn
      nextWord = word.next
      if nextWord is not None:
        
        ##Get next word start-anchor
        nextWordStart = nextWord.getStart()
        
        ##Only proceed if confidence is at least 50
        nextWordStartConf = nextWordStart.getConfidence()
        if nextWordStartConf >= 50:
          
          ##Get next word start-time
          nextWordStartTime = nextWord.getStart().getOffset()
          
          ##Tag with difference
          follPause = str(nextWordStartTime - wordEndTime)
          tag = word.createTag("foll_pause", follPause)
          log("Tagged word " + wordString + " with " + follPause)
        
        ##If confidence is too low, log and don't tag
        else:
          nextWordString = nextWord.label + " (" + '%.3f' % nextWordStartTime + "-" + '%.3f' % nextWord.getEnd().getOffset() + ")"
          log("Did not tag turn-internal word " + wordString + "; start confidence for next word - " + nextWordString + " - is " + str(nextWordStartConf))
      
      ##If next word does not exist in turn, get first word in next turn
      else:
        
        ##Determine if next turn exists in transcript
        nextTurn = turn.next
        if nextTurn is not None:
          
          ##Determine if next turn has a first word
          nextWord = nextTurn.first("word")
          if nextWord is not None:
            
            ##Get next word start-anchor
            nextWordStart = nextWord.getStart()
            
            ##If next word start-anchor confidence is at least 50, use it
            nextWordStartConf = nextWordStart.getConfidence()
            if nextWordStartConf >= 50:
              ##Get next word start-time
              nextWordStartTime = nextWord.getStart().getOffset()
              
              ##Tag with difference
              follPause = str(nextWordStartTime - wordEndTime)
              tag = word.createTag("foll_pause", follPause)
              log("Tagged turn-final word " + wordString + " with time to next word: " + follPause)
            
            ##Otherwise, use the start of the following turn
            else:
              ##Get next turn start-time
              nextTurnStartTime = nextTurn.getStart().getOffset()
              
              ##Tag with difference
              follPause = str(nextTurnStartTime - wordEndTime)
              tag = word.createTag("foll_pause", follPause)
              log("Tagged turn-final word " + wordString + " with time to next turn: " + follPause)
          
          ##If next turn does not have a first word, log and don't tag
          else:
            nextTurnString = "(" + '%.3f' % nextTurn.getStart().getOffset() + "-" + '%.3f' % nextTurn.getEnd().getOffset() + ")"
            log("Did not tag turn-final word " + wordString + "; next turn " + nextTurnString + " does not have a first word")
        
        ##If next turn does not exist, log and don't tag
        else:
          log("Did not tag turn-final word " + wordString + "; next turn does not exist in transcript")
    
    ##If confidence is too low, log and don't tag
    else:
      log("Did not tag word " + wordString + "; end confidence is " + str(wordEndConf))
