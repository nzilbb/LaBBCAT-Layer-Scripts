#
# foll_pause
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 16 Jul 2024
# LaBB-CAT Version: 20240702.1253
# Layer Scope: word
# Layer Type: number
# Layer Alignment: none
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Annotate word with the following pause within-speaker and across-utterance.
#   Only applies to words whose end-anchors have confidence at least 50 (i.e.,
#   are either force-aligned or set manually). Word end is compared to:
#     (a) the start of the following word (if that start-anchor has confidence
#         at least 50); or
#     (b) the start of the following utterance (if the word is utterance-
#         final), in order to cover pre-overlap words; or 
#     (c) the start of the following turn (if word or next word are missing
#         utterance tags), as a fallback to utterance---utterance is preferred 
#         because it more accurately reflects transcribed line breaks; or
#     (c) untagged (otherwise)
#
# inputLayer: participant
# inputLayer: utterance
# inputLayer: turn
# inputLayer: word
# outputLayer: foll_pause

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
  numWords = len(wordList)
  
  ##For each word (except for the last word)
  for idx, word in enumerate(wordList[0:(numWords-1)]):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get word end-anchor and end-time
    wordEnd = word.getEnd()
    wordEndTime = wordEnd.getOffset()
    
    ##Only proceed if confidence is at least 50
    wordEndConf = wordEnd.getConfidence()
    if wordEndConf >= 50:
      
      ##If next word exists
      nextWord = wordList[idx+1]
      if nextWord is not None:
        
        ##Get next word start-anchor and start-time
        nextWordStart = nextWord.getStart()
        nextWordStartTime = nextWordStart.getOffset()
        
        ##If next word start-anchor confidence is at least 50
        nextWordStartConf = nextWordStart.getConfidence()
        if nextWordStartConf >= 50:
          
          ##Tag with difference
          follPause = str(nextWordStartTime - wordEndTime)
          tag = word.createTag("foll_pause", follPause)
          log("Tagged word " + node_string(word) + " with " + follPause)
        
        ##If next word start-anchor confidence is too low
        else:
          
          ##Check next word's utterance
          utterance = word.first("utterance")
          nextUtterance = nextWord.first("utterance")
          
          ##If word's utterance and next word's utterance both exist
          if utterance is not None and nextUtterance is not None:
            
            ##If word is utterance-final
            if utterance.getId() != nextUtterance.getId():
              
              ##Get next utterance start-time
              nextUttStartTime = nextUtterance.getStart().getOffset()
              
              ##Tag with difference
              follPause = str(nextUttStartTime - wordEndTime)
              tag = word.createTag("foll_pause", follPause)
              log("Tagged utterance-final word " + node_string(word) + " with time to next utterance: " + follPause)
          
            ##If word is not utterance-final, log and don't tag
            else:
              log("Did not tag utterance-internal word " + node_string(word) + "; start confidence for next word - " + node_string(nextWord) + " - is " + str(nextWordStartConf))
          
          ##If either word's utterance or next word's utterance is missing, use turn instead
          else:
            
            ##Check next word's turn
            turn = word.getParent()
            nextTurn = nextWord.getParent()
            
            ##If word is turn-final
            if turn.getId() != nextTurn.getId():
              
              ##Get next turn start-time
              nextTurnStartTime = nextTurn.getStart().getOffset()
              
              ##Tag with difference
              follPause = str(nextTurnStartTime - wordEndTime)
              tag = word.createTag("foll_pause", follPause)
              log("Tagged turn-final word " + node_string(word) + " with time to next turn: " + follPause)
            
            ##If word is not turn-final, log and don't tag
            else:
              log("Did not tag turn-internal word " + node_string(word) + "; start confidence for next word - " + node_string(nextWord) + " - is " + str(nextWordStartConf))
      
      ##If next word does not exist (unexpectedly), log and don't tag
      else:
        
        ##Get word ordinal and end-anchor ID
        wordOrdinal = word.getOrdinal()
        wordEndId = wordEnd.getId()
        
        ##Log
        log("Did not tag utterance-final word " + node_string(word) + " with id " + wordEndId + " (corpus ordinal: " + str(wordOrdinal) + "; sort order: " + str(idx) + "); next word does not exist in participant")
    
    ##If confidence is too low, log and don't tag
    else:
      log("Did not tag word " + node_string(word) + "; end confidence is " + str(wordEndConf))
