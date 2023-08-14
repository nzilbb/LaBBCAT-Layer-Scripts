#
# NOT FUNCTIONAL RIGHT NOW
#
# Auxiliary for **unisyn syllables**:
# Label syllables based on pronounce code:
# If a pronounce code has syllable breaks, reconstruct syllable alignments from 
# segments; otherwise, label single syllable with pronounce code.
#

from nzilbb.ag import Annotation

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Get the "unisyn syllables" and "pronounce" tags, if any
    syllables = word.my("unisyn syllables")
    pronounce = word.my("pronounce")
    
    ##Only proceed if there is a "pronounce" tag
    if pronounce is not None:
      
      ##If there are no syllable breaks in the pronounce code, tag unisyn 
      ##syllables with pronounce code
      pronLabel = pronounce.label
      if "-" not in pronLabel:
        ##Create tag if it doesn't exist
        if syllables is None:
          word.createTag("unisyn syllables", pronLabel)
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
        
        ##Only proceed if there are "segment" tags
        segList = word.list("segment")
        if segList is not None:
          
          ##Loop over syllables marked in pronounce code
          segIdx = 0
          for syll in pronLabel.split("-"):
            
            ##Version without stress
            syllNoStress = syll.replace("'", "").replace('"', '')
            
            ##Loop over segments
            currSeg = ''
            startSeg = segIdx
            while currSeg != syllNoStress and segIdx < len(segList):
              currSeg += segList[segIdx].label
              segIdx += 1
            
            ##If matching, create annotation based on segment anchors
            if currSeg == syllNoStress:
              newSyll = word.addAnnotation(Annotation(word.getId(), pronLabel, "unisyn syllables"))
              
              start = segList[startSeg].getStart()
              newSyll.setStart(start)
              end = segList[segIdx - 1].getEnd()
              newSyll.setEnd(end)
              log("Tagged word " + word.label + " with " + syll + " between " + '%.3f' % start.getOffset() + " and " + '%.3f' % end.getOffset() + " seconds")
