# Author: Dan Villarreal, daniel.j.villarreal@gmail.com
# Date: 27 Mar 2019
# LaBB-CAT Version: 20190109.1225 
# Layer Scope: segment
# Layer Type: Text
# Layer Alignment: none
# Assumes Existing Layers: R classifier prob
# 
# Maps classifier probabilities to Absent or Present based on threshhold of 0.579065

threshhold = 0.566435

# for each turn in the transcript
for turn in transcript.list("turns"):
  if annotator.cancelling: break # cancelled by the user
  
  # for each word in the turn 
  for word in turn.list("transcript"):
    if annotator.cancelling: break # cancelled by the user   
    
    # for each phone in the word
    for segment in word.list("segments"):
      # get the "R classifier prob" tag, if any
      prob = segment.my("R classifier prob")
      
      # if there's a classifier probability...
      if prob is not None:
        
        # ...if it's convertible to a float...
        if isinstance(float(prob.label), float):
          
          # ...and if it's at least the threshhold
          if float(prob.label) >= threshhold:
            # tag as Present
            tag = segment.createTag(thisLayer.id, "Present")
            log("Tagged segment " + segment.label + " (classifier probability " + prob.label + ") with " + tag.label)
          
          # if the probability is less than the threshhold
          else:
            # tag as Absent
            tag = segment.createTag(thisLayer.id, "Absent")
            log("Tagged segment " + segment.label + " (classifier probability " + prob.label + ") with " + tag.label)
