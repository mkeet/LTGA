# LTGA LetsThink - GoAnswer

Project page: http://www.meteck.org/files/ltga/

## Aims

We aim to develop an ARS that has, at least, the following features: including figures, mathematical formula, proper HTML text--for display of diacritics--saving of the voting results of a session, display and saving of results (among others). It also has to be super easy to work with, fast, and with as few mouse-clicks as possible.
The core outcome of the project is a web-accessible ARS that can cater for various disciplines within one software system and that is simple and fast to work with. 

## Installation and usage notes

See the txt file. 

In addition: the python virtualenv is not included. It can be recreated from the requirements.txt and the alembic database schema  migration configuration and data layer. 
Also, the database password is embedded in peers/db.py, so in this code, it is changed to 'putyourpasswordhere'.

For the 'voting' page, the interface still says goanswer.co.za (see also screenshots below), but I stopped paying for the domain name (project funding ran out). You'll have to change that, too. 

Our current installation runs on a CS server at http://click.cs.uct.ac.za. Participants still can vote, but then have to use a different URL, like http://click.cs.uct.ac.za/students/question/96 for question 96 (rather than the goanswer.co.za), and for your installation it will be whatever the domain name of your instalaltion is.

For this current installation, there are a few loose ends, like don't lose your login (there's no password recovery) and at least a few computer science students in class always manage to find a way to vote multiple times (it won't happen with 'regular' participants).

## Examples (screenshots)

Administration interface; top of the page: <img src="http://www.meteck.org/files/ltga/newAdmin.png">

You also can create question groups to organise the questions by topic and questions can be moved between groups by draging and dropping them.


Administration interface; editing a question in the admin interface: 

<img src="http://www.meteck.org/files/ltga/Qcreation-finish.png">


Simple question, hiding and showing the results, respectively: 

<img src="http://www.meteck.org/files/ltga/simpleQresultsHidden.png">

<img src="http://www.meteck.org/files/ltga/simpleQresultsShown.png">


The same simple question in Spanish, mainly to show that diacritics indeed are supported (apologies for any translation errors): 

<img src="http://www.meteck.org/files/ltga/simpleQinSpanishDiacritics.png">


Question with figure and math display (and closed after voting): 

<img src="http://www.meteck.org/files/ltga/congestionwPicAndMath.png">


Answering a question - entering the question ID:

<img src="http://www.meteck.org/files/ltga/answer.png">


Answering a question (screenshot from the desktop interface; it works on the mobile as well): 

<img src="http://www.meteck.org/files/ltga/q26voteinterface.png">


Results are exported in csv and can be easily read into, say, OpenOffice's spreadsheet software, where the "Run" indicates the session (one can open, close, and reset the questions): 

<img src="http://www.meteck.org/files/ltga/resultsQ26.png">

## People

* <a href="http://www.meteck.org">Maria Keet</a> (PI), University of Cape Town (UCT)
* <a href="https://www.linkedin.com/in/yaseen-hamdulay-88766437/">Yaseen Hamdulay</a>, programmer (a CS Honours Student at UCT at the time now engineer at Google)
* There were CSC3002F networks block students who attended lectures at UCT where this was used and 'live tested'
* Input into the tool's requirements also from James Gain and Ian Schroeder at UCT


## Publications and dissemination

* Keet, C.M. An Experiment with Peer Instruction in Computer Science to Enhance Class Attendance. 23rd Annual Meeting of the Southern African Association for Research in Mathematics, Science, and Technology Education (SAARMSTE'15). Huillet, E. (Ed.), pp319-331. 13-16 January 2015, Maputo, Mozambique. (CRC: http://www.meteck.org/files/saarmste15KeetPI.pdf)
* "The LetsThink-GoAnswer audience response system" at the UCT's Teaching & Learning Conference on Oct 22-23, 2015.
* Blog post on the project/using the software:
    * <a href="https://keet.wordpress.com/2015/09/24/yet-another-software-based-clicker-system-letsthink-goanswer/">Yet another software-based clicker system: LetsThink -- GoAnswer</a>; Sept 24, 2015
    * <a href="https://keet.wordpress.com/2015/06/25/peer-instruction-with-a-computer-networks-course/">Peer instruction with a computer networks course</a>; June 25, 2015

