After a DVR recording (in my case from ChannelsDVR), this script will hard link files from the `watch_path` to the `dest_path`.

The primary use is to move a finished recording into my Plex folder structure.

---

### Config

#### Environment variables:
- Required
  - `watch_path` Points to the folder which will be monitored for new files. Files can be nested in folders.
  - `dest_path` Points to the folder in which recordings will be moved to.
    - Subfolders will be defined in the `mappings.json`
- Optional
  - `max_write_time` Defines the maximum amount of time the script will wait for a file to stop increasing in size

#### mappings.json:

The `key` of the items in the `mappings.json` file is the name of the recording that the script looks to match against
new files being created in the `watch_path`. The `value` of each dictionary item is the folder that the recording will
be placed in the `dest_path`.

The `mappings.json` file should be mounted to `/app/mappings.json`.

---

```commandline
docker run -d \
  -e watch_path=/media/incoming \
  -e dest_path=/media/processed \
  -e max_write_time=120 \
  -v /path/to/your/mappings.json:/app/mappings.json \
  -v /path/to/your/media:/media \
  benfugate/move-dvr-recordings
```

---

Scripts in Tautulli are set up to refresh Sonarr so the episode can be monitored and managed after this is done:

https://github.com/benfugate/hide-episode-spoilers/blob/main/config/scripts/JBOPS/utility/refresh_sonarr_show.py