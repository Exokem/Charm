INTRODUCTION
------------

Charm is an interactive console program that processes user input. Its interpretation of information is based almost
entirely on user input. 


EXISTING FUNCTIONALITY
----------------------

Presently, Charm will respond to input simply, firstly attempting to identify the part of speech that an unknown word
belongs to. Afterwards, Charm will ask the user to provide a definition for words that are known, but only when the 
user input is one word. Charm will, at some point following the successful identification of an unknown word, ask the 
user to provide a save phrase, which will be used thereafter as a command to save any new information. Charm does not 
know how to store information without instruction. 

Word data is stored in data/words in the format 'word,PART_INDEXES,DEFINITION,KEYS'. Keys are unimplemented but will
support more detailed analysis of input, including sentences. This format may be replaced with one that is more
efficient as the program becomes more complex. 

User data is stored in data/user_data. Line one is dedicated to the presently static alphabet, which will be 
modifiable by the user in the future. The second line holds the version, which is dynamically changed on startup to
represent the number of words Charm has learned. It will be changed further to include the last three letters of the 
user-specific alphabet. The format of this version is RELEASE.FEATURE.BUG-X.WORDS-xyz. The third and fourth lines
respectively hold the save phrase and greeting that Charm will use. The greeting is not yet implemented. 

When the user enters the defined save phrase, both data files are wiped and their contents are replaced with their
updated values. The separate parts of each line are separated with commas. 


PLANNED FUNCTIONALITY - CLOSE
-----------------------------

 * User-specific greetings on startup
 * More interactivity options to enhance detail of word index


PLANNED FUNCTIONALITY - DISTANT
-------------------------------

 * Sentence processing - tone, grammar, question answering