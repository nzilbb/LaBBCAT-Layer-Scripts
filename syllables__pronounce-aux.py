#
# syllables auxiliary: label syllables based on pronounce code
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
#   If a pronounce code has syllable breaks, reconstruct syllable alignments 
#     from segments; otherwise, label single syllable with pronounce code (as
#     long as the word has segment annotations)
#   Creates new annotations and overwrites existing annotations (i.e.,
#     "idiosyncratic pronunciation" pronounce codes)
#
# inputLayer: turn
# inputLayer: word
# inputLayer: syllables
# inputLayer: pronounce
# inputLayer: segment
# outputLayer: syllables

from nzilbb.ag import Annotation
import re

# regular expression for identifying the absence of a stress marker
noStressPattern = re.compile("^[^'\"0]+$")

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get the "syllables", "pronounce", & "segment" tags, if any
    syllables = word.my("syllables")
    pronounce = word.my("pronounce")
    segList = word.list("segment")
    
    ##Only proceed if there is a "pronounce" tag and "segment" tags
    if pronounce is not None and segList is not None:
      
      ##Get "pronounce" annotation
      pronLabel = pronounce.label 
      
      ##If there are no syllable breaks in the pronounce code, tag syllables
      ##  with complete pronounce code
      ##("segment" tags aren't needed for this case, but requiring them prevents
      ##  isolated syllables from being tagged in otherwise untagged turns)
      if "-" not in pronLabel:
        
        ##Add unstressed marker if needed
        if noStressPattern.match(pronLabel):
          pronLabel = "0" + pronLabel
        
        ##Create tag if it doesn't exist
        if syllables is None:
          word.createTag("syllables", pronLabel)
          log("Tagged word " + word.label + " with " + pronLabel)
        ##Relabel tag if it does
        else:
          currLabel = syllables.label
          if currLabel != pronLabel:
            syllables.label = pronLabel
            log("In word " + word.label + ", changed syllable label " + currLabel + " to " + pronLabel)
          else:
            log("In word " + word.label + ", no need to change syllable label " + currLabel)
      
      ##If there are syllable breaks, reconstruct syllables from segments
      else:
          
        ##Loop over syllables marked in pronounce code
        segIdx = 0
        for syll in pronLabel.split("-"):
          ##Version without stress
          syllNoStress = syll.replace("'", "").replace('"', '').replace('0', '')
          
          ##Add unstressed marker if needed
          if syll == syllNoStress:
            syll = "0" + syll
          
          ##Loop over segments
          currSeg = ''
          startSeg = segIdx
          while currSeg != syllNoStress and segIdx < len(segList):
            currSeg += segList[segIdx].label
            segIdx += 1
          
          ##If matching, create annotation based on segment anchors
          if currSeg == syllNoStress:
            start = segList[startSeg]
            end = segList[segIdx - 1]
            newSyll = transcript.createSpan(start, end, "syllables", syll)
            
            log("Tagged word " + word.label + " with " + syll + " between " + '%.3f' % start.getStart().getOffset() + " and " + '%.3f' % end.getEnd().getOffset() + " seconds")
