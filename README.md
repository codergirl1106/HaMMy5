# HaMMy5

HaMMy v5.0 User Guide
Sophia Yan’s Python version of HaMMy4.0 developed by Sean McKinney and Taekjip Ha 

Reference:
McKinney, S. A., Joo, C., and Ha, T. (2006) Analysis of single-molecule FRET trajectories using hidden Markov modeling. Biophysical journal 91, 1941-1951, PMID: 16766620

HaMMy5 is an updated version in Python of its predecessor, 4.0, and is compatible with Mac and Windows V8+ (there are no public versions of Python 3 that support Windows V7 or below).

Downloading HaMMy5 GUI
----
HaMMy5 supports two operating systems: Windows and Mac. Download the folder that is compatible with your operator.

Starting the HaMMy5 GUI
---
For Mac Users:
1.	Download Python 3.7 or above 
2.	Find where the haMMy5_mac folder is located (by right clicking any file in the folder and moving to Get Info; copy the “Where:” )
3.	Open the computer’s terminal shell
4.	Terminal Commands:
1)	cd 'copied_file_path'
for example: 
cd '/Users/user/Dropbox/Manuscripts/HaMMy/haMMy5_mac'
2)	python3 HaMMy5_mac.py

For Window Users
1.	Download python 3.7+ (https://www.python.org/downloads/windows/)
2.	Open HaMMy5_windows.py

Using the GUI
----
Select the number of states you would like HaMMy to try to find.  This can have a significant impact on your results.  You want to pick a number low enough that HaMMy runs reasonably fast, but you also want to be sure that you are not biasing your results by forcing HaMMy to find what you already think is there.  Guessing 10 states (the maximum) will almost always work, except that it will run MUCH MUCH slower than fewer states.  Underestimating is always bad, so avoid at all costs.  I like to guess 2 states more than the number of states you actually think are there.

Next you must decide whether to provide initial guesses.  By default, HaMMy assumes FRET states are uniformly distributed from 0 to 1 and then starts trying to adjust them until a maximum probability is found.  Sometimes this does not work, for instance if you have a two state system where the two FRET levels are closely spaced (FRET levels 0.45 and 0.55), HaMMy starts out assuming levels at 0.33 and 0.67 and begins iterating.  In this case, HaMMy will converge to a single FRET level of 0.5 with a high level of noise.  This is because the initial guesses are so far away from the actual values that it becomes easier to get trapped in non-ideal parameters.  To overcome cases like this, you may use guesses to tell HaMMy where to start looking first.  If we had chosen 0.4 and 0.6 as our initial values on the two-state system just described, HaMMy would have found the true 0.45 and 0.55 states just fine.  

If you are running HaMMy with few states and those states are very close in FRET you should probably provide guesses.  If you are running 8 or 10 states that are distributed throughout 0 to 1 there is no need to provide guesses.

Once you have chosen your parameters, you may push the load button and select the files you wish to run HaMMy on.  The files will take some time to process, and are processed one at a time (so if the program is terminated midway through a batch of files, half the files will have completed).  

When it is done, it will quit automatically, and where your original data file was there should be two new files named *path.dat and *report.dat

Input files
----
Input files all must be ASCII files similar to the example_trace.dat file provided.  They need not have the same amount of whitespace characters between fields, as long as there is a white space (space, tab, return) between each number.  The file has the form:
<time> <donor intensity> <acceptor intensity>

If one input file is loaded, the GUI will display the donor and acceptor intensity plot as well as the FRET plot with HaMMy fitting. If fitting parameters are modified, press the “refresh” button to update the graph.

After setting the fitting parameters, batch input files can be uploaded together to do the fitting.

If one has to input initial guesses to display a more accurate fitting or would like to zoom in on a particular section of the graph, a .png will not be automatically saved (unlike when multiple files are simultaneously loaded). Click the “save graphs” button to save the modified graph as a .png.

Output files
----
*path.dat provides the actual idealized FRET trajectory in the form: 
<time><donor intensity> <acceptor intensity> <observed FRET> <idealized FRET>

*pathplot.png provides the plot based on the path.dat file.

*report.dat provides the model parameters which optimized the probability returned by the Viterbi algorithm.  Number of states is the number of states the user selected.  FRET peaks are where the algorithm believes states to be.  FRET sigma is how wide it believes the distribution of FRET values to be for each state (to obtain the full width half max, the sigma value must be doubled).  Signal sigma is not used and is an invalid parameter.  Entries in the report take the form:  
<start FRET> <stop FRET> <transition probability> <fraction spent> <transitions found>
Fraction spent gives what fraction of the entire FRET trajectory was spent in a <start FRET> state that eventually transited into a <stop FRET> state.  Transitions found gives the number of transitions in the trajectory that were of the type <start FRET> to <stop FRET>.  To convert a <transition probability> to an actual rate, multiply the <transition probability> by the data sampling rate (if you take data with 100ms exposures the sampling rate is 0.1*sec-1).  Note that rows with the same <start FRET> and <stop FRET> are illegitimate and are provided only for compatibility with TDP.

*dwell.dat provides for every transition found in the *path.dat the <start FRET> <stop FRET> <frames lasted> <time lasted>
where <time lasted> tells how long (dwell time) the molecule was in <start FRET> before transiting to <stop FRET 

Some pointers
----
1.	Before trying to analyze a FRET trajectory, make sure that there is signal through the whole trace.  Since the algorithm looks simply at FRET values the random FRET values obtained when a molecule has gone dark confuse it.  Therefore, if at some point during the trace the donor has blinked or photobleached, that portion of the trace needs to be removed first.
2.	Check the output of some files to make sure it is reasonable before blindly trusting the output.  I have run into cases where a person’s data had the donor blinking every few dozen frames at a 1 or 2 point time scale while they were trying to look at rare dynamics on the 100-200 point time scale.  Naturally HaMMy found the donor blinking dynamics and not the dynamics of interest.
3.	If you are getting something you really don’t expect, try providing initial guesses.
4.	States must be distinct!
a.	Do I see discrete states or a gradual change?
b.	Gradual change=>no HaMMy
5.	States must be AT LEAST 0.03 FRET apart
a.	No trying to find 1bp sized substeps
6.	Good rule of thumb:  if you can sort of see where the states are by eye but cannot begin to do quantitative analysis, then try HaMMy
7.	Transition probabilities should be constant for the whole trace.
a.	Systems exhibiting multi-exponential kinetics can often still be analyzed and *path.dat and *dwell.dat will remain relatively good indicators
b.	*report.dat’s TPRs will not be appropriate however
c.	The same holds true for changes in behavior (fast kinetics->slow kinetics) happening during the trace
8.	FRET states should be between 0 and 1!
a.	If you think states are outside that range, you will have to scale your data
9.	If D or A is decrease or increase during the trace (defocusing, background photobleaching etc.) then they must do so in a way that preserves FRET values
10.	If A is gradually decreasing because the surface has a huge background of acceptor only molecules that are slowly photo-bleaching, then A/(D+A) changes regardless of how your molecule is moving and a FRET state at 0.7 slowly moves to a lower FRET value
