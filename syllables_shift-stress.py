#
# ADD HEADER
#

import re
# regular expression for identifying non-initial stress markers
stressPattern = re.compile("(.+)(['\"])(.*)")

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
          ##NOTE: label-setting doesn't currently work (but newLabel is constructed correctly)
          # syllable.setLabel(newLabel)
          syllable.label = newLabel
          log("Changed syllable label " + currLabel + " to " + newLabel)
