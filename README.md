This script has a very specific use case.

After a DVR recording, Plex is placing the files for The Challenge and Big Brother in folders based on the Episode Program Guide(EPG).
show name. This is incorrect, and the files should be placed in their matching folders based on my folder structure.
That is why we are placing the videos in the temp storage directory to begin with, instead of using a container like "post_processing".
This will cause Plex to refresh metadata, and properly show the recorded episode as expected.

Another issue this script solves, is 'Big Brother' currently has the incorrect episode numbers (Season 24) from the EPG.
This script gets around that issues by renaming the episode to represent the correct number, and move the renamed file from
the temp storage directory to the "Big Brother (2000)" folder mounted to "/dest/".

Scripts in Tautulli are set up to refresh Sonarr so the episode can be monitored and managed after this is done.

`https://hub.docker.com/repository/docker/benfugate/move-dvr-episodes`