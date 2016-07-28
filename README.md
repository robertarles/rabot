# rabot
A personal daemon, growing bit by bit as I have time. It is now a flask app that is intended to be run privately.
This readme will get better as I go. For now, browsing the code should be relatively helpful as rabot is not very expansive yet.

Current:
* Weather checks (now based on current location)
* Location checks, for use by other functions (e.g. the previous item)
* Sending of twitter DM messages.
* Storage of activity using MongoDB

Planned:
* Weather checks will use location, but only if I'm far from home (~100 miles, assumes I'm just moving about a little bit)
* Weather alerts. Any urgent weather updates, like rain (I ride a motorcycle), thunderstorms, hurricanes, etc.
* News checks
* Document storage, notes, references, etc
* Image storage, planned OCR for search and conversion by the curator.

Redesign is pretty much done. Things are modular now [Flask rest api, vault.py for storage, comms.py for comms, curator.py to manage inputs storage and communications]  I've created the core flask app to be the api, to be called by cron jobs and by rabot itself. The comms module that will handle all messaging (twitter DM's for now), the vault module handles all data storage, and the curator module is be where all info is passed, and the curator will handle that data as needs.
