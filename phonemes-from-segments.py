# Author: Dan Villarreal, daniel.j.villarreal@gmail.com
# Date: 24 Oct 2022
# LaBB-CAT Version: 20221013.1114
# Layer Scope: word
# Layer Type: phonological
# Layer Alignment: none
# Assumes Existing Layers: turns, transcript, segments
#
# Builds a segmental representation of the word based on aligned segments

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
