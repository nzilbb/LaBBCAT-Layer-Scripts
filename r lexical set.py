import re
# regular expression for identifying phones tagged as glide
glidePattern = re.compile("(rh|li)-glide")

# for each turn in the transcript
for turn in transcript.list("turns"):
  if annotator.cancelling: break # cancelled by the user
  
  # for each word in the turn 
  for word in turn.list("transcript"):
    if annotator.cancelling: break # cancelled by the user   
    
    # for each phone in the word
    for segment in word.list("segments"):
      
      # get the "rhotic or linking" tag, if any
      rhli = segment.my("rhotic or linking")
      
      # if there's a tag on the "rhotic or linking" layer
      if rhli is not None:
      
        # and the tag isn't a glide
        if glidePattern.match(rhli.label) is None: 
          
          if segment.label == "#":
            tag = segment.createTag(thisLayer.id, "START")
          
          if segment.label == "$":
            tag = segment.createTag(thisLayer.id, "NORTH")
          
          if segment.label == "@":
            tag = segment.createTag(thisLayer.id, "lettER")
          
          if segment.label == "1":
            tag = segment.createTag(thisLayer.id, "SQUARE")
          
          if segment.label == "2":
            tag = segment.createTag(thisLayer.id, "PRICE-R")
          
          if segment.label == "3":
            tag = segment.createTag(thisLayer.id, "NURSE")
          
          if segment.label == "6":
            tag = segment.createTag(thisLayer.id, "MOUTH")
          
          if segment.label == "7":
            tag = segment.createTag(thisLayer.id, "NEAR")
          
          if segment.label == "8":
            tag = segment.createTag(thisLayer.id, "SQUARE")
          
          if segment.label == "9":
            tag = segment.createTag(thisLayer.id, "CURE")
