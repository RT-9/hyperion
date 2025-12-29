# Notes for development

## Show development process

1. Create showfile
2. Patch devices
3. Create Scene
4. Create Cue (based on scene)

## Play Mode 

1. Pull Showfile
2. Pull Patched devices
3. Pull Cues
4. Pull Scenes
5. Calculate DMX Values for the $nth$ and $n+1$ cue

If any live interaction is happening (e.g. overrides) those things get püushed to redis.
