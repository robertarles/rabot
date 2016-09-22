# rabot
A personal daemon, growing bit by bit as I have time. It is now a flask app that is intended to be run privately.
This readme will get better as I go. For now, browsing the code should be relatively helpful as rabot is not very expansive yet.

Its (over?)modularized now to allow expansion later. E.g. there is a comms and a curator to create a bit of a pipeline so that I can later add new input modules. I'm planning to add document and image input with OCR. The curator will properly tag and handle management of these sorts of inputs, where the comms module will be able to check (or call sub-comms) to check for new inputs in places like email, twitter, slack, web pages, etc.

Current:
* Weather checks (now based on current location)
* Location checks, for use by other functions (e.g. the previous item)
* Sending of twitter DM messages.
* Storage of activity using MongoDB
* Weather checks use location, but only if I'm far from home (~100 miles, assumes I'm just moving about a little bit)

Planned:
* Weather alerts. Any urgent weather updates, like rain (I ride a motorcycle), thunderstorms, hurricanes, etc.
* News checks
* Document storage, notes, references, etc
* Image storage, planned OCR for search and conversion by the curator.

Redesign is pretty much done. Things are modular now [Flask rest api, vault.py for storage, comms.py for comms, curator.py to manage inputs storage and communications]  I've created the core flask app to be the api, to be called by cron jobs and by rabot itself. The comms module that will handle all messaging (twitter DM's for now), the vault module handles all data storage, and the curator module is be where all info is passed, and the curator will handle that data as needs.
