#
# syllables auxiliary: resyllabify intervocalic consonants
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal
# Date: 4 Mar 2026
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
#   For adjacent syllables in the same word, if the first syllable ends in a
#     vowel+consonant and the second begins with a vowel, shifts the end/start
#     and relabels annotations to place the consonant in the second syllable.
#   This makes Unisyn-like syllable boundaries (which coincide with morpheme
#     boundaries) more like CELEX syllable boundaries.
#
# inputLayer: turn
# inputLayer: word
# inputLayer: segment
# inputLayer: syllables
# outputLayer: syllables

import re

##Pronunciation regexes
coda = re.compile(".*[iIE\{Q\$VUu@78#3912645][pbtdkgmnlrfvTDszSZhJ_]$") ##Cons: excludes [NFHP]
onset = re.compile("^['\"0][iIE\{Q\$VUu@78#3912645FHP].*") ##Vowels: includes [FHP]

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
      if coda.match(prevLabel) and onset.match(follLabel):
        
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
        log("In word " + word.getLabel() + ", changed " + prevLabel + "-" + follLabel + " to " + newPrevLabel + "-" + newFollLabel + " (boundary shift from " + '%.3f' % oldBound.getOffset() + " to " + '%.3f' % newBound.getOffset() + " seconds)")
