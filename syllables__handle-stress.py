#
# syllables auxiliary: handle stress markers
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal
# Date: 26 Aug 2024
# LaBB-CAT Version: 20240814.1638
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: intervals
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Makes stress markers more consistent by:
#   - Shifting stress marker (if any) from before vowel to start of syllable
#   - Adding `0` to start of syllable if there's no stress marker
#   - Throwing an error if `,` (illegal tertiary-stress marker) is present in syllable
#   Overwrites existing annotations
#
# inputLayer: turn
# inputLayer: word
# inputLayer: syllables
# outputLayer: syllables

import re
# regular expression for identifying non-initial stress markers
stressPattern = re.compile("(.+)(['\"0])(.*)")
# regular expression for identifying the absence of a stress marker
noStressPattern = re.compile("^[^'\"0]+$")
# illegal stress marker
badStress = ","

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get the "syllables" tags, if any
    syllList = word.list("syllables")
    
    ##Only proceed if there are "syllables" tags
    if syllList is not None:
      
      ##For each syllable in the word
      for syllable in syllList:
        if annotator.cancelling: break # cancelled by the user
        
        ##Throw an error if there's an illegal stress marker
        currLabel = syllable.label
        if badStress in currLabel:
          raise ValueError("Illegal stress marker " + badStress + " in word ", word.getLabel())
        
        ##If the syllable has a non-initial stress marker
        if stressPattern.match(currLabel): 
          
          ##Move the stress marker to the start of the syllable
          newLabel = re.sub(stressPattern, "\\2\\1\\3", currLabel)
          # syllable.setLabel(newLabel)
          syllable.label = newLabel
          log("Changed syllable label " + currLabel + " to " + newLabel)
        
        ##If the syllable doesn't have any stress marker
        elif noStressPattern.match(currLabel):
          
          ##Add a 0 stress marker
          newLabel = "0" + currLabel
          syllable.label = newLabel
          log("Changed syllable label " + currLabel + " to " + newLabel)

