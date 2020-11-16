# sub-g
A framework for building Subsonic connectors (and possibly other skills/actions) for smart speakers.

This was heavily inspired by: [https://github.com/ctrlaltca/google-home-subsonic](https://github.com/ctrlaltca/google-home-subsonic)

I have rewritten the Subsonic class in Python, and interfaced with a few more endpoints.

I know there are several things that still need to be done, and I need to create some good solid documentation on using 
the current version of Google's Action console.

The most helpful documents for converting from the PHP project above have been the WebHookResponse documentation on 
Google

* https://developers.google.com/assistant/conversational/prompts
* https://developers.google.com/assistant/conversational/prompts-media#json_1

I also plan to build an Alexa/ASK response class, since I have code for an Alexa skill in one of my other projects 
already...and now have this:

* https://developer.amazon.com/blogs/post/Tx1DSINBM8LUNHY/new-alexa-skills-kit-ask-feature-audio-streaming-in-alexa-skills

I can also see these coming in handy:
* https://pypi.org/project/ssml-builder/
* https://pypi.org/project/skillful/

The oAuthprovider is just started, really doesn't do oAuth and is specifically for Django Rest Framework but I intend to 
make it possible to link Subsonic accounts with Google's Account linking process in the future....and for this whole 
project to at least have examples for Django and Flask.

So far, this is what I was able to hack together in a few hours over the weekend.  My ultimate goal is to be smart 
speaker agnostic.

Wish list:
* Account linking for both Alexa and Google Assistant
* Ability to integrate with MyCroft.AI
* Ability to integrate with HomeAssistant
* Ability to integrate with Almond

