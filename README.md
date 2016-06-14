#rabot
A personal daemon, growing bit by bit as I have time. It is now a flask app that is intended to be run privately.
This readme will get better as I go. For now, browsing the code should be relatively helpful as rabot is not very expansive yet.

Current:
* Weather checks.
* Sending of twitter DM updates.
* Storage of activity (using MongoDB)
Planned:
* News checks.
* Document storage, notes, references, etc.
* Image storage, planned OCR for search and conversion by the curator.

I'm currently focusing on design/re-design. I've created the core flask app to be the api, to called by cron jobs and by rabot itself. There is a comms module that will handle all messaging (twitter DM's for now), a vault module that will handle all data storage, and the curator module. The curator will be where all info is passed, and the curator will handle that data as it sees the needs.
