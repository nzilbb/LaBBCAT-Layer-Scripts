#
# syllables auxiliary: resyllabify intervocalic consonants
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal
# Date: 21 Apr 2026
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
#   Resyllabifies intervocalic consonsants in order to make Unisyn-like
#     syllable boundaries (which coincide with morpheme boundaries) more
#     like CELEX syllable boundaries.
#   For adjacent syllables in the same word, if the first syllable ends in a
#     vowel+consonant (other than r or ng) and the second begins with a vowel,
#     shifts the end/start and relabels annotations to place the consonant in
#     the second syllable.
#   If the first syllable ends with a vowel and the second begins with an r,
#     places the r in the first syllable.
#
# inputLayer: turn
# inputLayer: word
# inputLayer: segment
# inputLayer: syllables
# outputLayer: syllables

import re

##Pronunciation regexes
ons_v  = "[iIE\{Q\$VUu@78#3912645]"
coda_v = "[iIE\{Q\$VUu@78#3912645FHP]"

final_CV = re.compile(".*" + coda_v + "[pbtdkgmnlfvTDszSZhJ_]$") ##Coda cons: excludes [NFHPr]
initial_V = re.compile("^['\"0]" + ons_v + ".*")
final_V = re.compile(".*" + coda_v + "$")
initial_rV = re.compile("^['\"0]r" + ons_v + ".*")

##For each turn in the transcript
for turn in transcript.all("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.all("word"):
    if annotator.cancelling: break # cancelled by the user
    
    syllables = word.all("syllables")
    syll_pairs = [x for x in zip(syllables[:-1], syllables[1:])]
    for (prev, foll) in syll_pairs:
      prevLabel = prev.getLabel()
      follLabel = foll.getLabel()
      
      ##If intervocalic consonant is syllabified as coda rather than onset
      if final_CV.match(prevLabel) and initial_V.match(follLabel):
        ##Construct new labels
        newPrevLabel = prevLabel[:-1]
        newFollLabel = follLabel[0] + prevLabel[-1] + follLabel[1:]
        
        ##Get old and new boundaries
        oldBound = prev.getEnd()
        newBound = prev.last("segment").getStart()
                
        ##Modify annotations
        prev.setLabel(newPrevLabel)
        foll.setLabel(newFollLabel)
        prev.setEnd(newBound)
        foll.setStart(newBound)
        log("In word " + word.getLabel() + ", changed " + prevLabel + "-" + follLabel + " to " + newPrevLabel + "-" + newFollLabel + " (boundary shift backward from " + '%.3f' % oldBound.getOffset() + " to " + '%.3f' % newBound.getOffset() + " seconds)")
      
      ##If intervocalic r is syllabified as onset rather than coda
      if final_V.match(prevLabel) and initial_rV.match(follLabel):
        log(prevLabel + " " + follLabel)
        ##Construct new labels
        newPrevLabel = prevLabel + follLabel[1]
        newFollLabel = follLabel[0] + follLabel[2:]
        
        ##Get old and new boundaries
        oldBound = prev.getEnd()
        newBound = foll.all("segment")[0].getEnd() ##For some reason, foll.first("segment") is NoneType
                
        ##Modify annotations
        prev.setLabel(newPrevLabel)
        foll.setLabel(newFollLabel)
        prev.setEnd(newBound)
        foll.setStart(newBound)
        log("In word " + word.getLabel() + ", changed " + prevLabel + "-" + follLabel + " to " + newPrevLabel + "-" + newFollLabel + " (boundary shift forward from " + '%.3f' % oldBound.getOffset() + " to " + '%.3f' % newBound.getOffset() + " seconds)")
