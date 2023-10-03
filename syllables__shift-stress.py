#
# unisyn syllables auxiliary: shift stress markers
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal
# Date: 3 Oct 2023
# LaBB-CAT Version: 20231002.1520
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: intervals
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Shift stress marker (if any) from before vowel to start of syllable
#   Overwrites existing annotations
#
# inputLayer: turn
# inputLayer: word
# inputLayer: unisyn syllables
# outputLayer: unisyn syllables

import re
# regular expression for identifying non-initial stress markers
stressPattern = re.compile("(.+)(['\",])(.*)")

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get the "unisyn syllables" tags, if any
    syllList = word.list("unisyn syllables")
    
    ##Only proceed if there are "unisyn syllables" tags
    if syllList is not None:
      
      ##For each syllable in the word
      for syllable in syllList:
        if annotator.cancelling: break # cancelled by the user
        
        ##If the syllable has a non-initial stress marker
        currLabel = syllable.label
        if stressPattern.match(currLabel): 
          
          ##Move the stress marker to the start of the syllable
          newLabel = re.sub(stressPattern, "\\2\\1\\3", currLabel)
          # syllable.setLabel(newLabel)
          syllable.label = newLabel
          log("Changed syllable label " + currLabel + " to " + newLabel)

