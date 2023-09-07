#
# phonemes
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 6 Sep 2023
# LaBB-CAT Version: 20230901.1521
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
for turn in transcript.list("turn"):
  if annotator.cancelling: break # cancelled by the user
  
  # for each word in the turn
  for word in turn.list("word"):    
    if annotator.cancelling: break # cancelled by the user  
    
    # clear wordPhonemes
    wordPhonemes = ""
    
    # for each phone in the word, add to wordPhonemes
    for segment in word.list("segment"):
      if segment is not None:
        wordPhonemes += segment.label
    
    # if wordPhonemes is not empty...
    if wordPhonemes:
      # ...create tag
      tag = word.createTag("phonemes", wordPhonemes)
      log("Tagged word " + word.label + " with " + wordPhonemes)
