#
# phonemes
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 12 Feb 2026 
# LaBB-CAT Version: 20251105.1346 
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: none
#
# APLS-specific attributes:
#   Generate: always
#   Project: phonology
#
# Description: 
#   Builds a segmental representation of the word based on aligned segments
#
# inputLayer: turn
# inputLayer: word
# inputLayer: segment
# outputLayer: phonemes

# for each turn in the transcript
for turn in transcript.all("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  # for each word in the turn
  for word in turn.all("word"):
    if annotator.cancelling: break # cancelled by the user  
    
    # clear wordPhonemes
    wordPhonemes = ""
    
    # for each phone in the word, add to wordPhonemes
    for segment in word.all("segment"):
      if segment is not None:
        wordPhonemes += segment.label
    
    # if wordPhonemes is not empty...
    if wordPhonemes:
      # ...create tag
      tag = word.createTag("phonemes", wordPhonemes)
      log("Tagged word " + word.label + " with " + wordPhonemes)
