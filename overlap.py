#
# overlap
# (Python-managed LaBB-CAT layer)
#
# Author: Dan Villarreal
# Date: 25 Mar 2024
# LaBB-CAT Version: 20240306.1320
# Layer Scope: phrase
# Layer Type: text
# Layer Alignment: intervals
#
# APLS-specific attributes:
#   Generate: always
#   Project: alignment
#
# Description: 
#   Annotate utterance with TRUE if multiple utterances overlap, FALSE
#     otherwise. Only looks at segmentation, not actual speech.
#
# inputLayer: utterance
# outputLayer: overlap
# for each utterance in the transcript
for utterance in transcript.all("utterance"):
  if annotator.cancelling: break # cancelled by the user
  start = utterance.getStart().getOffset()
  end = utterance.getEnd().getOffset()
  # check if multiple utterance annotations
  if len(utterance.midpointIncludingAnnotationsOn("utterance")) > 0:
    utterance.createTag("overlap", "TRUE")
    log("Tagged utterance from " + str(start) + " to " + str(end) + " with TRUE")
  else:
    utterance.createTag("overlap", "FALSE")
    log("Tagged utterance from " + str(start) + " to " + str(end) + " with FALSE")
