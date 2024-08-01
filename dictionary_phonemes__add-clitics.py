#
# dictionary_phonemes auxiliary: add clitics
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal and Robert Fromont
# Date: 1 Aug 2024
# LaBB-CAT Version: 20240702.1253
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: none
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Add clitic phonemes to base phonemes specified in phonemes_no_clitic.
#   Does not override existing annotations (i.e., forms, cliticized or not, 
#     hard-coded into Unisyn or custom dictionary)
#
# inputLayer: turn
# inputLayer: word
# inputLayer: orthography
# inputLayer: orthography_no_clitic
# inputLayer: phonemes_no_clitic
# inputLayer: dictionary_phonemes
# outputLayer: dictionary_phonemes

import re
clitics = ["'s", "s'", "'d", "'ll", "'ve"]

##Pronunciation regexes
voiceless = re.compile(".*[ptkfTsShJ]$")
sibilant = re.compile(".*[szSZJ_]$")
cons = re.compile(".*[pbtdkgNmnlrfvTDszSZhJ_FHP]$")

##For each turn in the transcript
for turn in transcript.all("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.all("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Don't override existing entries (forms, cliticized or not, hard-coded 
    ##  into Unisyn or custom dictionary)
    phonemes = word.first("dictionary_phonemes")
    if phonemes is None:
      
      ##Only proceed if there's an orthography and orthography_no_clitic tag
      ortho = word.first("orthography")
      orthoBase = word.first("orthography_no_clitic")
      if ortho is not None and orthoBase is not None:
        
        ##Get orthography label
        orthoLabel = ortho.getLabel()
        
        ##Loop over existing phonemes_no_clitic tag(s)
        ##N.B. The set of words with no preexisting dictionary_phonemes tag
        ##  *and* no phonemes_no_clitic tag includes those with:
        ##  - a pronounce code
        ##  - no dictionary entry (Unisyn or custom) matching base form (incl.
        ##    redactions)
        for phonemesBase in word.all("phonemes_no_clitic"):
          ##Get base label and stem phonemes
          orthoBaseLabel = orthoBase.getLabel()
          currPhonemes = phonemesBase.getLabel()
          
          ##Copy orthography label for tracking progress to orthography_no_clitic
          currOrtho = orthoLabel
          
          ##Account for multiple clitics (e.g., "I'd've")
          while orthoBaseLabel != currOrtho:
            if annotator.cancelling: break # cancelled by the user
            
            ##Get clitic at end of currOrtho
            currClitic = [x for x in clitics if currOrtho.endswith(x)][0]
            
            ##Get pronunciation for clitic
            phonClitic = None
            if currClitic == "'s":
              if sibilant.match(currPhonemes):
                phonClitic = "@z"
              elif voiceless.match(currPhonemes):
                phonClitic = "s"
              else:
                phonClitic = "z"
            
            if currClitic == "s'":
              if sibilant.match(currPhonemes):
                phonClitic = ["@z", ""]
              elif voiceless.match(currPhonemes):
                phonClitic = "s"
              else:
                phonClitic = "z"
            
            if currClitic == "'d":
              if cons.match(currPhonemes):
                phonClitic = "@d"
              else:
                phonClitic = "d"
            
            if currClitic == "'ll":
              phonClitic = "P"
            
            if currClitic == "'ve":
              phonClitic = "@v"
            
            ##Update currPhonemes and currOrtho
            currOrtho = re.sub(currClitic + "$", "", currOrtho)
            if type(phonClitic) is list:
              currPhonemes = [currPhonemes + x for x in phonClitic]
            else:
              currPhonemes += phonClitic
          
          ##Modify tag
          tag = word.createTag("dictionary_phonemes", currPhonemes)
          log("Tagged word " + orthoLabel + " with " + currPhonemes)
