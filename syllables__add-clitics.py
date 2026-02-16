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
# inputLayer: orthography
# inputLayer: orthography_no_clitic
# inputLayer: syllables_no_clitic
# inputLayer: syllables
# outputLayer: syllables

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
    
    ##Don't override existing syllables annotations (which indicates that
    ##  the segments match what's already in Unisyn or custom dictionary)
    syllables = word.all("syllables")
    if len(syllables) == 0:      
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
                  phonClitic = "@z"
                elif voiceless.match(currPhones):
                  phonClitic = "s"
                else:
                  phonClitic = "z"
              
              if currClitic == "s'":
                if sibilant.match(currPhones):
                  phonClitic = ["@z", ""]
                elif voiceless.match(currPhones):
                  phonClitic = "s"
                else:
                  phonClitic = "z"
              
              if currClitic == "'d":
                if cons.match(currPhones):
                  phonClitic = "@d"
                else:
                  phonClitic = "d"
              
              if currClitic == "'ll":
                phonClitic = "P"
              
              if currClitic == "'ve":
                phonClitic = "@v"
              
              ##Update currPhones and currOrtho
              currOrtho = re.sub(currClitic + "$", "", currOrtho)
              if type(phonClitic) is list:
                currPhones = [currPhones + x for x in phonClitic]
              else:
                currPhones += phonClitic
          
          ##Add syllables annotation
          newSyll = transcript.createSpan(baseSyll, baseSyll, "syllables", currPhones)
          log("Tagged word " + word.label + " with " + currPhones + " between " + '%.3f' % baseSyll.getStart().getOffset() + " and " + '%.3f' % baseSyll.getEnd().getOffset() + " seconds")
