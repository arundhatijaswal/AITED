## TED 2.0

TED 2.0 is a web-based system that automates the process of generating a TED Talk-esque speech on a broad range of topics. Inspired by the TED A.I. XPrize, an upcoming competition focused on the automatic generation of a TED Talk, our main goal was to design and build a proof of concept that can eventually compete for the XPrize.  


Designed and developed by Amanda Anumba, Divir Gupta, Arundhati Jaswal, and Yang Zhang, our system can ideally accommodate any user, including users who want to prepare for a speech or debate, to improve oratory and public speaking skills, to get inspiration, or even to read a TED Talk-like speech. 


Usage
===========================

All essential files are located in the `flask` folder. In order to run the project, make sure all dependencies listed in the `requirements.txt` file are installed. Then, run the `views2.py` file (located in the `app` folder) in the terminal by executing `python views2.py` in your terminal. This will launch a localhost server where you can interact with the front end and see the live process from the terminal. 


Development
===========================
- `thesis2.py` generates a thesis from "debate.org"
- `TED_Talk.py` generates the entire talk. Inside the run function, the source of the thesis can be changed from "debate.org" to "NYT" to generate the thesis from New York Time's Room for Debate page
- `quoteTest.py` fetches a quote related to the topic
- `views2.py` is used for the front end with the additional features like the dictionary, avatar, etc.


Developers
===========================
***Amanda Anumba,***
***Divir Gupta,***
***Arundhati Jaswal,***
***Yang Zhang***
