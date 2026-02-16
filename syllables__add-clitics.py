#
# syllables auxiliary: add clitics
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal and Robert Fromont
# Date: 16 Feb 2026
# LaBB-CAT Version: 20251105.1346
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: interval
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Add clitic phones to base syllables specified in syllables_no_clitic.
#   Does not override existing annotations (i.e., forms, cliticized or not, 
#     hard-coded into Unisyn or custom dictionary)
#
# inputLayer: turn
# inputLayer: word
# inputLayer: pronounce
# inputLayer: orthography
# inputLayer: orthography_no_clitic
# inputLayer: syllables_no_clitic
# inputLayer: segment
# inputLayer: syllables
# outputLayer: syllables

import re
clitics = ["'s", "s'", "'d", "'ll", "'ve"]

##Pronunciation regexes
voiceless = re.compile(".*[ptkfTsShJ]$")
sibilant = re.compile(".*[szSZJ_]$")
cons = re.compile(".*[pbtdkgNmnlrfvTDszSZhJ_FHP]$")
onsetCons = re.compile("[pbtdkgmnlfvTDszSZhJ_]") ##cons without [NrFHP]

##For each turn in the transcript
for turn in transcript.all("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.all("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Don't override existing syllables annotations (which indicates that
    ##  the segments match what's already in Unisyn or custom dictionary)
    ##  or proceed if there's a pronounce annotation (since this might have
    ##  a different phonemic representation of a clitic)
    syllables = word.all("syllables")
    pronounce = word.first("pronounce")
    if len(syllables) == 0 and pronounce is None:      
      ##Only proceed if there's orthography, orthography_no_clitic, and syllables_no_clitic annotations
      ortho = word.first("orthography")
      orthoBase = word.first("orthography_no_clitic")
      syllablesBase = word.all("syllables_no_clitic")
      
      if ortho is not None and orthoBase is not None and len(syllablesBase) > 0:
        ##Get orthography label
        orthoLabel = ortho.getLabel()
        
        ##Get final syllables_no_clitic in word
        lastSyll = word.last("syllables_no_clitic")
        
        ##Loop over existing syllables_no_clitic tag(s)
        for baseSyll in syllablesBase:
          ##Reset phonClitic
          phonClitic = ""
          
          ##Get stem phones
          currPhones = baseSyll.getLabel()
          
          ##Only add clitics if final syllable in word
          if baseSyll.getOrdinal() == lastSyll.getOrdinal():
            ##Get base label and copy orthography label for tracking progress to orthography_no_clitic
            orthoBaseLabel = orthoBase.getLabel()
            currOrtho = orthoLabel
            
            ##Account for multiple clitics (e.g., "I'd've")
            while orthoBaseLabel != currOrtho:
              if annotator.cancelling: break # cancelled by the user
              
              ##Get clitic at end of currOrtho
              currClitic = [x for x in clitics if currOrtho.endswith(x)][0]
              
              ##Get pronunciation for clitic
              phonClitic = None
              if currClitic == "'s":
                if sibilant.match(currPhones):
                  phonClitic = "0@z"
                elif voiceless.match(currPhones):
                  phonClitic = "s"
                else:
                  phonClitic = "z"
              
              if currClitic == "s'":
                if sibilant.match(currPhones):
                  phonClitic = "0@z"
                elif voiceless.match(currPhones):
                  phonClitic = "s"
                else:
                  phonClitic = "z"
              
              if currClitic == "'d":
                if cons.match(currPhones):
                  phonClitic = "0@d"
                else:
                  phonClitic = "d"
              
              if currClitic == "'ll":
                phonClitic = "0P"
              
              if currClitic == "'ve":
                phonClitic = "0@v"
              
              ##Update currPhones and currOrtho
              currOrtho = re.sub(currClitic + "$", "", currOrtho)
              currPhones += phonClitic
          
          ##Add syllables annotation(s)
          ##Clitic creates new syllable
          if len(phonClitic) > 0 and phonClitic[0] == "0":
            ##Get list of segments for timing
            segList = word.all("segment")
            
            ##Get version without stress
            cliticNoStress = phonClitic[1:]
            
            ##Get final segment annotation of stem
            trackSyll = ""
            segIdx = len(segList) - 1
            while trackSyll != cliticNoStress:
              trackSyll = segList[segIdx].getLabel() + trackSyll
              segIdx -= 1
            stemFinalSeg = segList[segIdx]
            
            ##If stem-final segment is an onset consonant, tag the stem-final syllable minus that segment as one syllable, then that segment plus the clitic as another syllable
            if onsetCons.match(stemFinalSeg.getLabel()):
              end1 = segList[segIdx-1]
              start2 = stemFinalSeg
              label2 = stemFinalSeg.getLabel() + phonClitic
              
            ##If stem-final segment isn't an onset consonant, tag the stem-final syllable as one syllable, then the clitic as another syllable
            else:
              end1 = stemFinalSeg
              start2 = segList[segIdx+1]
              label2 = phonClitic
            
            ##Add annotations
            label1 = re.sub(label2, "", currPhones)
            start1 = baseSyll
            end2 = baseSyll
            newSyll1 = transcript.createSpan(start1, end1, "syllables", label1)
            log("Tagged word " + word.label + " with " + label1 + " between " + '%.3f' % start1.getStart().getOffset() + " and " + '%.3f' % end1.getEnd().getOffset() + " seconds (split syllable)")
            newSyll2 = transcript.createSpan(start2, end2, "syllables", label2)
            log("Tagged word " + word.label + " with " + label2 + " between " + '%.3f' % start2.getStart().getOffset() + " and " + '%.3f' % end2.getEnd().getOffset() + " seconds (split syllable)")
            
          ##Clitic doesn't create new syllable
          else:
            newSyll = transcript.createSpan(baseSyll, baseSyll, "syllables", currPhones)
            log("Tagged word " + word.label + " with " + currPhones + " between " + '%.3f' % baseSyll.getStart().getOffset() + " and " + '%.3f' % baseSyll.getEnd().getOffset() + " seconds")
