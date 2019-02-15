import re
# regular expression for identifying phones that might be rhotic
rhoticPattern = re.compile(".+r")
# regular expression for identifying vowels
vowelPattern = re.compile("[cCEFHiIPqQuUV0123456789~#\{\$@]")
# regular expression for identifying mis-tagged phones
badPattern = re.compile("[dD]r")

# for each turn in the transcript
for turn in transcript.list("turns"):
  if annotator.cancelling: break # cancelled by the user
  
  # for each word in the turn
  for word in turn.list("transcript"):    
    if annotator.cancelling: break # cancelled by the user  
    
    # don't tag the word "er"
    log("Word label: " + word.label)
    ortho = word.my("orthography")
    if ortho is not None:
      if ortho.label != "er":
      
        # there's no immediately preceding segment yet
        lastSegment = None 
        
        # for each phone in the word
        for segment in word.list("segments"):
          
          # get the "gam segments", "foll segment", and "foll pause" tags, if any 
          gam = segment.my("gam segments")
          follSeg = segment.my("foll segment")
          follPause = word.my("foll pause")
          
          # if there's a gam version of the segment...
          if gam is not None: 
            
            # ... and it matches our regular expression
            if rhoticPattern.match(gam.label) is not None: 
              
              # if there is a following segment
              if follSeg is not None:
              
                # if the following segment is a vowel (which should only match rhoticPattern word-finally)
                if vowelPattern.match(follSeg.label) is not None:

                  # if there's a following pause
                  if follPause > 0:

                    # tag as rhotic
                    tag = segment.createTag(thisLayer.id, "rhotic")
                    log("Tagged segment " + segment.label + " (" + gam.label + ") " + " with " + tag.label)

                  # if there's no following pause
                  else:

                    # tag as linking
                    tag = segment.createTag(thisLayer.id, "linking")
                    log("Tagged segment " + segment.label + " (" + gam.label + ") " + " with " + tag.label)

                # if the following segment is not a vowel
                else:

                  # tag as rhotic
                  tag = segment.createTag(thisLayer.id, "rhotic")
                  log("Tagged segment " + segment.label + " (" + gam.label + ") " + " with " + tag.label)
              
              # there's no following segment or following segment is unknown
              else:
                
                # tag as rhotic
                tag = segment.createTag(thisLayer.id, "rhotic")
                log("Tagged segment " + segment.label + " (" + gam.label + ") " + " with " + tag.label)
              
          else: # there's no "gam segments" tag
            
            # if this is schwa, and the last segment has a nonempty tag
            if segment.label == "@" and lastSegment is not None and lastSegment.my(thisLayer.id) is not None:
              
              lastLabel = lastSegment.my(thisLayer.id).label
              # if the last segment is tagged as rhotic
              if lastLabel == "rhotic":
                
                # tag the schwa
                tag = segment.createTag(thisLayer.id, "rh-glide")
                # and change the label of the preceding tag
                lastSegment.my(thisLayer.id).label = "rh-nuc"
                log("Moved tag of segment " + lastSegment.label + " to following schwa")
                
              # if the last segment is *tagged* as linking...
              elif lastLabel == "linking":
                
                # double-check that it's *actually* linking; it could be erroneously tagged "linking" for one of two reasons:
                
                # 1. the gam rhotic token ends up as "dr" or "Dr" because of errors in Unisyn (in words with stems "modern", "northern", "southern")
                lastGam = lastSegment.my("gam segments")
                
                # if the previous gam label matches "dr" or "Dr"
                if badPattern.match(lastGam.label):
                  
                  # tag the current segment and remove the tag from the last segment
                  tag = segment.createTag(thisLayer.id, "rhotic")
                  lastLabel = lastSegment.label
                  lastSegment.my(thisLayer.id).destroy()
                  log("Moved tag of segment " + lastLabel + " to following schwa")
                  
                else:
                
                # 2. the "next segment" is not the next segment but the offglide in MOUTH-R/PRICE-R/FACE-R

                  # if there is a following segment
                  if follSeg is not None:

                    # if the following segment is a vowel
                    if vowelPattern.match(follSeg.label) is not None:

                      # if there's a following pause,
                      if follPause > 0:

                        # tag the schwa
                        tag = segment.createTag(thisLayer.id, "rh-glide")
                        # and change the label of the preceding tag
                        lastSegment.my(thisLayer.id).label = "rh-nuc"
                        log("Moved tag of segment " + lastSegment.label + " to following schwa")

                      # if there's no following pause
                      else:

                        # tag the schwa
                        tag = segment.createTag(thisLayer.id, "li-glide")
                        # and change the label of the preceding tag
                        lastSegment.my(thisLayer.id).label = "li-nuc"
                        log("Moved tag of segment " + lastSegment.label + " to following schwa")

                    # if the following segment is not a vowel
                    else:

                      # tag the schwa
                      tag = segment.createTag(thisLayer.id, "rh-glide")
                      # and change the label of the preceding tag
                      lastSegment.my(thisLayer.id).label = "rh-nuc"
                      log("Moved tag of segment " + lastSegment.label + " to following schwa")

                  # there's no following segment or following segment is unknown
                  else:

                    # tag as rhotic
                    tag = segment.createTag(thisLayer.id, "rh-glide")
                    # and change the label of the preceding tag
                    lastSegment.my(thisLayer.id).label = "rh-nuc"
                    log("Moved tag of segment " + lastSegment.label + " to following schwa")
              
          # remember the immediately preceding segment
          lastSegment = segment