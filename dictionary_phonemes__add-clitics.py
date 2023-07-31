#
# dictionary_phonemes auxiliary: add clitics
# (Python-managed LaBB-CAT layer auxiliary)
#
# Author: Dan Villarreal
# Date: 31 Jul 2023
# LaBB-CAT Version: 20230731.1146
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: none
# Assumes Existing Layers: turn, word, orthography, orthography_no_clitic, phonemes_no_clitic, dictionary-phonemes
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Add clitic phonemes to base phonemes specified in phonemes_no_clitic.
#   Does not override existing annotations (i.e., forms specified in Unisyn or custom dictionary)
#

import re
clitics = ["'s", "s'", "'d", "'ll", "'ve"]

##Pronunciation regexes
voiceless = re.compile(".*[ptkfTsShJ]$")
sibilant = re.compile(".*[szSZJ_]$")
cons = re.compile(".*[pbtdkgNmnlrfvTDszSZhJ_FHP]$")

##For each turn in the transcript
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  ##For each word in the turn 
  for word in turn.list("word"):
    if annotator.cancelling: break # cancelled by the user
    
    ##Don't override existing entries
    phonemes = word.my("dictionary-phonemes")
    if phonemes is None:
      
      ##Only proceed if there's an orthography_no_clitic tag *and* 
      orthoBase = word.my("orthography_no_clitic")
      
      if orthoBase is not None:
        
        ##Get orthography label
        orthoLabel = word.my("orthography").label
        
        ##Only proceed if there's a phonemes_no_clitic tag (which might be missing if there's a pronounce code and/or a custom dictionary entry matching the version with a clitic)
        phonemesBase = word.my("phonemes_no_clitic")
        
        if phonemesBase is not None:
          ##Get base label and stem phonemes
          orthoBaseLabel = orthoBase.label
          currPhonemes = phonemesBase.label
          
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
          tag = word.createTag("dictionary-phonemes", currPhonemes)
          log("Tagged word " + orthoLabel + " with " + currPhonemes)
          
        else:
          log("Did not tag word " + orthoLabel + " (no phonemes_no_clitic tag)")
