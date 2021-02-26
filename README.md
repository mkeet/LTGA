# LTGA LetsThink - GoAnswer

Project page: http://www.meteck.org/files/ltga/

## Aims

We aim to develop an ARS that has, at least, the following features: including figures, mathematical formula, proper HTML text--for display of diacritics--saving of the voting results of a session, display and saving of results (among others). It also has to be super easy to work with, fast, and with as few mouse-clicks as possible.
The core outcome of the project is a web-accessible ARS that can cater for various disciplines within one software system and that is simple and fast to work with. 

## Installation notes

See the txt file. 

In addition: the python virtualenv is not included. It can be recreated from the requirements.txt and the alembic database schema  migration configuration and data layer. 
Also, the database password is embedded in peers/db.py, so in this code, it is changed to 'putyourpasswordhere'.

## Examples

Administration interface; top of the page: [Question administration interface for the lecturer]


Administration interface; somewhere further down on the page, using question groups to organise the questions by topic (questions can be moved between groups by draging and dropping them): [Question administration interface for the lecturer]


Administration interface; editing a question in the admin interface: [Editing a question]


Simple question, hiding and showing the results, respectively: [Question and hidden restults] [Question adn restults shown]


The same simple question in Spanish, mainly to show that diacritics indeed are supported (apologies for any translation errors): [simple question in Spanish, with diacritics]


Question with figure and math display (and closed after voting): [Question with figure and math display]


Answering a question - entering the question ID:
[Answering a question - entering the question ID]


Answering a question (screenshot from the desktop interface; it works on the mobile as well): [Answering a question]


Results are exported in csv and can be easily read into, say, OpenOffice's spreadsheet software, where the "Run" indicates the session (one can open, close, and reset the questions): [Viewing exproted restults]


## Publications and dissemination

* Keet, C.M. An Experiment with Peer Instruction in Computer Science to Enhance Class Attendance. 23rd Annual Meeting of the Southern African Association for Research in Mathematics, Science, and Technology Education (SAARMSTE'15). Huillet, E. (Ed.), pp319-331. 13-16 January 2015, Maputo, Mozambique. (CRC: http://www.meteck.org/files/saarmste15KeetPI.pdf)
* "The LetsThink-GoAnswer audience response system" at the UCT's Teaching & Learning Conference on Oct 22-23, 2015.
* Blog post on the project/using the software:
    * <a href="https://keet.wordpress.com/2015/09/24/yet-another-software-based-clicker-system-letsthink-goanswer/">Yet another software-based clicker system: LetsThink -- GoAnswer</a>; Sept 24, 2015
    * <a href="https://keet.wordpress.com/2015/06/25/peer-instruction-with-a-computer-networks-course/">Peer instruction with a computer networks course</a>; June 25, 2015

