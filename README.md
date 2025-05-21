# Voice-Activated-Bartending-Table
This piece of furniture looks like a regular table, but underneath is a hidden secret. Powered by a raspberry pi 4, this table uses a series of pumps and servos to quickly and discretely mix cocktails with voice commands. Meant as a little fun party bot to show off to friends and family.

### How it works
Using a Vosk voice to text model, I transcribe audio input from a microphone into a string which I parse for an activation phrase and turn on an indicator LED to let the user know that the table is ready for a command. There are several recipes I have added in a dictionary with the keywords being the names which I parse from the text. Then using the gpio python library I lower the platform via a stepper motor and use a sensor to check if there is a glass on the platform before beginning to make the cocktail. Then I can control 12 pumps set up to pump a set list of drinks using recipes I find online for various cocktails and voila, a drink without even getting up.

## Outside
![PXL_20240218_002457868 MP](https://github.com/Angeraa/AI-Bartending-Table/assets/82167983/2037c1fd-068a-493b-a3e4-80e2fe5d3143)

## Inside
![PXL_20240102_001342462 MP](https://github.com/Angeraa/AI-Bartending-Table/assets/82167983/9c4ec096-0817-44db-8f91-0428dec37ee3)
