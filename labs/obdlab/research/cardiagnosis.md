Radovan MARI
Car diagnostics
step by step
OBD diagnostics without the use of devices
OBD I diagnostics
OBD II diagnostics
The most common causes of DTC faults
ECU Flashing and Mapping
EVAP system
Immobilizer
Radio decoding
Control Module or ECM/PCM repair
4
Author
Radovan Marin
General Automobile Engineer
British Institute of Engineering Technology
Aldermaston College
Reading, England
Reviewer
Dr. sc. Darko Biljaković
Editor
and
Graphic design
Radovan Marin
Publisher

Zagreb, January 2013.
ational University Library in Zagreb
ISB 978-953-95888-4-5
d.o.o.
ZAGREB
Kamaufova 2
www.auto-mart.hr
 5
R E V I E W
 When a failure occurs on our car, the first step that we expect from our
servicer is accurate or nearly accurate diagnosis, because misdiagnosis
has multiple unwanted consequences. To be able to determine what is not
working properly, we have to move in the direction our author went. First
we have to learn how the modern car works, and than we will be able to
figure out how to detect failure. The diagnosis is generally result of experience and a multidisciplinary synthesis of knowledge. Therefore, a new
book of Mr. Radovan Marin “Car diagnostics” connects his previous
books, “Automobile electronics & 4-stroke engines” and “Automobile technology”.
 And this time I am pleasantly surprised by the new interesting data and
high quality of expression, as well as with a great number of images. With
this book, author has increased the value of his previous books, which
now form a complete trilogy.
 With a risk of repeating myself, I must point out that author has chose
the type of presentation which is a happy compromise of a lot of conflicting requirements such as high skill, legibility, convenience, didacticism
and methodology.
 After these three books, it becomes apparent that Mr. Marin is a person
with the rare gift of true professionalism, eager for new knowledge, and
more importantly, with the gift of a good writer and a desire to convey his
knowledge to a wider population. As new technologies are rapidly developing, I am confident that in due time we shall witness new books about
our pets on four wheels. I strongly recommend purchasing of the entire
trilogy, because that would make every part of it to be worth more than it
would have been separately.


 Dr. sc. Darko Biljaković
6
 7
F O R E W O R D
 After a great acceptance of previous two books "Automobile electronics
& 4-stroke engines" and "Automobile technology", automobile technicians
showed further interest for detailed explanation of vehicles diagnostics
and usage of diagnostics equipment. With this third book, the theory of
automobile mechanics, electrics and electronics on modern cars is generally covered. By mastering content of these three books, technicians will
undoubtedly acquire basic knowledge to deal with most problems on
automobiles. Acquired theoretical knowledge accompanied with everyday’s practical work, which always brings new experiences, will definitely
create a very professional automobile craftsman. It is quite understandable, that acquired knowledge has to be complemented by following new
technologies and modifications of existed.
 We should be aware of the fact, that diagnostics programs are sometimes very complex, and have to be considered very seriously. If we would
go in details explaining all functions of particular programs and problems
related to diagnostic trouble codes, a book of several thousands pages has
to be written. This book should provide even more than just fundamentals
of car diagnostics, but certainly not complete knowledge which is gained
by experience and further learning. Therefore, before using a particular
diagnostic program, it is recommendable to study all available literature
about it.
 With such introduction about the principles of diagnosing faults, and
assuming that we have mastered the theory from previous two books, we
will surely be able to deal with diagnosed problems and eliminate them.
 During the writing of these three books, in addition to several decades of
experience, all worldwide available literature related to this subject matter was used. Beside the literature composed by several authors, knowledge and experiences of individual authors are used too. As it is evident
from the books contents, examples are shown from a range of programs
and automobile data. Just because of so great number of literature and
programs used in these books, the sources, titles and authors are not mentioned by name.
 Author

8
CAR DIAGOSTICS ........................................................................................... 10
Electronic Engine Management ...................................................... 10
Diagnosing an engine failure without the use of devices ............... 12
SRS diagnostics without the scanning device ................................. 19
ABS diagnostics without the scanning device ................................ 22
Resetting service intervals without the use of devices ................... 24
OBD I ................................................................................................. 25
Diagnosing failure with diagnostic device .,.................................... 25
K and L diagnostics lines .................................................................. 27
KL diagnostics ................................................................................... 29
Installing KL interface and software .............................................. 33
OBD II ............................................................................................... 48
Using the OBD II software and interface ....................................... 52
Handheld scanners ........................................................................... 65
OBD II and new vehicles .................................................................. 67
Pending codes P0xxxx * ................................................................... 69
The most common causes of trouble codes .................................... 70
O2 sensor DTC problems ................................................................. 70
MAP sensor DTC problems ............................................................. 72
TPS sensor DTC problems ............................................................... 73
Content:
 9
CTS sensor DTC problems ................................................................ 75
Misfire DTC problems ....................................................................... 78
EGR valve DTC problems ................................................................. 80
CKP sensor DTC problems .............................................................. 82
Turbocharger DTC problems ........................................................... 84
Wideband O2 sensor with 5 wires .................................................... 85
Evaporative Emission Control System (EVAP) .............................. 87
ECU Flashing i Mapping .................................................................. 89
Immobilizer ........................................................................................ 95
Additional protection from car theft ............................................... 101

Radio decoding ................................................................................... 108
Car parking sensor system ................................................................ 112
Control Module or ECM/PCM repair ............................................. 116
Transistor testing ............................................................................... 120
Resistor testing ................................................................................... 124
Capacitor testing ................................................................................ 126
Cruise control ..................................................................................... 129
Start/Stop system ............................................................................... 135
Regenerative braking system ............................................................ 138
HHO .................................................................................................... 139
10
 Electronic Engine Management
 In the previous two books, Automobile electronics & 4-stroke engines and Automobile technology, it
is pretty thoroughly explained the
principle of new types of petrol
and diesel engines, as well as electronic engine management and
other car components. Bearing in
mind that users of these two previous books have studied them, and
they are now clear with a function
of the electronic management and
its associated components, i.e. sensors and actuators, in this book we
will proceed with process of diagnosing faults in the electronic system using diagnostic devices, and
without them on the types of vehicles where it is predicted by manufacturers.
 The concept of basic diagnostics
was explained in the first book:
OBD diagnostics, protocols and
use of diagnostic tools. With this
basic knowledge many people was
enabled to use diagnostics tools
and understand the purpose and
possibilities of their use in combination with the acquired knowledge about the function and manner of testing sensors and actuators in the vehicles. All those who
have used their newly acquired
knowledge in practical application
are aware of its complexity and
almost daily updating demand. So,
let’s go ahead, or continue in following order.
 In the beginning, let’s recapitulate our knowledge related to the
electronic engine management and
transmission under the common
name Powertrain.
 Engine computer, or we can say
command center, in which all the
information are flowing in from a
wide range of sensors and commands are sent out to a range of
actuators is known as ECU, or on
the newer cars PCM Powertrain
Control Module.
 Lambda probe or O2 sensor provides information about saturation
of carbon monoxide in air-fuel
mixture after combustion. On the
base on received information the
computer adjusts the mixture, constantly keeping proper air-fuel ratio and thereby minimizing fuel
consumption and emission of
harmful gases. In newer cars an
additional lambda probe is fitted
and located behind the catalyser or
downstream. This probe measures
the final value of emissions and
may also indicate a malfunction of
the catalyst. Lambda probe is
somehow popular among mechanics to cause a series of failures, and
often interpreted as the cause of
problems related to improper engine operation. Lambda probe
malfunction will cause increased
fuel consumption, performance
loss and increased emissions, but
the engine will still operate satisfactorily. amely, in the case of O2
sensor failure, computer will conCAR DIAGOSTICS
 11
trol injectors by spare installed
program which will regulate the
amount of fuel injected relying on
following parameters: engine
speed, intake air quantity, etc. In
other words, the dosage of fuel
based on these parameters will be
quite correct, but not ideal as in
the case of the properly functioning probe.
 Coolant Temperature Sensor
CTS is very important for the engine cold starting and driving before the engine reaches operating
temperature. Having received information about the engine coolant
low temperature, computer will
inject greater amount of fuel and
proportionally reduce it as the
temperature increases. After
reaching operating temperature,
the computer will rely on the parameters received from lambda
probe.
 Parameters of the TPS, throttle
position sensor, on the engine inlet
manifold, computer will use, along
with other sensors parameters, for
proper ignition timing and fuel
dispensing. One of the most important data of this sensor is sudden
acceleration, when computer have
to inject a greater amount of fuel
to avoid the engine sudden stoppage (dead spot) caused by entry
of large amounts of air into the engine.
 MAF, mass air flow sensor, provides the information about the
amount of intake air at certain engine speed which computer will
use in the calculation of fuel dispensing.
 Depending of the type of engine,
MAP manifold air pressure sensor
and IAT, intake air temperature
sensor, can be installed in conjunction with the MAF sensor or without it. The parameters of these two
sensors will further assist in the
proper dosage of fuel, depending
of intake air temperature and engine load.
 Engine crankshaft position sensor CKP at any point shows the
position of the crankshaft and pistons. Data from this sensor will
allow the engine computer determining the exact moment of fuel
injection and spark on the spark
plugs. This is the only sensor due
to which failure engine will not
run.
 Besides the CKP sensor, on
higher performance engines one or
two camshafts CMP sensors are
fitted too. These sensors send information about the exact position
of camshafts and thus the exact
time of engine valves opening and
closing which facilitates accurate
calculation of ignition timing and
fuel injection.
 Knock sensor records the vibrations, or knocking, caused by the
detonations inside the engine cylinders. The received signal computer
will use to adjust the ignition timing and prevent premature ignition of the mixture due to inadequate fuel octane value or higher
engine loads.
 These sensors are an integral
part of the today’s car engine
management. Additionally, depending on the type of vehicle, we
12
will find a number of other sensors
on the engine which further improve engine function and performances. As sensors are essential
for proper engine functioning, so
they exist in other vehicle devices
too: transmission, ABS, air conditioning, SRS ... controlled by separate modules or computers.
 On today's cars, it would be
impossible to achieve high performance and simultaneously satisfy global regulations related to
pollution emissions, without the
use of electronics. Very rigorous
emission regulations forced the car
manufacturers to introduce a very
complex electronic engine management which increased production
costs. On the other hand, new
technologies have multiplied and
improved engine performance,
thus saving on the production of
robust high capacity engines that
have been, until now, incorporated
into high-performance cars.
 Electronic vehicle’s management, at first glance, seems quite
daunting. However, if the material
from the previous two books has
been mastered, with the help of
instructions in the following chapters and the various, now available, diagnostic tools at affordable
prices, and even without them in
some cases, we will be able to diagnose the most failures in the electronic car systems. Why the most?
It is not uncommon for the DTC to
occur as a consequence of other
DTC, in which case it takes a lot of
knowledge and experience that is
gained over time to solve the problem. In any case, using the current
knowledge and some effort, we will
be able to diagnose even such failure by eliminating consequential
DTC on the basis of checking the
validity of some electronic elements, and logical conclusions derived by linking their functions
and interactions.
 Diagnosing an engine failure
without the use of devices
 As already mentioned in previous publications, OBD or On
Board Diagnostic means that the
engine computer diagnosis DTC of
electronic systems and stores them
in the form of codes in its memory.
Some carmakers have predicted
the possibility of accessing the
codes without diagnostic devices. It
is mostly the case on Japanese
cars, not late models, and can be
also found in most European car
models.
 As on the newer cars generation
almost nothing is simple, even such
process of diagnosis will not be
possible without the assistance of
provided auto-data. As each type
of car has a specific way to access
data from the engine computer, we
need to find the vehicle manufacturer's instructions. Such information can be found in various commercial vehicle data programs,
which are conducted under various names. One of the most popular is Autodata. In the lack of such
commercial data, a little wiser and
more persistent may seek instructions on the Internet.
 For the first example to diagnose failure on the engine elec-
 13
tronic management we will take
the car model Honda Civic 1.4
made 2000. Here we shall use the
instructions from the one of many
databases available Autodata. In
browser we choose: the year of
manufacture, brand and model of
vehicle. In the right column we see
the capacity of engine installed in
this model of this car, and at the
bottom of the page we can select
the type of engine selected by serial number and power. In the
program header, we will select the
option to diagnose trouble code or
DTC. By clicking on the selected
14
option, two additional options are
offered: engine management and
air bags. To begin, we choose the
first option. On the newly opened
window we can immediately notice
the ability to diagnose without the
assistance of the diagnostic device.
In fact, otherwise in the right column only one sentence would be
written which indicates that access
is only possible with diagnostic device. In such happy circumstances
where we can access the data from
the computers without diagnostic
equipment, fault diagnosis can be
approach in the following order: in
the left column, we are offered 5
different connectors for plugging
diagnostic devices (in most cases it
is just one) and sketch of its position in cab car. Concluding that in
our car we have connector with
only two terminals, we shall select
Type 1 solution. In the case of connector with multiple terminals, we
shall click on different type of connector opening its sketch. Choosing connector identical to the vehicle’s we are prompt to the option
of general information. In the
right column of the new page we
get information to read error
codes by counting the flashes of
the MIL light, actually the same
light which warns us about the
faults in electronic management.
 Further information from this
site in our case is not so important,
and therefore we shall go directly
to the option on the left, or: Accessing data. On this page, in the
column on the left we see the connection or connector where terminals 1 and 2 are bridged with a
piece of wire. Let’s go to the right
column of the page and follow the
exact procedure describing accessing data. Instructions go in this
order: bridge terminals 1 and 2 on
two terminals connector, do not
 15
bridge the terminals on the three
and five terminals connectors,
switch the ignition O, count the
flashings of MIL light on the instrument panel, write down the
codes defined by flashings and
compare them with the code’s table. If the MIL light illuminates
constantly, there are no faults
stored in the engine computer.
Further on, follow instructions
how to read trouble codes by
counting flashings and following
pauses between them. Error codes
16
from 1-9 are shown in the following order: the number of short
flashings followed by short breaks
indicates the error code. In this
case, the code number 3 is visible
on the sketch in the lower left corner of the column. A longer pause
between flashings separates the
codes, or we read the new code.
Error codes with values greater
than 9 are read as follows: a longer
duration of flashings indicates the
value 10, each following brief flash
followed by short break has a
value of 1, long pause marks the
end of the code and next code
comes up if exists. On the previous
sketch in the lower left corner we
see an example of the existing code
under the number 12. If read code
is not clearly listed in the code’s
list, we can suspect a malfunction
of the engine computer.
 Reading out error codes, diagnostics procedure is completed and
we can proceed with deleting codes
after we have written them down
on a piece of paper. ow, we can
return to the left
column of the
page and select
Erasing or deleting. Clicking this
option a new page
opens where we
find the instructions for DTC removal on the right
side of the page:
turn the ignition OFF, remove the
wire that we bridge the terminals,
remove the fuse of 7.5 A sketched
on the left, and put it back after 10
to 15 seconds. There are two
sketches of the fuse, depending of
the engine type listed on the right
side. The DTC can
be also erased by
removing one of
the battery terminals for 10 to 15
seconds.
 Finally, like
all other jobs
when they are
done, they look
simple and easy.
However, finishing diagnostics
 17
and erasing DTC we have not
solved the problem nor do we
know where the problem lies.
Therefore let’s move further on to
decipher recorded codes. On the
left side of the shown window,
choose the option Trouble code
identification. The newly opened
site contains a list of DTC definitions.
 Suppose that we have read the
above mentioned diagnostic trouble codes 3 and 12. In DTC definition list under number 3 we see the
problem related to the MAP sensor, but not the advice to replace
it. So, now we are back on knowledge. This definition gave us only
the orientation to the sector of possible problem. To be certain that
we are properly eliminating existing problem without unnecessary expenditure, it
is necessary to know what
the MAP sensor is and
how it works. The DTC
description points to the
possibility of problems
with the wirings, connector and sensor itself or
even the engine computer.
So if we have learned
from previous books how the sensors work, we will be able to test
the sensor itself as well as the
power supply. After we carried out
all possible checking, we can conclude with great certainty where
the problem lies. Similar case is
also with a code 12 which indicates
a problem with the EGR valve.
And here we get only the orientation about the problem, because
the problem may lie in the wiring,
vacuum hoses, EGR solenoid valve, the valve position sensor, EGR valve or
finally in engine computer. Therefore, we need
to know how the EGR
valve works, to be able to
determine with certainty
where the problem lies.
This diagnostic procedure
clearly shows how diagnosis of vehicle’s electronics management, with the device or without it,
is not a magic where we can point
out the problem with the finger
and say: this is the part which has
to be replaced. In other words,
only after the diagnostics is performed, the right knowledge comes
to the fore. Certainly there are
18
cases where the problem is solved
by changing certain elements, but
I would classify such cases into the
lottery game, rather than professionally performed work. But if we
still want to perform our job professionally before we bring our self
and customer in an unenviable position regarding possibility of unnecessary and non small investment in repair which is caused by
changing parts in the order of
elimination until the error is removed, we will use these databases
which provide information of each
element value during the testing.
For example, in the trouble code
line number 3 we have the possibility of entering the MAP sensor
page by clicking on the highlighted
text and find the description of error. By selecting this option, we
will find the sensor testing description and all sensor values which we
have to obtain during the test. Just
like with diagnosis, and here we
find the instructions and drawings
for sensors testing. Sentences are
short and relatively easily understandable. The sequence is very
similar to the preceding. Check the
power supply: turn ignition off,
unplug the connector from the
MAP sensor, turn ignition on,
check voltage between terminal 1
and the earth, check the voltage
between terminals 1 and 2. In both
cases, the voltage should be about
5 volts. Check the MAP sensor signal: turn ignition off, do not disconnect connector and approach
connector terminals with voltmeter from the outer side, switch ignition on, check the voltage between terminals 1 and 2 whose
value should be about 3 volts. So
verifying power from the engine
computer and the sensor signal
voltage, we can easily guess
whether the problem is associated
 19
with the sensor, wiring, connector
or the engine computer. DTC 12 in
this database does not have a test
description as it was the case for
MAP sensor, but if we go back to
the EGR valve chapter in our book
Automobile electronics & 4-stroke
engines, we will be able to make
very quality valve, sensor, and wiring tests.
 Described diagnosing procedure
without the use of diagnostic devices is identical in all types of vehicles. Of course, every type of car
has a different terminal bridging.
That's why we need instructions
for a particular model that has
data access from the computers in
the described manner. How to
know which vehicles can be diagnose this way? For this kind of information it is necessary to have
one of sketched data, workshop
manual for particular vehicle or
with a little effort information can
be found over the Internat. This
last method is a bit complicated,
but perseverance is often rewarded. When using the Internet,
it is always recommended to consider the usage of closest key
words to find what we are seeking.
Let’s say that we are trying to find
a workshop manual to diagnose
Honda car without the diagnostic
device. Appropriate key words
would be: How to access DTC on
Honda by MIL or how to access
error codes using MIL lamp on
Honda vehicles. These and similar
concepts, will surely lead us to a
title in which we can find the instructions we need. Surely, such
process is sometimes time consuming and laborious, but with a lucky
hand, it may happen that at first
attempt we get the right information. Frequent use of Internet to
obtain the required data, will leave
a positive mark in terms of memorizing professional terminology
which will spontaneously very
quickly get into the everyday’s use
of professional expression.
 As we saw at the beginning of
this chapter, when choosing a diagnostic failure, in addition to the
engine management we are offered
the option of diagnosing failure of
ABS and SRS Supplemental Restraint System, whose translation
could be: an extra stop system
linked to existing, referring to already installed seat belts. Well,
let’s now perform diagnostics on
air bag system in the same vehicle.
 SRS diagnostics without the
scanning device
 Getting back to the menu, we
shall now select the option Airbags.
After new page is opened, a new
menu is offered with general data
on the top. On the right hand side
we can notice instruction to perform diagnosis without the scanner and reading DTC again by
counting MIL flashings, in this
case SRS MIL light, while in the
lower left corner we see the position of the connector, or DLC, for
diagnostic scanner. Moving to the
next page by clicking on Accessing
Trouble Codes, we find the instructions to access information from
20
module or SRS computer, and on
the left side we can see the drawing
how to bridge the terminals. Here
is the procedure of diagnosis on
the right side of the page: turn ignition OFF at least for ten seconds,
find the connector (sketched) with
two terminals, bridge the terminals, switch ignition O, the SRS
light flashes six seconds, if there is
an error MIL starts flashing, write
down the number of flashings and
compare them with the codes on
the list. Each error, or DTC, consists of two groups. Long flashings
indicate the tens and short ones
single numbers. Short pause separates flashings,
long pauses are
separating codes.
As an example,
code 12 is shown
in the sketch in
the lower left corner. Finally, turn
ignition OFF for
ten seconds and
remove the bridge
wire (jumper).
Module or SRS
computer can also be tested by diagnostic device connected to DLC.
 ow we can proceed with erasing stored codes by clicking on the
option Erasing Trouble Codes and
following the instructions: turn
ignition OFF, find two pin SRS
connector to delete the stored data
(sketched in the left corner of the
page), bridge the terminals, switch
ignition O, the SRS light flashes
six seconds, remove bridge wire
within four seconds after MIL is
turned OFF, the
MIL lights up
again, bridge the
connector terminals again within
four seconds, light
goes out, remove
the jumper within
four seconds after
the MIL turns
OFF, light flashes
twice and errors are eliminated
from the SRS module, turn ignition OFF.
 Finishing diagnostics procedure
we can proceed with a definition of
 21
trouble codes by switching to
Trouble Code Identification page.
On the right side of the page we
look for read
DTC number 12 and
interpret the
d e f i n i t i o n
which says:
great resistance on the
driver's airbag. The
p r o b l e m
may be related to the
wiring or
connector, the airbag unit or the
SRS module. As
we see in the description of the
code, there is only
an orientation to
the problem but
does not give a
much of advice.
But, at least we
know in which
bush the rabbit
lies. Thus, we have to check the
contacts and the wiring of the
driver airbag unit. If that does not
encounter a noticeable problem,
we can move on to
test the air bag
unit. Knowing
that the airbag is
activated by electric igniter, we can
assume that there
is some resistance
on air bag unit
terminals, but
22
what is its value? The resistance
value has to be found in the manufacturing literature, workshop
manual, or again over the Internet.
When we find the value of resistance, we can verify it with assistance of Ohm meter. If the measured resistance value significantly
differs from the specified, the
problem lies in
the air bag unit.
 In both diagnostic cases we
jumped to the
DTCs erasing
procedure before we solved
the existing
problems. It is
quite obvious
that failure has
to be eliminated
before deleting
DTC from memory, otherwise it
will appear again. But sometimes
there are trouble codes memorized
in module’s memory but we can
not see that there is anything
wrong with engine or other systems electronic management. In
such cases, we can erase DTCs and
see if the same will occur again. In
fact, sometimes the DTC is saved
due to some other circumstances
while driving, and how it appeared
so it disappeared. However, the
computer registers a problem, regardless of its duration and never
deletes it by it self. Therefore, if we
doubt the existence of a fault, regardless of the stored errors, we
can erase DTCs, and after a short
drive repeat the diagnosis.
 ABS diagnostics without the scanning device
 The problem with the ABS MIL
which illuminates because of malfunction of the ABS system can
also be solved in a similar manner
as the previous two on this vehicle.
If we select option ABS Component
Testing, the program will show us
a menu similar to previous with
the instructions of the availability
to access the codes without the use
of diagnostic devices. In the option
Accessing Trouble Codes we follow
the instructions: turn ignition
OFF, bridge the terminals
(sketched), switch ignition O,
ABS light starts flashing, longer
flashings indicate tens and short
single numbers, short pause separates flashings and long ones error
codes, longer flash followed by two
short ones indicate DTC 12
(sketched), write down read codes,
turn ignition OFF and remove
jumper.
 Deleting codes: turn ignition
OFF, bridge connector terminals 1
 23
and 2, press the brake pedal and
hold it pressed, turn ignition O,
hold the brake pedal pressed until
ABS light goes out and than release it, wait until MIL turns on
again, press the brake pedal and
hold it down, wait until light goes
out and release the brake pedal,
wait five seconds, the MIL flashes
twice and errors are deleted, remove jumper.
 If we move to the next option
Trouble Code Identification and
look up the definition of code 12
which we read, it is immediately
noticeable that this error is easily
solvable. The code definition indicates a short circuit in ABS sensor
of the front right wheel. With such
clear definition, most will immediately proceed with sensors
replacement, and the
problem is solved. But
those little pedantic, will
make a sensor test before
replacement. amely, as
already mentioned, we
should never fully rely on
the codes definitions to
make final diagnosis,
which may be wrong and
expose the customer to unnecessary costs as well as bring us in an
uncomfortable situation. In this
case, rather than having problem
with the sensor, there may be a
problem in wiring or sensor’s connector which is short connected for
a number of possible reasons.
That’s why precautionary checks
have to be always made, especially
if we have access to data as we
have in this database. On the attached sketches we see
the option of checking
the ABS system elements, or in this case the
sensor. The sensor resistance whose value on this
vehicle is between 750
and 1050 ohms can be
measured on the module
connector terminals,
connecting the instrument to the marked terminals. However, such checks do
not exclude a potential problem of
short-circuit on sensor connector
or its wiring. Therefore it is advisable to measure the resistance at
the terminals of the sensor located
on the wheel hub. Only if we found
no resistance on the sensor termi-
24
nals, we can conclude that there is
a short circuit inside the sensor
and replace it.
 Resetting service intervals without
the use of devices
 Beside the possibility to perform
diagnostic operations on hundreds
car models without the use of diagnostic devices, by using these databases we can also reset service intervals on most of them. Here is
shown example on BMW 3 Series
(E36) 1.6 316i year 2000. After selecting a vehicle’s brand and
model we choose the option Service
Indicator or a similar topic on different types of
cars. On the left
side of the page,
diagnostic connector drawing is
v i s i b l e w i t h
marked terminals.
Above the drawing, menu offers
options to reset
the oil service
warning light, inspection service
warning light or all service warning lights in the package. So, let’s
select this reset in package by
clicking the last
option and follow
the instructions:
switch ignition
O, connect a test
lamp between terminal 7 and the
ground (ground is
anywhere on the
metal part of the
body or engine),
after 12 seconds
five green LEDs
will illuminate on instrument
panel, turn ignition OFF, wait
twenty seconds, switch ignition
O, reconnect the test lamp to terminal 7 and ground, after 12 seconds all five green LEDs on the
instrument panel will illuminate
again, turn ignition off and reset is
complete.
 Ability to access data stored in
the modules or computers memory
as described enables us to engage
in repair and to deal with problems on hundreds of car models
 25
without the a number of expensive
diagnostic equipment. These options should not be ignored even
when it comes to cars for which we
suspect not to be able to handle
tests without a diagnostic device,
but there are always surprises
even when we least expect them.
Therefore, always check if there is
a possibility to do diagnostic or
reset service intervals without the
use of scanning devices.
 OBD I
 Diagnosing failure with diagnostic device
 In this chapter, let's start with
instructions and examples using
OBD I diagnostic devices and related software. As it has been already mentioned in the book Automobile electronics & 4-stroke engine, OBD diagnostic system is divided on OBD I and OBD II. Repeating already read text, in most
cases it is very useful. Therefore,
let's say one more time that OBD
On Board
Diagnostic
means that
engine and
other system comp u t e r s
have the
ability to
d i a g n o s e
faults of
electronic
m a n a g e -
ment of the
entire car by them self. Of course,
every computer or module does it
for certain system. It also means
that the engine, ABS, SRS, AC and
other systems have a separate
module which is often called the
Electronic Control Module ECM
and control particular system on
vehicle. Although the modules or
computers are separated and responsible for managing the system
and diagnosing faults in their system, they can be connected if they
interact. For instance, the ECU
Engine control unit in newer cars
is associated with the ABS module.
The interaction of these two modules is necessary on vehicles with
embedded ESC Electronic Stability
Control system. ESC as a separate
system has installed own software
in its ECM. However, ESC can not
control the vehicle stability if it
does not use the ABS system.
Therefore, ESC module is associated with ABS module. However,
vehicle’s stability is not controlled
only by ABS, but if necessary, engine power is reduced in critical
26
situations, and therefore ESC
module is associated with the ECU
too.
 In older cars models, the modules are not interacting, and they
are separate and independent of
each other. For this reason, sometimes we need specific diagnostic
devices to access data stored in
each device module. It is not uncommon, that each module has a
separate connector for specific
scanner. Such an example, we had
a chance to see on the Honda Civic
when we had performed a diagnostic test without the use of diagnostic device. To access the engine
data we used DLC Data link connector, or connector for accessing
data which is located on the left
below the instrument panel, and
for SRS data access we used the
second connector located behind
the handbrake lever. Thus, these
are two completely separate and
independent systems. Because of
the impracticality of such separately located and different DLCs
or connectors, over the time, car
manufacturers increasingly practiced installing multi-pin connectors through which accessing data
from different ECMs becomes
much easier. However, regardless
of the joint connector, not all scanners can read data from all modules. If we had the scanner which
reads the engine module, the same
could not read ABS or SRS module. Complete reading could do
just more expensive and complicated devices with installed software for each system and built-in
protocols. Under the protocols, we
understand the wire or terminal
connections between the scanner
and DLC or diagnostic connectors.
 To have the clear picture of protocols, it is necessary to know the
following. Each module has a Kline trough which information are
collected and the L-line which
stimulates the module. Therefore,
if we have a diagnostic device,
more known as a scanner, with Kline to access data from the engine
module, the same is not able to get
data from the ABS module, even if
we have installed program to read
data from ABS module. So, to
have a scanner which could read
the data from multiple modules in
the vehicle, we need to have programs for reading these modules
and scanner’s K-line associated
with the K-lines in all modules
trough the DLC. This kind of diagnostic devices, or scanners, complexity, which can perform multiple functions have much higher
price than those provided for reading data from only one module in
particular vehicle. Even these
more complex scanners do not
cover all vehicles, but one or two
groups or car models. Since the
protocols are not standardized,
nor the programs, it is extremely
difficult to produce a device that
would cover all types of cars and
all the modules installed in them.
Knowing that almost nothing is
impossible, and the production of
such a device is possible, but the
issue is cost. Manufacturers of diagnostic equipment came to a sim-
 27
ple conclusion. Larger services are
often specialized for particular
brand or group of car manufacturers. Such services are mostly specialized in vehicle group: VAG,
Fiat-Lancia-Alfa, Rover-Jaguar,
Mercedes-BMW, etc. Therefore,
we can find on the market highly
complex diagnostic devices covering a particular group of cars at
reasonable prices. Smaller services
due to the lack of work are doing
all types of cars and would not be
able to pay such a high price for
universal diagnostic device which
would cover everything. That is
why such services are generally
equipped with limited purpose
universal devices and additionally
purchasing other scanners for a
particular brand or group of vehicles.
 K and L diagnostics lines
 In car diagnostics Kline is the
single core
wire for data
transmission
in both directions and
has a standard labels
ISO 9141
and ISO
14230-1. In combination with Lline, in car diagnostics K-Line has
a capacity for information to flow
in both directions, collecting and
sending information in the same
time. In accordance with the standards, L-line has only a function of
ECM stimulation. Stimulation or
initialization (start / impulse) with
separate L-line is usually used on
older devices, while the newer
scanners solve initialization via Kline. Property of two-way communication via K-line with a single
wire can not function simultaneously. Only after the data is transferred in one direction, it is possible to transfer data to another.
 The attached sketch shows the
schematic diagram connecting the
diagnostic device with the ECU in
two ways. The first ECU is connected only with the K-line which
initializes the diagnostic procedure
by sending data of the diagnostic
device, and then collects and sends
data. Second ECU is connected
with the L-line to initialize and the
K-line to collect and send data. Because of clarity, this is a simplified
sketch without the power and
ground connections.
 As shown, connection has been
done only with the K-line of ECU
or engine computer, and only the
engine data will be available. Complex diagnostic device connection
28
(protocols) with multi-pin diagnostic connector can be seen on the
following sketch. Here is shown
diagnostic connector of Opel car
model. In the first case the vehicle
is manufactured between 1988.
and 1996. for U.S. market. On the
models made for the European
market, these kinds of connectors
we will meet until the year 2001.
The terminals on the connector are
labelled alphabetically, and the
following table shows what is connected to each terminal. Thus, terminal A is the ground, F is the
power supply terminal for interface (or scanner) connected to a
PC or laptop. The use of different
terms for the diagnostic devices is
done on purpose, because we shell
meet such different terms gong
trough the various literature and
programs, what could be confusing
if we do not know what it is. As
already said on several occasions,
none of these scanners is diagnostic device, because ECM does diagnostics it self. We only have access
to information from the ECM by
the specified devices and programs
which allow us communication between the ECM and a home computer. Definition of interface: a
program that allows us communication between the two, for example, devices. Under the letter G we
see the K-line connected with automatic transmission, engine and
ABS module’s K-line from which
we can obtain all data, while other
terminals are provided for other
modules.
 In the next case, we see far more
complex OBD II
diagnostic connector with terminals
labelled by numbers from 1 to
n u m b e r 1 6
( s t a n d a r d i z e d
number of terminals on the OBD
II connector). In
the table that follows we can see
what is connected to the OBD II
connector terminals. Power supply
for interface on the terminal 16
and ground on terminal 4 is standard on all OBD II connectors,
while connections on other connector terminals vary depending of
vehicle model (protocols). This second table significantly clarifies
previous text associated with the
 29
K-line. At Terminal 2 we see the
ABS ECM's K-line, and at the terminal 3 common K-line which is
associated with the modules of radio, automatic gearbox, immobilizer, steering wheel and other additional components which can be
incorporated into the vehicle. Furthermore we see specifically derived K-line for complex diagnostic procedure of ABS, automatic
transmission, SRS, etc.
 If we try to diagnose this vehicle
with an OBD II scanner for engine
diagnostics only, we will access
data from the engine module via
the CA protocol at 14th terminal.
As we can see, to read the data
from other modules, we have to
have an interface which will connect with the K-line of these modules. Other words, to read data
from other modules, interface has
to be connected to the K-line of
each module and than we can have
data access with appropriate programs. But if we work only on
OPEL cars, we can certainly afford a multi-function scanner
which will have
the software installed to read all
the modules and
interface adapted
for the initialization of each module, along with the
multiprotocol connector or connector that connects
all K-lines terminals with the interface.
 KL diagnostics
 As function of K and L lines has
been explained, we can proceed
with the diagnosis using the KL
interface. This type of diagnosis is
applicable on cars manufactured
before 2005th when diagnostics is
switched to newer, faster protocols. Protocols which standardize
and support the KL diagnosis are
ISO9141 and ISO14230. This second protocol is also known as
KWP2000.
 In order to begin the process of
diagnosis, we need a KL interface
which is usually connected to a
computer via a 9-pin serial port
which is the most reliable data
transmitter. The same interface
can be also found with a USB port
30
connection. However, with USB
connection some problem may occur during diagnostic procedure
with KL interface, because the
programs that we are using are
mainly the older generation and
are designed to work over the serial port.
 Beside the interface, we need
programs to read data. If we buy a
factory made interface, drivers are
usually found in the package
which enable interface to operate
in Windows, and at least one diagnostic program for certain group
of vehicles, most often VAG cars.
Since the KL diagnostics can diagnose a whole range of cars, we
shell require programs for other
vehicles too. Beside the possibility
to purchase commercial software,
we can download a number of
them over the Internet as freeware. If we do not have the name
of the program that we are looking
for through the Internet, or Web
address from which we can
download, this key words may
help: KL diagnostic freeware, KL
Opel diagnostic freeware, OBD
freeware …
 In the interface shown in transparent plastic, we can see an electronic circuit which enables secure
communication between the ECM
and computer. On the other side of
the cable we see the 9-pin connector which has to be plugged into
the computer's serial port. When
the interface is connected to the
computer, we get notification in
new window that new hardware
has been found and request to install it. After we select Yes, it is
necessary to insert supplied CD
with drivers. Finally we select the
option automatic installation and
the interface is ready for use.
 As seen on photo, this KL interface has OBD II connector and it
can not be used on cars with OBD
I diagnostic system. Suppose that
in this case we perform diagnostics
on VAG vehicle. We know that the
OBD II diagnostic system on cars
with gasoline engines is found only
in those made since 2001. and very
rarely on some earlier models.
However, it is not uncommon on
older models to find the OBD II
connector, but OBD I diagnostic
system. Therefore, this scanner is
sold with OBD II connector which
is most commonly installed in vehi-
 31
cles. But what to do with the older
types of cars for which this scanner is provided?
 On the above drawing we see
how the VAG older diagnostic connector, located under the bonnet,
looks like. First rectangular connector has two terminals K and Lline, and second one 12V and
ground terminals for interface
power supply. Knowing which terminals on the OBD II connector
are K and L lines and which are
power supply, we can make adaptor with four wires. However, such
connection is quite risky as we can
easily cause short circuit and have
unwanted consequences. Therefore, it is advisable to buy factory
made adapter. Such adapter is
plugged into the OBD II connector
and its other side to the rectangular connectors on the vehicle. With
this adopter cable we connected
power supply and K and L lines
from vehicle to the designated terminals on the OBD II connector.
 The sketches show mentioned
terminals on the OBD II connector
and on the VAG vehicle diagnostic
connectors. It is quite clear now, if
we do not have the adapter cable
for a particular vehicle, we can always make a connection with the
wires. As we saw in previous articles, each vehicle has a different
arrangement of terminals, i.e. K
and L lines and power supply, if is
not the case of OBD II connector
on the vehicle. In other words, it
would be advisable to obtain
original adapter cables for all
types of vehicles or just for the
common ones. However, if we have
to make wire connections, then we
have to obtain a diagram of the
vehicle’s diagnostic connector.
Such diagram will be very similar
to this with VAG's marked terminals. The sketched OBD II connector terminals are standardized and
can be easily remembered, but the
terminal markings of older cars
connectors should be obtained.
Again, one of the easiest ways to
find needed diagrams is the Internet. Typing the term i.e. OPEL
pinout will certainly result with a
number of sketches with marked
terminals.
 In this case we had a situation
where all the information was obtained trough the only one K-line.
In previous sketches we have seen
that some diagnostic connectors
have several K-lines. These connectors we will find on Fiat, Opel,
Mercedes and some other models.
This means that we have to connect K-line, if necessary, and Lline if marked, with the K-line ter-
32
minal on the ECM with
whom we interact. Thus, to
test the engine we shall
connect to engine’s module
K-line, ABS to the ABS’s
module K-line etc. Power
supply we can connect to
the diagnostic connector
marked terminals, or directly on the positive and
negative battery terminals.
 As we see, on the VAG cars is
really not so complicated to connect terminals with wires, as is the
also case with Fiat and Alfa cars.
But, if we have to do such wiring
on BMW, Mercedes or some other
car models, a matter considerably
changes due to the multi-pin connectors. Of course, adapter cables
are available for all these vehicles
as well as universal OBD II
adapter cable with four banana
connectors (K and L lines, 12V
and Ground) together with socalled Pinout Box.
 Let’s make one example with
an Opel vehicle manufactured
1998th with the OBD I diagnostic
system and OBD II connector. If
we do not have interface for Opel
automobiles, standard terminals
on OBD II connector will be: 16
 33
Power, 15 L-line, 7 K-Line and 4
Ground. Such a protocol will suit
VAG vehicles which have the same
terminals arrangement on OBD II
connector. This protocol will also
suit Opel cars, but only for accessing data from engine module. ABS,
SRS and AC module’s K-line will
be at the terminal 12, while for
gearbox and central locking we
shall use 3rd terminal. It means if
we want to read data from other
modules, we have to connect interface’s K-line with their K-lines on
the vehicle’s OBD II connector. It
is quite obvious that wire connection in this case is more than inconvenient and awkward. If we
use now OBD II adapter with four
banana connectors (Red +, Black-,
K-Line Blue and L-line Yellow)
and Pinout Box (Ground at 4th and
5
th terminals marked in black and
the power on 16th marked in red),
whole process becomes simple. By
plugging OBD II adapter into the
OBD II connector on the interfaces
we shall get four banana connectors (12V, Ground, K-Line and Lline). OBD II connector from Pinout Box has to be plugged into the
vehicles OBD II diagnostic connector on the vehicle and we have got
all 16 terminals accessible from
OBD II diagnostic connectors.
Positive and negative banana connectors have to be plugged into the
Pinaut Box holes labelled with
number 16 and 4. Remaining two
bananas we shall plug in holes of K
and L lines of the chosen module
from the diagram which we previously obtained for particular vehicle. Thus, in the case of our Opel,
if we want to test the ABS, we shall
see on diagram that the ABS Kline is at the 12th terminal. If we
have previously obtained an appropriate program for Opel cars,
with ignition O, testing can begin. Throughout this process has
remained untold a trifle to which
we will look at during the OBD
program installation, coordination
of communication ports in the program we work with.
 Installing KL interface and software
 How to install program and interface? Suppose we have just
bought the interface and programs
on CD. In most such cases people
ask for assistance from someone
skilled to install the program
(Software) and device (Hardware).
Therefore, let’s pass this procedure step by step. With purchased
Interface, beside the drivers for
interface installation, we will usually find i.e. VWTOOL program.
Insert the CD in the laptop or PC
and wait while menu shows up and
select the option Open folder. In
34
case that mentioned menu does not
open after inserting the CD into
the computer, the procedure is as
follows. Look on the desktop for
My Computer icon. Double click
on the icon, and new window will
open displaying all computer’s
disk drives: C, D, E. .. Select CD or
DVD drive, clicking twice on it
content of the CD will show.
 One way or the other we have
opened the CD and found the first
folder K+CA. The folder’s name
itself indicates that we are going to
install quality program which supports the KL diagnostics or OBD I
and OBD II diagnostics with latest
CA protocol. Clicking twice on
that folder, new one opens. In the
new folder, among other things, we
see the program folder VWTOOL.
Double click on that VWTOOL
folder and new one will show
again. With double click on this
last folder we are opening its content and finding Setup option.
Double click on Setup and program installation is activated. If
we have an antivirus program installed, it will stop installation and
warn us about unidentified program and ask permission to continue with installation. Permit continuation with Yes and program
installation begins. During the installation program asks specific
questions for which we must provide answers. The first question we
meet is whether the program may be installed
at the proposed location
of the disk C. If not, you
we have to enter the location, but in practice
programs are always
installed on the C drive.
By clicking Continue,
the program continues
with the installation.
Oops! Problem. The
installation has started
and stopped. ew window appears with mes-
 35
sage that certain components of the program can not be installed. Another two
or three attempts
were unsuccessful.
What is it? Antivirus
protection allowed
installation but it
failed.. The only conclusion is as follows.
Here was made attempt to install program on a laptop
with Windows Vista.
Since this is an older
program, it is probably not foreseen for
Vista, what is not uncommon for older
generation programs.
The only solution that
remains is the attempt to install program on another
computer with Windows XP. So let's try.
 We went to another
computer and repeated previous procedure. Assumptions
were obviously justified. On Windows
XP, the program was
properly installed.
The red installation
line which has
stopped in an earlier
attempt to install the
program on Windows
Vista passed without
stopping from the left
to the right side and
36
completed program installation.
Before finalizing program installation new window appears where
we have to define interface communication port. The older programs offer very limited
number of ports, very often from 1 to 4. At that
time when such a programs were used, more
ports were not needed
because the 9-pin serial
port 1 was mostly used
and automatically suggested. However, with
this modified K+CA
interface, which we have
just bought, connection is
foreseen via the USB
port. Knowing that the
COM 1 is serial port and
COM 2 parallel typically
used for printers, we shall
choose the port 3 or 4. In
our case we have selected
the last port 4, for pure
precaution if port 3 has
been accidently occupied
for some reason. After
selecting the port,
through which the diagnostic program will communicate with the engine’s ECM, or any
other, a new window appears with the sentence:
VWTOOL installation is
completed.
 During installation, we
are often offered to create
a program icon on the
desktop. Seeing that this
option was not available
during installation, we have to create it our self. To do that, we have
to click on Start in the lower left
corner of the monitor and click on
Programs. In the programs menu
 37
we look for installed VWTOOL.
As we go over the program title
with mouse, we shall notice program icon on the right
side. In the right side column, right click on the
program icon and choose
Send To and Desktop
(create short cut).
 Program is successfully
installed, communication
port is defined, and we
only need the interface to
make connection with the
vehicle. So, let's start with
the interface installation,
and prepare our computer
for communication with
vehicle’s modules.
 Connect the interface
via the USB port to the
computer. Shortly after
plugging scanner to the
computer, new window
appears with the message
Found 2ew Hardware. Automatic
installation and Hardware Wizard
will guide us trough the installa-
38
tion process. To find the right
track in finding programs and
drivers to install the interface,
Wizard raises three questions.
First: can windows connect to
Internet to search for
software? Second: Do
you want to connect to
the Internet each time
you connect the device?
Third (suggestion): ot
this time. In our case we
choose the third option
because we have the installation program. If
we, for any reason, removed the CD from the
c o m p u t e r w i t h
VWTOOL Setup and
drivers for interface installation, insert it back
into the computer's CD
drive. The next window
that appeared after we
selected the third option
on the previous window
and clicked on 2ext, offers us the option with
automatic installation
and manual where we
have to specify the location of the installation
program. Here we
choose automatic installation, in which case the
Wizard finds the drivers
on the inserted CD. By
clicking on 2ext after
selecting the first option,
we see how the Wizard
scans our computer for
installation program.
After finding the program, data transfer follows from
CD to the computer. Completion
of green line stream in the next
window indicates the end of data
transfer. Finally we click on Finish
 39
in the next window and
the interface installation
is successfully completed.
However, to make sure
that we have connected
chosen USB port with a
diagnostic program, we
have to make the following checks. In the lower
left corner of the monitor
click on Start. In the
open menu, select Settings that leads us to the
Control Panel with programs which control
computer operations.
Find the System icon,
open the Hardware and
then the Device Manager.
In the computer components menu, click the +
mark in front of the
Ports (COM & LPT). In
addition to the physical
ports (COM 1) and
(COM 2), we see a whole
series of virtual ports
which are installed when
we installed the interface. These ports are
usually marked with the
acronym USB, but here
we see them labelled as
Bluetooth ports. The reason is pre-installed wireless OBD II scanner
which works over the
Bluetooth. If we find on
this list the number of
USB or Bluetooth port
(COM 4) which we have
previously defined in the
program, the installation
40
was completely successful and the
program will be linked with the
interface and the vehicle through
the existing fourth port. But if we
do not find a port number, which
we defined in the program, diagnostics will not work because the
program can not find defined communication port for connection
with interface. In this case, the
procedure is as follows. From the
ports list choose one port (9, 12,
16 ..) and right-click on the one of
them. When new window opens
select the Port Settings option. By
clicking Advanced, new window
opens where port number can be
changed. In the option COM Port
2umber simply overwrite the existing number with number 4
and click OK. Check the
ports list again to see if
(COM 4) is listed. If the
whole procedure is properly done, the program is
installed and communication between the programs
and interface is harmonized and diagnostics is
ready for use.
 Just like when any job is done,
we can not wait to see the effect of
what we did. So let's check it. With
this type of interface and K+CA
program, diagnostics can be performed on all types of VAG cars
(VW, Audi, Skoda, Seat) combining older models made until 2001st
for which we are suppose to use
KL diagnostics, and models made
since 2001st for which we use OBD
II diagnostics. As known,
Interface has to be connected to the vehicle diagnostic connector and ignition switched O2. On the
computer, double click
the program icon, and diagnostic process begins.
In the open program’s
menu we can immediately
notice complexity of the
program by offered scan
options. The upper main
menu gives us the possibility to
scan ECMs of: engine, transmission, ABS and SRS, thus the four
most important automobile systems. Additional menu provides us
with expanded possibilities to scan
other vehicle systems: clutch, adjustable suspension, anti-skid sys-
 41
tems, anti-theft system, sunroof,
central locking, instrument panel,
air conditioning and heating, electric seat adjustment and a high
pressure pump on diesel engines.
But that's not all. When we click
on the More Modules, scanning is
expanded to additional modules:
the car level control, the monitor
in the vehicle, the range of the
headlights, setting the position of
the steering wheel, a module that
manages all incorporated devices
in the vehicle (Central Convenience), or better known as accessories: radio, rear view mirrors,
parking system and additional
heaters.
 One should be aware of the
fact that the diagnostic programs are sometimes very
complex, although they simpler programs should not be
taken as simple ones. If we
would clarify in detail all the
functions of individual programs and their capabilities,
as well as issues related to
read errors, it would certainly take a several thousands pages. This book should provide even more than just fundamentals of diagnostics, but by no
means a complete knowledge
which is gained by experience and
constantly updating knowledge.
Therefore, before using a particular diagnostic program, it must be
well studied as well as all available
literature about it.
 Proceeding to use VWTOOL
program, we will refer only to the
few functions of this program
which are very similar to the programs of other vehicles. With this
introduction, and assuming that
we have mastered previous book
Automobile electronics & 4-
stroke engines, we will certainly be able to deal with
the problems of diagnosing
faults and eliminating them.
 So, this program in the
main menu offers the choice
of scanning individual modules of vehicle’s electronic
management. Selecting by
mouse click, in this case the
engine, we get detailed information about the engine
42
module (on the above sketch we
have selected accessory module or
Central Convenience. In common
practice, we usually go first
to read the DTCs by clicking on this option. If the
program has installed
DTCs definitions, it will display them along with the
DTC number. If definitions
are not installed, we will
have to search for them in
the Workshop Manual or in
databases programs. The third option is the Internet. In this last case
we should look for DTC definition
for particular car make, if it is not
a generic code (P0...) whose
definition is valid for all
types of vehicles. Factory
codes can have the same
number for multiple types
of vehicles, but the definition is different. Presented
codes on photo can be confusing because each code is
displayed by one number
and than by other in brackets. The first number is the
internal manufacturer’s or
VAG's number. The second is also
manufacturer’s number as begins
with the P1... but is harmonized
with OBD II standard codes identification. Thus, it is a same DTC
marked in two different ways.
 Very practical option is the actuator test. Selecting this
option program will give
command to the module of
the system which we are
scanning to drive the actuators. In the sketch we have
shown the process of testing
the EGR valve. By clicking
on the 2ext Output we proceed with the next actuator
test. This option can test the
solenoid valves, throttle idlemotor, ABS actuators, open
 43
and close the sunroof, electric windows, etc.
 Let’s go back one more time to
the ports synchronization. When
we installed this modified interface
that covers OBD I and OBD II diagnostic system, we had connection with a computer via a USB
port. However, how we can see on
the first photo of the interface
coated with transparent insulator,
KL interfaces have only 9-pin connector for connection to the serial
port on the computer or communications port (COM1). Therefore,
in the program provided for diagnostics with KL interface, we are
offered by default (COM 1) as
communication port. Thus, by
plugging in the interface with 9-
pin connector to the serial port, we
only have to check the port settings in the program. If a COM 1
port is already highlighted by default, communication synchronization is solved.
 Beside a number of programs for
the KL diagnostics which are designed to work on certain brands
of cars, it is worth mentioning a
very complex program for the diagnostics of all European cars,
which beside the engine also covers
ABS, SRS, and resets service interval on the most listed car models.
This program is known as Uniscan, Euroscan or Visa 1.83. The
only disadvantage of this program
and interface is that it can not be
used with newer computers. However, it is not surprising considering that this is a relatively old diagnostic configuration designed
for installation on computers of
that time, as on Windows not
newer than Widows 98. In addition
to the older Windows such as Win
95 and Win 98, a computer has to
have installed the DOS program
through which this diagnostic
works. Problem does not lie only in
Windows and DOS, but in the computer too. This interface is connected to the computer via two 9-
pin serial ports which can be
found only on older PCs (486 and
Pentium 1) and even more rare on
older types of laptops. Therefore,
if we have this very useful diagnostic tool with which we can do a lot
of work, from diagnosis to testing
actuators on hundreds car models
of European production until the
year 2000, it is necessary to obtain
an older computer just for this
purpose. However, even an extra
computer won’t be a great expense, because if we find today
such a computer its price will be a
bargain, which is another reason
for having this diagnostic tool. So,
we need an older computer with
Windows 95 or Win 98 with installed DOS which is usually installed on such computers by default. In addition, such a computer
must have two serial ports, which
are marked in Device Manager as
Communications Ports (COM 1
and COM 2).
 On the following photos just
some functions of this diagnostic
program are shown indicating its
broad application. In the first
menu we choose car manufacturer.
The following indicates the vehicle
44
model and engine type. After selecting a brand and type of car, we
have presented model of ECU installed in the vehicle and its position in the vehicle, as well as location of diagnostic connector. Finally, we have to confirm selected
vehicle.
 Unlike other diagnostic programs and interfaces, Uniscan is
very slow and sometimes gives the
impression that program does not
work. But with a little patience,
this ancient program, by today's terms, will do very well
determined functions on its
pensioner’s mode.
 After establishing communication with the engine
module, menu with diagnostics options is offered: accessing DTCs codes, parameters, actuators testing, information, ECU program identification and exit. Let’s choose the
option for testing engine’s actuators. This option gives us the opportunity to test: injectors,
EVAP valve and engine
idling electric motor. These
options will save us a good
deal of time that would be
otherwise spent to verify the
values by ohm or volt meter.
When checking injectors, the
program will give the command to the engine module
to activate each injector and
thus verify its correctness and
power supply. But there will be
still some work left for us if we
have a problem with the injectors.
amely, this test will not
determine the insufficient
flow of fuel through the injector, which may be reduced due to accumulation
of carbon deposits on the
injectors. Therefore, if test
determines that injectors
are properly functioning
and we still suspect the improper fuel dosage, it will be
 45
necessary to clean the injectors.
However, in case of one injector
malfunctioning, this test will be
very useful, indicating exactly in
which injector problem lies.
 Fast testing of EVAP valve will
also save us a great deal of time
knowing that this valve is
sometimes quite inaccessible for physical inspection.
And in this case will be
some work left for us if we
have problem with EVAP
system. But knowing that
solenoid valve is in order,
we can focus on hoses
leakage and the fuel tank
cap. Again we are back to
work and knowledge. We see how
the diagnostic tools are of invaluable help, but only in terms of
pointing to the area of existing
problems, when we usually have to
use all our knowledge and
quite some time of physical work to solve the existing problem.
 When testing the engine
idle speed controller, the
engine module will give
command to turn the electric motor several times
and thus determining its
correctness or incorrectness. As in other cases,
this step-motor may be functioning
correctly, but we still doubt in its
proper functioning.
Knowing how the air enters into the engine trough
the separate channel or
passage regulated by stepmotor, we can suspect a
build up of dirt in the
channel and on the valve,
as well as on the throttle
butterfly which therefore
does not close completely
and disturbs the proper
air proportions entry.
46
 At the end of this KL diagnosis
chapter, here are a few examples
and schematic presentation of diagnostic connectors with marked
power supply and K and L-lines.
 The first sketch of the Alfa Romeo vehicle has labelled connectors: C terminal for K-line, A terminal for L-line, B terminal for
ground and terminal B+ 12V
power supply which does not exist
on the connector. As already mentioned, the power supply for interface can
be obt a i n e d
directly
f r o m
battery.
So, the
F i a t -
A l f a -
L a n c i a
cars have
o n l y
three term i n a l s
while the
p o w e r
s u p p l y
connects
directly
to the battery. The original
diagnostics cable will have
a connector with three terminals and specially derived red alligator clip for
connection with the battery
positive terminal or any
other positive terminal on
the engine or car body.
 47
48
 OBD II
 Through the previous text we
have seen how difficult is, or
rather complicated, to be able to
deal with all types of cars and
thereby maintain a high quality of
diagnosing failures. Dozens of protocols, various terminals, scanners,
software and other literature, is
essential for such an operation.
ot to mention the amount of
knowledge and experience.
 Such a complex diagnostics system was most suited for car manufacturers. Due to lack of hardware
and software, or how we say, diagnostic devices, programs and literature, the authorized services
have had a monopoly in terms of
maintaining and repairing cars.
The law that was put into effect in
America in 1996th related to ecology forced the manufacturers to
standardize protocols and diagnostic connectors. By standardizing
the access to data from the ECU,
almost all small repair shops were
able to access data with relatively
inexpensive scanners. Easy access
to engine module enabled quickly
diagnose and fault repair. We
would say in the jargon, where is
the catch? Malfunction of any electronic management element will
result in increased emissions of
harmful gases. Knowing that in
most cases we can continue to ride
and when Check Engine light illuminates, we can imagine how
much time will elapse until owner
of the vehicle visits authorized service and then waits for another
date of appointment, polluting
meanwhile. This was the reason to
come up with the law to standardize connectors and protocols in order to enable any repair shop to
deal with problems on engine electronics management.
 Thus, in 1996th a standardized
OBD II diagnostic system went
from USA. The standardized 16-
pin connector had to be incorporated into all types of passenger
cars and light trucks. The terminals on the connectors were also
standardized. The first step has
already been made by the interfaces having only one type of connector for all types of cars, where
all terminals were connected in the
same order as follows: First terminal is reserved for factory line data
availability which are not related
to ecology, and for this reason
should not be available to everyone. On the terminal two, we shall
connect with the interface that has
 49
access to module data with the
J1850 bus protocol. The third terminal is empty, and reserved for
manufacturers as well as the first
terminal. The fourth terminal is
ground for interface power supply
and the fifth terminal is minus
pole for signal transfer. The sixth
terminal has access to high CA
data protocol and the seventh terminal to ISO9141-2 K-line. Terminals eight and ninth have the same
purpose as terminals 1 and 3.
Trough the 10th terminals we have
access to the J1850 data bus protocol, while the terminals 11 and 12
are again free for the vehicle
manufacturer. On the terminal 13
we will find again minus pole for
signal transfer and at terminal 14
CA Low. Terminal 15 allows us
to access data by the protocol
ISO9141-2-L line. That is, terminals 15 and 7 we use to connect
with the K and L lines, as previously explained. Finally, the terminal 16 is the 12V power supply for
interface.
 Even with standardized terminals, there is still a problem with
protocols. amely, after the introduction of OBD-II diagnostic system, the market was supplied with
various scanners at acceptable
prices. Labels on them marked the
protocols through which they communicated with the engine ECM
or ECU. For example, if we have
obtained the interface with VPW
protocol that has a standard connection: 2 Data, 5 Ground and 16
Power, we could not establish communication with the engine module which has worked over the ISO
and KWP protocol that has the
flow of data through terminals 7
or in combination with a terminal
15 (K and L lines) and power supply via 16th terminal. So, these two
protocols have only in common
Ground and Power, while access to
data is on different terminals.
Thus, initially it was necessary to
know which protocol has to be
used for particular vehicle and
then use the scanner with the appropriate protocol. Here are some
protocols for certain vehicles: Alfa
Romeo, BMW, Honda, Jaguar,
Toyota, VW ... will work through
the ISO protocol. But VW made
for the American market, will
work through the PWM protocol
as well as some Volvo cars made
for the Swedish market. Ford Fiesta for the Italian market will
work through the PWM protocol
and the Ford Mondeo for the Austrian market through the VPW
protocol. As we see, quite colourful. Such, shall we say, confusing
situation with protocols lasted until 2008th when new and fast standardized CA bus protocol
started to be used on all types of
vehicles.
 Protocols for particular vehicles
can be found in workshop manuals, but also can be recognized by
existing terminals on connector.
For example, VPW protocol can
be identified by protocol defined
contacts terminals embedded in
connector, while others will be
empty. Certainly, we should not be
confused if some other contact ter-
50
minal is embedded too, providing
access to other data. In other
words, if we do not know the protocol by which we can communicate with the module, we can recognize it by active diagnostic terminals on the connector.
 Until now we mentioned terminals connections for three existing
protocols and here are terminal
connection lines for other two.
PWM protocol has a data access
via terminals 2 and 10 and Ground
and power supply terminals are
the same as for other protocols, 4
and 16. CA protocol will use terminals 6 and 14 to access data, 5
and 16 for the interface power
supply.
 As we can see, neither the OBD
II diagnostic system is quite that
simple as the opinion prevails
among the car service personnel.
To overcome this obviously confusing situation about protocols,
which are usually less well-known
in the circle of vehicles servicing
personnel, diagnostic equipment
manufacturers have begun producing Multi-protocol scanners.
Such scanners are connected to the
all protocol terminals on connector
and have an electronic circuit
which detects the vehicle’s protocol. By connecting such an interface to the vehicle, an electronic
circuit in the interface connects all
protocols by order. At the moment
when interface establishes communication with the module, the protocol is defined and communication between module and program
is established.
 By establishing connection
through the one of protocols, we
will be able to read data only from
the engine module, and all those
data that go through it. For obtaining data from other modules,
we will have to use an interface
and program for the particular
vehicle which has connected data
terminals for accessing other modules. So, if we want to test the ABS,
or SRS, we will require such a
scanner and the reasons we have
already explained. On presented
drawing is clearly visible where in
addition to the standard terminals
are others terminals connected
with different modules. Certainly,
today we shall meet more complex
diagnostic devices with terminals
 51
on connector, or protocols, to
reach data from number of modules beside the ECU, however, the
cost of such devices is very high,
and again, none of these devices
cover all vehicles and all the modules in them. In addition, updating
programs for such scanners, usually over the Internet, cost extra.
 ext to the protocol name, we
noticed the mark Bus. Let’s explain its meaning. The word bus in
the English language means auto
bus or coach. Okay, but what it
has to do with the protocol? Going
back a bit to translate programs
and other literature, we note that
the English phrases used in the
computer world have not any similarity with a literal translation.
Such an example, we had with the
term Freeze Frame. Thus, the term
bus is a picturesque term applied
to data transferred by the bundle
of wires in the electronic management, compared with the full bus
speeding on highway. Simply, the
Bus is the wire line between electronic elements trough which address (required information) of
recipient is sent, and toward whom
required information will be sent.
 CA bus protocol replaces all
previous protocols. In standard
option of OBD II connector we replaced the CA protocol on two
terminals: on 6 CA2 High and
CA2 Low on 14. High Speed CA2
transmits data rate expressed in
Baud rates from 40Kbit/sec to 1
Mbit/sec. Low Speed CA2 transfers data at Baud rates from 40
Kbit/sec to 125 Kbit/sec. Baud rate
is the mark for pulse per second,
or frequency.
 How the CA2 Bus communicates? This protocol uses two
wires. One is called a CA2 High
and other CA2 Low. When the
CA2 Bus is at Sleep Mode, and
there is no information flow, both
wires are powered by 2.5V. During
data transmission, the CA2 High
voltage line increases to 3.75V, and
CA2 Low line voltage falls to
1.25V. At this moment difference
of 2.5V is generated between the
lines, which is in he same time the
signal. Such data transfer is not
subject to possible environment
voltage interference, and therefore
no wires protective net coat is
needed. It is not uncommon for the
sensors and other electronic elements that we see sometimes
wrapped with confusing net shield
whose only one side is connected to
connector while the other side is
free. Such wrapper is called the
Shield which absorbs the external
voltage signals and annuls them by
connecting it to the ground
through the connector.
 The OBD II diagnostic system
we will also meet as: EOBD, JOBD
and ADR. These are versions of
OBD II acronyms that indicate areas where applicable as: European
On Board Diagnostics, Japanese
On Board Diagnostics and Austra-
52
lian OBD Standard.
 Just like with KL diagnostics,
and here we can play with the Pinout Box if we have appropriate
programs. For identification of the
CA bus wires that we need, we
can always look for sketches or
photographs on the Internet or in
other literature.
 And, at the end of this chapter,
let’s explain the meanings of diagnostic protocols acronyms:
 CA Controller Area 2etwork, a
free translation, control of data
transmission networks.
 ISO International Standards Organization, International Organization for Standardization.
 PWM Pulse Width Modulation,
modulation of pulse width.
 VPW Variable Pulse Width, variable pulse width.
 KWP 2000 Keyword protocol, is
one more protocol used by manufacturers of European and Asian
cars, but uses the same terminals
as ISO 9141-2.
 Using the OBD II software and
interface
 In some kind of cheaper version,
we will use the OBD II Multiprotocol interface. This scanner will allow us to access the data from the
engine module on all types of vehicles with built-in OBD II Diagnostic System.
 These scanners we will find on
the market under the name ELM327, which is usually hidden behind the names of manufacturers
such as Scan Tool and others. Depending of the scanner name, the
price will vary. Scanners are available with 9-pin serial connector for
older computers and USB or Bluetooth connection between the
newer computers and interface.
With the interface is usually supplied installation disk with drivers
and at least one diagnostic Freeware program. One of the most
common programs, which are supplied with the interface, is the Scan
Tool 113win. This program does
not offer too many options such as
Freeze Frame, PID, oscilloscope,
etc. but it is very quick and easy to
use. Two offered options for readings in this program are generally
sufficient to solve a series of problems. The first option offers the
readings of the engine sensors parameters, and the second one
reads the trouble codes and deletes
them, as well as it turns the MIL
Off (Malfunction Indicator Lamp)
or a lamp which warns us about
any malfunctions of the electronic
engine management.
 Procuring such a scanner, CD
has to be inserted into the computer to install the diagnostic pro-
 53
gram, in the same manner as previously described. Connecting interface to the computer, we shall
install it as a new hardware using
the CD which is already in the
computer, again in the same way
as we have done it before. In this
procedure we also have to take
care about the ports synchronisations. If we have obtained interface
with 9-pin connector for serial
port, we shall make connection
with interface through the port
COM 1. But if we own a scanner
with a USB connection, we shall
repeat the procedure of synchronising the ports as in the case already described.
 When the program Scan Tool is
installed and opened, the menu
appears with the options offered.
First what we have to do is synchronisation of the communications ports in Options in the main
menu. As this procedure would not
be skipped, when first booting the
program the window appears
warning us that it is not possible to
establish communication with the
interface because the port is not
defined. If we click on Configure
port, it automatically opens the Options. Unlike the previously described installation, here we have
offered eight communication
ports. As said before, in the case of
connection via the serial port, we
choose COM 1, which is already
offered by default. If we are connected via the USB port, after installing the interface we will go
into Device Manager and check if
the USB port is listed with numbers from 3 to 8. If so, let's say we
choose COM 5 port for communications between the interfaces and
program, this port number we will
define in the program too, by
clicking on the circle in front of the
label COM 5. Once we are already
in this option, we can modify units
by clicking the Metric circle. Frequency (baud rates) is not necessary to change because it is generally consistent with the port frequency. But sometimes it can be
synchronized with the frequency
of selected port in the option Port
Properties in Device Manager. Finally click Save and the installation is completed.
 The third possibility of connection between the computer and interface is via Bluetooth. This con-
54
figuration is very practical for
workshops for two reasons. Using
a laptop during the diagnosis is
impractical because most often we
have to sit in the car with a laptop
on our lap or placing it on the passenger seat. In such a cramped
space, only one person has access
to the results displayed on the
monitor. Furthermore, when shifting laptop, there is always a possibility of damaging it, pinning the
cables etc. Bluetooth allows us to
set up a laptop or PC to a fixed position on the bench where we are
comfortably placed and have at
hand a paper, pencil and everything else we need. Separate
monitor will provide insight
into the results displayed on
the monitor to other colleagues also, who usually
comment presented results
in terms of suggesting a diagnosis.
 Installed software on the
PC will communicate with
the vehicle, or interface, via
Bluetooth inserted in the
computer USB port. Interface for wireless communication
has also installed Bluetooth. This
interface attaches to the diagnostic
connector in the vehicle, and the
connection between it and the
computer will be established via
Bluetooth. Diagnostic procedure
with cable connected or Bluetooth
interface is identical, except that in
the second case we have to match
the wireless connection between
the computer and interface.
 When purchasing wireless interface, along with other popular programs, the BlueSoleil Bluetooth
software is supplied too, providing
data transfer. If this program is
not supplied with interface, it can
be installed over the Internet as
freeware. So, let’s go through the
installation and synchronisation of
this program too.
 After installation of the BlueSoleil program in the usual way,
we shall notice a new icon on the
desktop. If the icon does not show
up, we can transfer it from All
Programs in the Start menu, as already described. ew program
opens with double click on the icon
with previously inserted Bluetooth
into the USB port. After the Bluetooth self installation, the program
is ready for use. If we click twice
on the orange ball in the middle of
the window, the program will find
all Bluetooth devices in the
neighbourhood. So, in this presented case a program has found
via Bluetooth two cell phones and
an unidentified device. This device
is our interface. If we have an interface with known manufactur-
 55
er, instead of this sign, we will see
different icon with the name of the
company, for example Scan Tool.
 From the found devices select the
interface to establish communication. To establish connection with
the selected device, we must pair it
with the program. This function will be achieved by right
clicking the mouse button and
highlighting our device. In the
newly opened menu choose Pair
Device option, and click on it.
After pairing device, new window may appear where we have
to enter a password. Password
for this free program is: 1234.
Enter the password and click
OK. If the program did not
automatically choose the communication port icon on the top menu,
simply double click on this icon.
Once the communication port
shows in the yellow square
frame, the communication
should be established. As soon
as the communication is established between the interface
and computer, the red dots
which connect the selected device and computer will start
travelling between the device
icon and the orange center.
The number of red dots in the
column shows the signal strength.
After achieved connection, we can
lower the window by clicking on
the minus (-) in the upper right
corner, and open the diagnostic program. In the case of encountering a problem with the
communication between the
interface and program, the
ports should be checked in the
Device Manager. In this case,
the ports will be marked with
Bluetooth instead of USB, as it
was the case with USB interface. However, the verification
process is identical to the al-
56
ready described. COM port defined in the diagnostic program,
must be listed on the port list in
Device Manager.
 Having passed successfully the
installation procedure of the diagnostic program and interface, we
can start reading sensor parameters and faults or DTCs
(Diagnostic Trouble Codes) in already open Scan Tool program,
which we took as an example.
 In the main menu we can choose
between the options Read Codes or
Sensor Data. In practice, we usually have a problem with illuminated MIL which indicates the
fault in engine electronics. Therefore, let’s first read the codes in
order to eliminate the fault. So, we
have to click on the Read Codes.
 In the presented example we see
three DTCs and the MIL is O.
That means, that scanner has
pulled out from ECU stored trouble codes and information that
Check Engine light is O. By
P0xxx codes marks, we can conclude that a generic codes are
shown, whose definitions are usually stored in the diagnostic program. If we click on the one of displayed codes, its definition will be
shown in the window. In this case,
we see the definition of the selected
code P0234, which says that the
Turbo or Supercharger supplies
engine with too high air pressure.
 Knowing how the Turbo or Supercharger works, we will inspect
the by-pass valve which directs the
exhaust gases to the turbine or
partially to exhaust system. One of
the most common causes is
blocked by-pass valve, what disables redirection of exhaust gases
from the engine, and causes too
high rotation of the charger and
thus the excessive air pressure in
the engine intake manifold. If the by-pass valve
is mechanically in order,
we can suspect that the
problem lies in the control mechanism which
operates the valve. Depending of the make of
vehicle and type of
charger, we will check the
vacuum regulator valve
connected directly to the
charger, or stepper motor
controlled by ECU on the
newer car models.
 If there are more DTCs displayed, it should be considered
that some of them may be causal.
amely, if consequence of mentioned displayed code are: high
engine cooling and oil temperature, then we can suspect that
 57
these codes are caused by malfunction of the turbine or a Supercharger, what usually leads to engine overheating. The DTCs which
occurred as a consequence of the
real problem will no longer appear
after deletion, if the real failure
has been corrected. So, when reading trouble codes, it is more than
important to think about them and
see where the real problem lies
among displayed codes. Of course,
and again, the theoretical
and practical knowledge
is essential for proper diagnosis.
 If we suspect that there
is a malfunction in the engine despite the DTCs
shown, write down their
numbers and remove
them from the ECU by
clicking on Clear. After a
short or long run, we shall
re-engage a diagnostic device and repeat the scan.
If we find the same DTCs registered again, we can say with certainty that some malfunctions exist. After elimination of fault,
DTCs have to be deleted and MIL
lamp turned Off by clicking on
Clear.
 It is not uncommon when reading DTCs, to be in dilemma about
the failure due to illogical sequence
of displayed codes. In such cases,
the Sensor Data option can be of
great help. Exiting the option Read
Codes by clicking on Main Menu
and than on Sensor Data, we shall
be able to read sensor values. Certainly, in this option we shall need
engine running. If we started the
engine by switching ignition Off
and O, there is a possibility that
we have lost communication between the vehicle and computer.
Port status indicator in the upper
part of the program will show us
whether the connection is established. The yellow light will be a
sign of a broken link, while a
green-established. In the case of
broken link we shall click on the
Interface Reset in the upper right
corner and re-establish the connection.
 In this new opened option, we see
in the lower part eight pages from
which we can read a variety of values or data. But let's start from the
first one. The first row shows
throttle butterfly opening, which is
in this case open 14.1% at 798
revolutions per minute RPM. In
the third row we can monitor vehicle speed, if testing is done when
driving. The fourth row Calculated
Load Value, tells us about calculated engine power in percent during a certain number of engine
58
revolutions. In other words, with
the shown engine RPM, the available power and torque is 24.3%.
ECU performs this calculation by
dividing the amount of airflow into
the engine with the maximum possible flow. In diesel engines, this
calculation is performed by dividing the current torque by maximum torque at a given engine
RPM. The fifth row Timing Advance shows us the ignition timing
in degrees at a given engine RPM.
Intake Manifold Pressure tells us
about the air pressure in the engine inlet manifold. Air Flow Rate
tells us the mass of intake air into
the engine. As we see, the measures in this program are expressed
in American or English units. If we
select in Options Metric readout,
measures will be expressed in the
metric system of measures. In
other words, the air flow will not
be lb/min but kg/min; the temperature will be expressed in C
(Celsius) instead in F (Fahrenheit).
 Here on the first page of reading
values, we can do some checking
and compare the data without usage of a specific engine data. By
increasing the engine RPM, we can
follow the timing advance whose
value must be proportionately
greater in degrees at higher engine
revs. A similar situation follows
with the air flow. If we doubt
whether the MAF sensor works
correctly, we will verify the
amount of air entering at lower
and higher engine RPM. Certainly, at higher engine RPM, the
mass of air must be proportionately greater. If there is no significant difference in the mass of air
flow, we can suspect that we have
defective MAF sensor.
 In the row number eight, we find
the term Fuel System 1 Status:
Closed Loop. This phrase can not
be explained in a short and understandable sentence. amely, if we
look for assistance in various programs or through the Internet regarding this term, in most cases we
shall be confused by various explanations. Fuel System Status Closed
Loop in a free translation, or explanation, would mean: a closed
fuel system circle. However, since
this phrase even English born people can not translate or explain in
understandable words (see the
questions on the forums), it is necessary to understand what the author of this phrase intended to say.
Thus, Fuel System Status Closed
Loop controls the fuel dispensing
in the engine via injectors, relying
on the lambda probe signals, and
other engine sensors parameters.
In order that ECU could establish
such status, the engine must be
running at operating temperature.
Opposite to this mode is the Open
Loop Status which ECU will apply
when the engine is cold and
Lambda probe is not in operation
and the entire system runs on the
installed program for such condition. Open Loop will also be used
while driving under conditions of
high engine load, and extreme
weather conditions.
 In the following example on the
new page, we can see a number of
 59
rows where we can read the O2
sensors or lambda probes with different labels. These marks usually
give quite a headache when testing
because of lack of their meaning.
Every diagnostic scanner has a
possibility to read several O2 sensors values. To know that readings
are related to a particular sensor,
they are marked with O2 1, O2 2,
O2 3 etc. The word Bank has multiple meanings which depend of
sentence context. In our case, the
closest explanation would be the
river bank, left and right. Thus,
depend of their positions the
probes are labelled as Bank 1 or
Bank 2. In an in-line engine, Bank
1 probe will be positioned next to
the engine or before the catalytic
converter and the Bank 2 after
catalytic converter. In six cylinder
in-line engine with a split exhaust
manifold into two groups, the
probe before the catalytic converter would be labelled as O2 sensor 1 Bank 1 for the first three cylinders and O2 Sensor 2 Bank 1 for
the next three cylinders. If such
engine has one catalytic converter,
the probe behind it would be labelled as O2 Sensor 1 Bank 2. In
case of two catalysts, probes are
labelled as O2 Sensor 1 Bank 2 and
O2 Sensor 2 Bank 2. On in-line engines Bank 1 is the position of the
first engine cylinder. On the engine in V formation, Bank 1 is the
side where the first engine cylinder
is marked. umber of sensors will
depend of number of cylinders and
the type of exhaust manifold. If the
six-cylinder V engine on each side
has one exhaust manifold, socalled three in one, then we have
one sensor on each manifold labelled as O2 Sensor 1 Bank 1 and
O2 sensor 1 Bank 2. Depending of
number of catalytic converter on
such engine, central one or left and
right when two installed, the probe
behind the converter will be labelled as O2 Sensor 1 Bank 2, or
O2 Sensor 1 Bank 2 and O2 Sensor
2 Bank 2. On eight cylinders engine in V formation, we will often
find two sensors on the exhaust
manifold: O2 sensor 1 Bank 1, O2
sensor 2 Bank 1, O2 sensor 1 Bank
2 and O2 sensor 2 Bank 2. Behind
each catalytic converter sensors
are labelled as: O2 sensor 3 Bank 1
and O2 Sensor 3 Bank 2.
 If we come to the situation that
we are not certain which is Bank 1,
we can always unplug one of the
sensors. The program will
notice the lack of data from
the sensor and immediately
determine whether the
faulty sensor is on Bank 1 or
Bank 2. Due to the misinterpretation of these marks, in
practice is often replaced
wrong sensor and fault remains uncleared. Of course,
60
the next step is replacement of the
other sensor by the principle of
elimination, what considerably
and unnecessarily increases the
cost of repair.
 In most cases, diagnosing a malfunction of the probe is a routine
job. But sometimes, it is not. For
example, there is a DTC which indicates a defect lambda probe.
Routine work, install a new
probe and the problem is
solved. The engine is
warmed up, DTC is erased
and O2 voltage reading is in
order. But, the next day the
MIL illuminates and the
same DTC comes up again
We clear the DTC again and
it does not come up until the
next day. Where is the problem? When reading the
DTC definition, people usually do not pay much attention to the full text. amely, at
first glance we see the O2 sensor
code and do not read any further.
The definition usually warns us
about the short circuit in the sensor, or malfunctioning of sensor
heater. Well, and this is solvable
by replacing sensor, but obviously
sometimes not. Beside the malfunction of the sensor heater, there
may be a problem with sensor
heater power supply. Thus, the
probe heater is in order, but there
is no power supply. When engine
runs at low temperature, ECU registers faulty sensor heater and
turns the MIL on. If we are performing diagnostics test when engine is warmed up and clear the
DTC, it will not appear until we
restart the engine when it cools
down. Here is another example
which points to the caution and
requirement of certain checks before a final diagnosis is concluded.
 On the shown picture we see
readings of the O2 sensor 1 Bank 1
and O2 sensor 1 Bank 2. If the sensors are in order, we shall read the
voltage oscillation between 0.2 and
0.8V on the first sensor. Second
sensor will have a constant voltage
with a value of about 0.45V.
Knowing that the front sensor with
its variable voltage regulates fuel
dispensing trough the ECU, such
oscillation within mentioned voltage is normal. Having passed
through the catalyst CO burns out
and gases oxidise. Thus, the exhaust gases value ratio is relatively
constant, and so is the voltage at
the second probe. In the case of
voltage fluctuations on the second
probe, we can conclude that the
catalytic converter needs replacement. On the following oscilloscope photos, we can see the ideal
 61
romašne smjese. sinusoidal probe voltage, rich
mixture voltage and lean mixture voltage.
 Constant probe high-voltage
due to the rich fuel mixture is
not always associated with its
malfunction. So, beside a lot of
information which we can obtain
trough these eight program
pages, we can check the engine
coolant temperature which may
be the cause of increased fuel
dosage.
 Unlike Scan Tool which is
really satisfactory for the engine
and transmission diagnostics, as
already said, on the market we
can find a serial of commercial
and Freeware programs. These
free programs are not able to
provide any more readings than
Scan Tool program. But, commercial programs offer some additional options which are related to the engine and transmission only. This refers to the universal OBD II programs. Programs which provide diagnostic
options for other vehicle modules
are programmed for a particular
brand or group of car manufacturers.
 One of the commercial programs which provide additional
options is the Scan Master. This
program gives us the opportunity to read PID (Performance
Information Data) or in free
translation, performance data of
individual sensors. In this option, we will be able to read the
performance of sensors that are
selected on the left side of the
62
program. Read and compare
the performance of sensors
selected, is only possible if the
program has the original parameters for this vehicle.
Therefore, in the lower part
of the program we have a
choice of performance readings for options which are
supported in (Select only Supported) or all the options
(Select All).
 Let’s say that we have MIL
On and the code which indicates faulty O2 sensor. Selecting
the PID option we can see what
data the O2 sensor sends to the
ECU. Marking multiple sensors in
the PID option, comparing the
voltage value or a percentage, we
can see how an error affects the
other. For example, if we suddenly
accelerate, engine RPM will increase and the value of the TPS
sensor readings will change as well
as the value of the MAP sensor signal due to pressure drop.
 Another interesting feature of
this program, which would more
suits the enthusiast, is the: acceleration, torque and power
measuring. Selecting Power
we have opened up the possibility to measure the acceleration and engine power. This
program will calculate just
how much time has elapsed to
reach the speed of 100 km/h,
or any other rate that we defined in the Max speed.
 For engine power and
torque measurements (Dyno
test) will be required to enter
a good deal of data: gross vehicle
weight, the weight of the driver
and front passenger, baggage, fuel
quantity, length and height of the
vehicle, wheel size, weather conditions etc. The more information we
enter, the more precise measurements are. To make this test the
most accurate, it is advisable to
make measurements in both directions on the same road track.
Knowing that road is never perfectly flat, or that we are going uphill or downhill, the engine power
will vary. In addition, however it is
 63
unnoticeable, wind will always
blow in our front or back. Finally,
calculating the mean value of each
measurement, we will get a realistic power. After the test is done,
the results can be saved to our
computer and printed. In addition
to the graph on the printed document, we can see the sequences of
results. Beside the data that
we have entered, there are
also information of measured engine power (58.35
kW) and power on the
wheels (52.69 kW). The difference in power between the
engine and driving wheels
was lost on the transmission
mechanism between the engine and wheels. Maximum
power of 58.35 kW is
achieved at 5085 rpm. The
maximum torque of 127.49 m is
achieved at 3367 rpm. Maximum
power and torque were measured
in third gear.
 Let’s go back for a moment to
those more complex diagnostic
devices which can perform more
functions on a number of vehicles. Some of the most known devices among mechanics are Bosh
KTS and Multi-Diag. To start
with, let’s mention that KTS 570
is offered (Internet) at a price of
U.S. $ 4,510, where some other
expenses like postage and… have
to be added. We should admit,
very serious price. But this is not
the end of expenses for such devices. They usually come with the
OBD II connector, while the
other connectors and cables have
to be purchased separately. Furthermore, the program upgrade
is charged, if the price does not
include one-year free upgrade.
Before purchasing, the program
content has to be checked to
avoid any surprises regarding its
testing capabilities in a way: this
vehicle or system is supported
64
but others are not... Let’s say that
even we can afford such costly
equipment, it will be in most cases
useless without adequate knowledge about electronics management and diagnostic testing. Besides having a much more functions than universal ELM 327 device, such expensive scanner does
not explain faults any clearer than
other devices. ow, we are back
again on the trouble codes and the
possibility that read DTC does not
mean solving the problem by replacing a sensor or actuator. That
is to say, without knowledge
it simply does not work. In
addition, even with these
expensive devices Pinout
Box is often used, and therefore we need to know what
are the protocols, K and L
lines and everything else related to the diagnosis.
What's more, when we are
talking about the functions
complexity of such a device,
then we can certainly expect
much better results from
cheaper interface and program, foreseen for a particular type of vehicle. Thus,
purchasing one universal
OBD II scanner and subsequently buying other devices, financially is far more
bearable than buying very
expensive equipment, which
can disappoint us because
we expected quite a lot for
such amount of money.
Many people do not understand exactly what program
upgrade means. All manufacturers
of diagnostic equipment complement their programs from year to
year. Knowing that these are not
universal scanners, they have to
have installed software for particular type of vehicle with diagnostic functions. Because of the
programs complexity, manufacturers constantly supplement programs with new types of cars,
more functions and expand programs for already listed vehicles.
Certainly, such updates someone
has to pay. But, that revenue
 65
would not only depend on the program upgrade, the producers
launch on the market new devices
with improved performances,
compatibility, wireless connectivity, etc. So, the only Bosh company launched the scanners KTS
340/520/540/650/670, and so on.
 The intention of this article is
not invalidation of these devices,
but only a comparison of their
functions with simple universal
devices or those foreseen for a particular type of car. Moreover, this
was a little warning to those who
have believed that the purchase of
such expensive devices solve the
problem of diagnosing faults on all
types of vehicles and their equipment.
 An appropriate comparison to
the function of such devices is the
review of database such as the
popular Autodata, without which
no one decent car workshop can
function properly. Autodata and
Tolerance Data have thousands of
precious data. However, in comparison with the professional
workshop literature (Workshop
Manual) for particular vehicle,
these databases are quite scarce.
Therefore, we may conclude that a
professional interface and software
for a particular type of vehicle will
provide far more functions than
any expensive universal diagnostics device.
 Handheld scanners
 In addition to the interfaces and
associated programs which work
with the help of the computers, we
can fid on market a great offer of
so-called hand-held scanners.
These scanners are very practical
for work outside the workshop and
quick access to DTCs. So what is
the difference between them and
66
the interfaces that run through the
computer? Primarily, computer
gives a better program functions
visibility on the big screen than it
is on, usually very small, handheld
scanner display. Furthermore, in
addition to the diagnostic program, we have other programs
with databases in the computer
which we use in diagnosis, and this
is basically the biggest advantage.
 In any case, when we talk about
universal OBD II handheld scanner, it does not give any less information than ELM 327 interface
with Scan Tool program. Even
more, little more expensive handheld scanners provide Freeze
Frame option, and the PID configuration. Handheld scanners
which are designed to diagnose
faults on certain types or groups of
vehicles can be also very complex
in terms of diagnostic programs.
Good example is easy affordable,
handheld scanner for VAG group
cars with the ability of scanning
the vehicles from 1991 onwards.
With the scanner and additional
small fee we will get the connector
adapter for OBD II cable to OBD I
(two individual connectors), which
is used on cars prior the OBD II
system. In addition, it is not uncommon for these scanners to provide readings of ABS and SRS systems and resetting the service intervals. Thus, the seemingly frivolous little braces may well serve
the purpose. However, it should be
borne in mind that these scanners
are designed for quick access of
DTCs, while those for use by computer have more complex programs with multiple functions, oscilloscope readings etc.
 On the previous page, we can see
the photo of a very good handheld
multiprotocol middle class scanner
GS 500, which will along with
other information provide the ability to read the Freeze Frame. Connecting such a scanner is more
than easy. Immediately after connection to the vehicle OBD II connector, the scanner searches for
the corresponding protocol. avigation trough the scanner program is simple by using the up and
down and Yes-o buttons. This
scanner will be equivalent to an
ELM 327 interface and Scan Tool
program with the additional possibility of reading Freeze Frame,
which a basic Scan Tool program
does not have. However, if we use
ELM 327 interface via computer,
 67
we have the possibility to use different programs which we can
purchase or download as a freeware, while with handheld scanner
this is not possible. Thus, it is a
matter of choice and needs.
 OBD II and new vehicles
 So far we have seen that the
OBD II scanners can only access
the engine module and provide
relatively limited information compared to other options provided by
scanner foreseen to scan the certain types of cars. Thus, from a
large number of uninformed in the
principle of diagnostic tools, we
can often hear the question,
whether a universal OBD II diagnostic device can read DTCs occurred in the ABS and other systems. In the current text this possibilities were intentionally ignored,
in order to avoid misunderstanding in terms of, if it can, why it
does not or similar. Thus, the vehicles of the new age are equipped
with modern technology related to
driving safety, and other comforts
of today's cars.
 We will mention one of many examples where universal OBD II
scanner can read DTCs associated
with ABS. A car that has a built in
ESC (Electronic Stability Control),
uses ABS system and engine module to control the vehicle stability.
When vehicle has tendency to drift
due to excessive speed, slippery
road and similar situations, the
ESC module will use the ABS to
slow down one of the wheels to
help stabilizing the vehicle. At the
same time, it will automatically
reduce the engine power to prevent sudden acceleration which
could additionally disturb the vehicle stability. Using a very complex calculation of all available parameters, this ECM will maximally stabilize the direction of the
vehicle. As we see, the complex
process of vehicle stability control
requires an interaction of engine,
ABS and ESC modules. In one
such integrated circuit of several
modules, where the main module
is engine control module, all data
will be stored in the ECU, or engine computer.
 If we know that the OBD II
scanner has access to data
from the engine module, in
this case it will be able to access all data stored in it. In
other words, if there is a
problem or fault in the ABS
system, it will be stored in
the form of DTC in the engine module, and will appear
in option of DTC Reading on
any OBD II scanner.
 The shown photo, humor-
68
ous but very clearly, shows the integration of ECMs, where the central computer is the chief of situation, for now still the ECU. If we
have this situation in a modern
car, all stored codes will be available to us trough the ECU regardless of system to which they are
related: ABS, ESC's etc.
 Vehicle manufacturers are obligated to provide access to trouble
codes which are related only to the
ecology. These are mainly the generic trouble codes with marks
P0xxxxx. However, it is very difficult to select the availability of generic and factory codes. Therefore,
manufacturers use their codes for
which many technicians do not
have definitions. But we saw
trough the previous text, that this
obstacle is not insurmountable. In
addition, environmental laws are
now so rigorous that some kind of
malfunction of other systems in the
vehicle can affect excessive pollution. Thus, according to the
world’s regulations, air conditioner malfunction can cause pollution. Insufficient air pressure in
tires will contribute to increased
fuel consumption. Improper setting of the suspension (where automatically adjusted) will affect the
air resistance in terms of turbulence, and also contribute to increased fuel consumption. Automatic adjustment of lights, in case
of failure could endanger someone's life, etc. Therefore, more or
less, all systems on the car are subject to enabling fast fault recovery,
and hence a simple approach to
trouble codes.
 Availability of trouble codes
should not be a secret for a number of circumstances which can
put a vehicle’s owner in some inconvenient situation. For the mentioned reason, on some vehicles
DTCs are displayed on the instrument panel. For example, even
older Jaguar models, say produced
1990th have the button, whose
function is defined in the owner’s
manual, which we can press and
read the DTC, or fault in the electronic management of the vehicle.
Thus, even then the choice was left
to the vehicle’s owner, whether to
service or repair his car at an authorized service center, or elsewhere. Of course that such company could afford easy access to
DTCs relaying on Jaguar’s owners
decisions to maintain their vehicles
nowhere else but in official Jaguar
services. Returning to the diagnostic procedure described in the previous article, we are aware that
access to DTC's does not mean
successfully and simply solving the
problem.
 Using OBD II scanner on new
cars, many will be surprised how
much information is available. If
we take for example today’s cars
which uses a modified gearboxes,
mainly controlled by the ECM,
faults at all actuators on Automatic, Tiptronic, Dual Clutch and
other types of transmission will be
accessible by simple OBD II multiprotocol scanner.
As always, one has to be careful
when giving instructions as there is
 69
a need for a warning that such a
scanner is not all diagnostic equipment that we need for proper diagnostics, regardless of the expanded
capabilities of accessing the information. So, a simple OBD II scanner will be able to draw out all the
trouble code from the central
ECM on newer vehicles. But, that
is all, no further testing will be
possible to run without the proper
interfaces and programs. However, to an expert, DTC or fault
code should be sufficient to cope
with a problem or malfunction of
the vehicle.
 Pending codes P0xxxx *
 When reading the DTCs, we often encounter the trouble codes
which are usually marked with an
asterisk, PD or Pending Code, in
free translation error in development. This type of code stored in
the module memory will not turn
on the MIL. What is it? There are
number of situations which can
cause the sensor o actuator failure
for a short time. Such failure can
last for a second or two, but
enough to be registered by module.
If the fault is not constant, computer is not sure if problem is real,
just some coincidence or kind of
causal error. Therefore, the module will register an error, but will
not record it as effective until it is
repeated and the calculations show
the actual defect. Therefore, when
we encounter such a code, it
should not be ignored, but definitely taken into account as a
cause of possible problem. After
recording the code number and
eliminating the real fault, we can
wipe out the code from module
memory and check after a while if
it comes up again. If we encounter
during the scanning just such a
pending code, after writing its
number down we can delete it and
check if it shows up again after a
while.
 In case of repetition of the same
DTC marked as Pending code, the
error is probably related to mechanical problems. Suppose that
we have such a code associated
with MAF or MAP sensor, the
cause may be a light damage of
one of the vacuum hoses connected
to the engine intake manifold.
When the code is associated with
turbine, such failure may be related to the defective (sticking) bypass valve mechanics which redirects exhaust gases. Partially defective fuel cap may indicate a
malfunction of the Purge Valve
(valve for removing gases from the
fuel tank).
 If we are not sure what to do
with a Pending code, and assuming
that the engine is running
smoothly, it is advisable to leave it
in the ECU memory. If the error
does not show up again after about
forty times that engine is restarted,
and after running at the operating
temperature, the module will delete it from memory. If the error is
repeated, the module will register
the problem as an existing DTC,
remove the asterisk and turn the
MIL on.
70
 The most common causes of trouble codes
 In this section we shall have
some examples of trouble codes
where the problem does not lie in
the failure of sensors or actuators.
As said before, the error stored in
the engine computer only directs
us to the particular sensor or actuator, and never suggests its replacement as solution for solving
problem. Therefore, before deciding to replace a particular part, it
is necessary to make a series of
checks. For this purpose, the biggest benefit is a universal multimeter which can measure: voltage,
resistance... Voltmeter will measure the input or output voltage,
while the ohmmeter will help us to
test coils or O2 sensor heater. In
addition to tests which we can do
ourselves, it is advisable to use
professional factory books, if available, which are foreseen to help
repairers of certain types of cars
with various sketches and data.
Such a literature leads to more
possible problems associated with
individual trouble code numbers.
 Described examples do not solve
problems related to the trouble
codes, but can definitely be helpful
in diagnosing procedure.
 O2 sensor DTC problems
 This example is related to the
reading of a constant low or high
voltage on the lambda probe, as
well as very slow or no voltage oscillations.
 Lambda probe reads presence
of oxygen in the exhaust gases, and
generates a voltage signal proportional to the amount of oxygen.
The voltage signal can vary from
approximately 0.1 to 0.9V. Low
voltage indicates the lean mixture
and the high voltage rich mixture.
When the engine is at operating
temperature (Closed Loop) the
ECU uses the voltage signal to balance the mixture. Faulty sensor
will disable the Closed Loop, and
the result will be increased
fuel consumption.
 Constant low voltage signals can cause the occurrence of DTC, which indicates a malfunction of the
probe. However, the cause of
the low signal value may lie
in damaged vacuum hoses
connected to the engine intake manifold. The entry of
additional volume of air will
pauperize the mixture and
automatically increase the
amount of oxygen in the ex-
 71
haust gases. The same case we
shall have if there is a damaged
gasket on intake manifold, as well
as on exhaust manifold. The misfire of one or more cylinders or a
burnt exhaust valve can also be
cause of excessive oxygen in the
exhaust gases. In both last cases,
the unburned gases will increase
the amount of oxygen in the exhaust gases.
 Test of the O2 sensor has to be
done by reading the voltage oscillation when suddenly fuel-air mixture is changed. Apart from reading voltage value with voltmeter,
this option is provided in every
OBD II program. When the engine
is at operating temperature, disconnect a vacuum hose from the
engine inlet manifold. The value of
voltage at the test must fall sharply
and quickly. Small, slow or no
change in voltage certainly indicates a malfunction of the probe.
 If, in addition to the O2 sensor,
trouble codes are also related to
the MAP sensor and the occasional
misfire, problem usually lies in a
serious vacuum leak from the intake manifold. Vacuum leakage
which is often the cause of mentioned problems usually is present
only during the engine operation
at idle.
 Checking the vacuum leaks can
sometimes give a real headache,
especially if there is a small leak.
In the number of cases, vacuum
leak is not visible or hearable.
Apart from the described possibilities, the vacuum leak
can be expected on the
worn fuel injector
seals, which are usually inaccessible for
inspection. In certain
cases we can use WD
40 spray for finding
smaller leaks. Spraying vacuum connec-
72
tions when engine is running, we
can hear and see the entry of fluid
into the intake manifold. Moreover, when we encounter a vacuum leak with spray, the engine
RPM will change for a moment. In
the photographs we see several examples related to this problem. It
is not necessary to mention that
there are various instruments to
check the vacuum leaks. However,
in most cases, we have to cope with
minimal equipment which we have
on disposal.
 MAP sensor DTC problems
 MAP sensor, depending of the
type (see Automobile electronics &
4-stroke engines), changes the output voltage as the vacuum changes
in the engine inlet manifold, and it
is the one of the parameters that
ECU uses to determine the moment of ignition and dosing fuel.
Malfunction of this sensor will affect the engine performance
and may be manifested by
slow acceleration, lack of
power etc.
 As it was the case with the
O2 sensor, here we can also
look for problem in a vacuum leaks. If the engine is
equipped with TPS sensor,
we can compare the values
of voltage oscillation on both
sensors, which should be
proportional. Regardless,
whether on one of these sensors value rises or falls during acceleration, the value
must be proportional on
both sensors. Suppose, that by
opening the throttle at the engine
inlet manifold TPS sensor indicates voltage deviation by plus or
minus, the same situation we
should meet at MAP sensor. Vacuum is the strongest when engine
is running at minimum RPM
(idle). By opening the throttle vacuum is reduced, and the MAP sensor registers it by stronger or
weaker voltage signal. If there is
not TPS sensor installed, we are
measuring MAP sensor output
voltage at different engine RPM. If
after these checks, there are
doubts about the accuracy of the
sensor, we should check the power
supply on the connector and perform the identical test previously
described. Disconnect the vacuum
hose from the intake manifold and
monitor the changes of output
voltage values. If the power supply
is correct and we do not notice the
change of sensor output voltage at
 73
this test, we can conclude that the
sensor is defective.
 If we use the OBD II program
for such test and choose the option
Sensor data we can read the pressure values at different engine
speeds (RPM). The value of pressure is shown in row Intake Manifold Pressure.
 On the shown graph we see the
reaction of the MAP sensor when
vacuum oscillates in the engine
inlet manifold. By increasing the
engine speed, or opening the throttle, the vacuum in the engine inlet
manifold drops and sensor output
voltage increases.
 TPS sensor DTC problems
 Among other parameters from
the TPS sensor that ECU uses in
the calculations of the air-fuel ratio and ignition timing, one of the
most obvious problems related to
this sensor is hesitation during the
rapid acceleration. Wrong or undue signal in the form of changes
in output voltage from the sensor
may be the cause of this problem
and others related to engine performance and fuel consumption.
 Checks and measurements of this
sensor can be also performed with
the voltmeter (depending of the
type of sensor). Knowing that
these sensors usually work as sliding resistors, it will not be difficult
to conclude that the output voltage
is proportionally falling when
opening or closing the throttle. Of
course, it is necessary to check the
sensor power supply on positive
terminal of the sensor connector.
As these sensors are mostly mechanical sliding resistors, the problem is mainly associated with oxidation of the sliding elements or
worn bushes causing free-play in
the sensor and poor contact.
 It often happens that measuring
of output voltage is correct, but
after running car for several kilometres MILL turns back on with
the same DTC. Therefore, when
measuring the output voltage from
the sensor, use a plastic screwdriver handle and gently tap on
the sensor. If there is a poor contact on electrical sliders inside the
sensor, we will not have continuous but interrupted output voltage.
If this is the case, we can conclude
that sensor is defective. Such a sensor can be replaced, but those
more experienced can try to dismantle the sensor, clean the contacts and test it again. Certainly,
such task can be performed on
older vehicles models, while newer
cars have mostly sealed elements
which can not be repaired.
 On new types of cars, TPS sensor
is automatically calibrated by the
74
installed program in the ECU. On
older types of cars, it is necessary
to calibrate the TPS. Calibration
possibilities we shall find only in
more complex programs provided
for the diagnosis of specific types
of vehicles.
 In the photographs we see the
usual TPS sensor position on the
throttle shaft, and disassembled
sensor with sliding contacts. Going
back to the sensor test, it should be
 75
noted that skilled mechanics will
cope with sensor terminals and
measurement values. The others
will look for specifications in
workshop manuals or in data programs.
 On the following sketches we see
shown examples of connecting and
calibrating the TPS sensor in the
program for a particular type of
vehicle. TPS sensors usually have
only three terminals. On the
sketch, the positive terminal or
sensor power supply, whose value
is usually 5V, is highlighted in yellow. The negative terminal or
earth is highlighted in black, while
the sensor output terminal whose
voltage value varies from 0-5V is
highlighted in green.
 On the program window we see
the option Basic Settings. The
menu shows the values of the TPS
sensor (TPS Settings) in the highest (High) and lowest (Low) throttle opening position, which we obtained by clicking on the Fetch
From ECU. If the program does
not provide automatic values adjustment for particular type of engine, we can enter them manually,
previously finding them in workshop manuals or else where. After
entering appropriate values and
clicking on the Send to the ECU,
we have completed the sensor calibration.
 CTS sensor DTC problems
 Coolant Temperature Sensor can
give quite a headache in terms of
causal errors. Malfunction of the
sensor will affect significantly elevated concentrations of carbon
monoxide due to the excessive dosage of fuel. Engine coolant temperature sensor also acts as a resistor. It is usually supplied with voltage of 5V, which drops in the output signal as sensor heats up. This
information will be used by ECU
to increase the dosage of fuel until
engine reaches the operating temperature.
 Suppose two situations. Resistor
is in a short-circuit, and signal has
a constant value of 5V, regardless
of engine temperature. The engine
will run smoothly until the coolant
76
warms up, when the mixture becomes too rich, and engine starts
to run erratically at idling with
significantly increased consumption and tendency to stop running.
There is also a quite confusing
situation in the ECU processor calculation system. Lambda sensor
reads high concentration of carbon
monoxide, while the temperature
sensor provides a signal that the
engine is cold and needs increased
fuel dosage. After a certain period
of engine running under such conditions, leads to deposition of carbon on the lambda probe, what
completely disrupts its reading. It
is quite obvious that chemical
process in catalytic converter is
also disturbed, and control probe
will send negative signal accompanied with few more errors related
to fuel pressure, etc. So, in this
case also, we read several DTCs
but problem lies in only one of
them. With a good theoretical
knowledge, everyone will first consider the validity of the CTS sensors. How to test CTS sensor?
 As in previous examples, we will
first check the sensor power supply. It is strongly recommended to
use the multimeter instead of test
lamp which is commonly used in
such procedure. Due to possible
incorrect connection, the test lamp
may cause a short circuit with very
undesirable consequences. If we
have, when ignition is on, power
supply of 5V or other value specified for particular vehicle, we can
perform the sensor testing. The
sensor can be tested on the engine,
or when taken out.
With the multimeter we shall
measure the resistance between
two terminals on the sensor, which
value, in this case, suppose to be
7000-13000 Ohms when sensor is
cold. By heating the sensor, the
resistance must be proportionately
reduced to 700-1000 ohms when
engine reaches the operating temperature. If there is no difference
in the resistance, the sensor is
faulty.
 Why should we test the sensor if
DTC shows its obvious failure?
Primarily, because reading showed
several codes instead of one. Furthermore, the problem does not
necessarily lie in the sensors failure. Insufficient coolant volume
 77
will affect the faulty sensor response. In such cases, the heated
coolant will not heat the sensor,
but only a formed steam to which
the sensor will not react as it
would immersed in the liquid. Another problem may lie in the thermostat failure, which does not
close the fluid flow completely and
thereby preventing the engine to
reach the operating temperature.
Therefore, if we want to be absolutely sure that we know we are
doing and prevent possible unnecessary investment, it is advisable to
test the sensor. Presented sketches
show the CTS sensor test procedure.
 The last sketch shows the sensor
test when immersed in a heated
fluid. On the chart we see how resistance increases when sensor is
heated. This is the opposite situation from previous one where the
resistance decreases by heating the
sensor. In any case, the resistance
changes its value by heating the
sensor, either by reducing or increasing the resistance value. Just
because of such different values, it
is very useful to use the literature
for particular vehicle, so that we
know what we are looking for.
Such information is quite helpful if
we are performing test by short
connecting terminals on the connector. Suppose we have a case of
excess fuel as described before.
Knowing that resistance is reduced
by heating the sensor, we can
bridge the two terminals on the
sensor connector and see the effect. How? If warming reduces the
resistance of the sensor, the value
of the sent signal to the ECU, at
engine operating temperature, will
be 5V. The same values of the signal we shell get by short connecting two terminals. In other words,
if the sensor was faulty, leading the
full voltage output to the engine
computer, we provide information
of the engine operating temperature achievement. Taking into account this information, the ECU
will reduce the dosage provided
for a cold engine and switch on the
Closed Loop, when it relies on the
Lambda probe signals.
78
 Misfire DTC problems
 Misfire term is usually badly defined and interpreted. The literal
translation would be the lack of
fire, which is not so bad explanation. However, this term refers to
the malfunctioning of one or more
cylinders, either due to lack of
spark or fuel. When such codes
appear, we shall read Random
Misfire or Misfire of 2nd cylinder, or
some other number. In the first
case we have a problem with sudden malfunctioning of several cylinders without any order, or, we
would say, randomly. In the second case, malfunctioning refers to
the cylinder number 2, or some
other numbered cylinder. This
means, that the ECU has detected
discontinuity of functioning on one
or more cylinders defined by numbers.
 Random Misfire usually occurs
due to the bad fuel or some impurities in it. The cause may also be
due to failure of the vacuum hoses
or worn seals. Disrupted ignition
timing and carbonized injectors
are also often the cause of these
errors. Worn out distributor cap
(on engines with distributor) and
spark plugs cables covered with
dirt and grease can also cause disruption of cylinders without any
order.
 When a Misfire DTC occurs with
cylinder number, then we know
that we have to focus on that cylinder and look for the cause of firing
interruption. To solve such problem, theoretical knowledge and
experience will be of great necessity. Most often, we firstly check
the condition of spark plugs. Having in mind how any mechanic is
familiar with problems caused by
spark plugs, cables and pipes; let’s
talk about misfiring of cylinders in
pairs. Vehicles which have two ignition coils, or one for two cylinders, and the error refers to a pair
of cylinders that are connected to
the one of them, we can doubt its
validity. On vehicles with a separate coil for each cylinder, we can
apply the test by exchanging the
coils from one cylinder to another,
and see if the error will again refer
to the same cylinder, or the one on
which we set up a coil of doubtful
validity. The same test can be applied in the first case too, if we
have identical connectors. Such
verification will certainly determine, whether we have defective
coil, or the problem lies elsewhere.
 The second problem usually lies
in the injectors. If we suspect the
injector, it is recommended to replace it with one from another cylinder. The test is identical to previous one with coils. If an error occurs with the number of cylinder
where we installed the injector
with dubious validity, we can conclude with certainty that injector is
faulty. However, if the error repeats with the same cylinder number as before, the problem lies
elsewhere. Certainly, if we
swapped coils ad injectors between
cylinders and found nothing
wrong with them, but DTC still
exists on the same cylinder, we
 79
should look for the problem in the
worn vacuum seals or, furthermore, bad piston rings and valve
seals, which will cause accumulation of oil deposits on the spark
plugs.
 In practice, the occurrence of
such DTCs is usually caused by
deposit of carbon on the injectors
where occasionally proper injection fails. It is not uncommon that
mentioned checks are performed,
and, in those worse cases, very
costly replacements of injector,
spark plugs cables and coils are
done, without any results. Just for
this reason, these tests are recommended. Satisfied with all performed tests which have showed
the correctness of all electronic elements and mechanical parts, injectors cleaning is all what is left do
be done. Do we have to do this job
before or after these tests, it is difficult to say. Those a little more
experienced will be lead by vehicles mileage and bring the right
decision. Certainly, if we work on
the vehicle with mileage of several
hundred thousand miles, we shall
immediately suspect a carbon deposit on the injectors, while on
those with low mileage we shall
first perform described tests.
 Injectors contaminated with
various sediment, are the most
common cause of hesitation during
the acceleration and uneven engine
idling, including Misfire. On the
photographs we can see the irregular fuel injection due to deposits of
carbon and other materials.
Proper injection is shown on comparative photo. So, let's say something about the possibility of cleaning the injectors. The simplest way
is pouring special chemical product into the fuel tank, which will
pass through the injectors and dissolve the accumulated material.
Such a procedure is quite effective,
if there is a milder form of deposits. In more serious cases of deposited carbon and other impurities,
injectors have to be removed from
the intake manifold and cleaned by
machine. If we want to save some
money, a similar procedure can be
done by purchasing a spray, and
clean the injectors under the pressure with its content. The photo
shows this process with the help of
battery which activated the injector solenoid and opened flow.
80
Some sprays offered on the market, allow us to empty its content
directly trough the throttle, previously removing the air filter. Such
sprays will clean the outer surface
of injectors, deposits on valves, pistons and cylinder compression
area. But if we want a proper injectors cleaning without risk of
failure during the cleaning, they
should be connected to the cleaning machine. Using professional
equipment to clean injectors, allows us to have the flow of solvent
trough the injector until we are
satisfied with proper fuel injection.
During the cleaning, these machines allow us to measure the
amount and equalization of the
fuel flow through the each injector.
 On the next photo we see a typical injectors cleaning machine.
Unlike the smaller available machines, this one can clean and test
up to eight injectors at once. In the
measuring cups below the injector,
we measure the quantity of injected fuel, which ideally should be
identical in all eight cups.

 EGR valve DTC problems
 Problems related to the EGR
valve, usually are results of failure
on vacuum or electromagnetic actuator due to the accumulated carbon deposit. It is not uncommon to
 81
have blocked passages through
which the exhaust gases passes into
the engine intake manifold (see
how the EGR valve works in the
book Automobile electronics & 4-
stroke engines).
 Testing the EGR valve begins
with checking the vacuum or solenoid operated valve. If there is a
vacuum operated valve, it is necessary to check the vacuum and vacuum regulator which operates the
valve. Weak vacuum or no vacuum at all, at the valve, usually is
the result of the worn hose or a
bad connection. The solenoid valve
will shall check by bringing power
supply directly to it from the vehicle battery. Such a test would not
be effective if we do not take the
EGR valve assembly of the engine.
In most cases, carbon deposit on
the mechanism (valve shaft) is so
great that disables the opening and
closing of passages for gases flow,
even when the actuators are working. Therefore, in order to properly determine the condition of the
EGR unit, it must be removed
from the engine, carbon deposit
dissolved and entire assembly
thoroughly cleaned. Only after we
have cleaned all dirt from the
housing and all mechanical moving parts, we can test the actuator.
If there is a vacuum actuator, we
can test it by connecting it to any
vacuum hose on intake manifold.
The vacuum will lift the diaphragm and the valve must be
fully open. After that, we have to
test the vacuum regulator which is
controlled by ECU. Knowing how
EGR works and when the valve is
opened, such a test will be harder
to do when car rests. However, if
we found defect during the cleaning and testing the unit, further
testing, most probably, won’t be
needed.
 When servicing the EGR unit, it
is necessary to pay attention to the
output gases passages from the engine exhaust manifold and inlet
passages in the engine intake
manifold. If we overlook this part
of checking procedure, it may happen that we have the EGR unit in
order but did not solve the DTC
problem as gasses passages, to and
from the EGR unit, are blocked.
 In addition to the carbon deposit
preventing the opening of the EGR
valve, it can cause a constant partial opening of the valve. In this
case we shall have a problem with
very uneven engine idling, and the
possibility of DTC appearance as-
82
sociated with a MAP sensor and
Misfire. So, if we have the trouble
code related to the EGR and few
additional codes, it would be wise
to service the EGR valve first and
then deal with other codes if they
still exist.
 CKP sensor DTC problems
 When DTC occurs related to the
crankshaft sensor, it is also necessary to make a few checks before
deciding to replace the sensor. Before we start with checking the accuracy of CKP sensor, it is necessary to determine whether it is a
magnetic inductive sensor, or the
so-called Hall Effect sensor.
 Inductive sensor usually has only
two terminals. Using the, previously mentioned, multimeter we
can measure the resistance between two terminals on the sensor.
The resistance value of particular
sensor we can find in the workshop manuals or in data programs.
But if we do not have access to the
exact resistance values, the measured values between 200-400 Ohms
can determine the accuracy of the
sensor. The next inspection will
determine induced AC voltage output. Switching the multimeter
knob to AC (Alternating Current),
connect the instrument probes to
both CKP sensor terminals. When
turning the engine with starter, the
output voltage must be between
0.2-2V. This value can be also
found in the manuals, but this approximate value will be sufficient
to evaluate the possible malfunction of the sensor. amely, in the
case of sensor failure, it will not be
possible to read the specified value
of resistance, nor voltage.
 Here is a hypothesis. Suppose
that the measurement shows accurate sensor resistance, but the voltage reading fails. Knowing that
induction voltage generates at the
time when tooth of the pulley arrives on the nose of the sensor, the
cause of problem may lie on the
toothed pulley or sensor bracket.
If there is dirt, which always has
metal particles, accumulated between the teeth on the pulley, volt-
 83
age induction will fail. The same
will happen if dirt is present on the
sensor. The irregular gap between
the sensor and the tooth on the
pulley will also be the cause of induction failure. It is not uncommon for a number of reasons that
this gap increases or decreases.
Therefore, if such irregularity is
noted, it is advisable to find specified gap distance value and make
correction. In the case that we
reach a satisfactory measurements
and error still exists, the problem
could be caused by oxidized contacts on the sensor connector terminals.
 When we are talking about CKP
sensor connector, it should be
mentioned that inductive sensor
can have three terminals, which
sometimes confuse technicians by
leading them to idea that they are
dealing with Hall sensor which always has three terminals. Inductive sensor has two terminals,
while the third is earth connected
to the protective mesh covering
around the two wires and annuls
foreign voltage interference. If we
look carefully wire connections, we
shall see that two wires are connected to the sensor and the third
one to the protective layer and the
third terminal of the connector
which is connected to the ground.
 Hall sensor has the power supply, earth and signal through the
connector, thus three active terminals. Unlike inductive CKP sensor,
Hall sensor output voltage will depend of the moment of the open
circuit. Thus, when testing this
type of sensor, it is primarily necessary to determine whether there
is a power supply (typically 5V) on
the sensor connector.
 Finally, we should not be surprised if we sometimes encounter
two CKP sensors, which manufacturer has provided to read several
crankshaft positions. In such cases,
the DTC will be marked with the
problem of sensor Bank 1 or 2, as
it was the case with O2 sensors.
84
 Turbocharger DTC problems
 As in previous cases, the DTC
associated with the turbine problem does not refer to its replacement. Suppose that we have a
DTC-P0234 with the definition
Turbo/Super Charger Overboost
Condition or PO299 Turbo/Super
Charger Underboost. The first definition talks about Turbine or Supercharger overcharging, and the
second abut the air undercharge.
 Worn out shaft bearings will
cause the fatal turbine defect. In
such case, we shall notice free play
when moving shaft left-right by
hand. Worn bearings will cause
leakage of engine oil, which lubricates the shaft under the pressure,
in the exhaust system. Of course,
the consequences will be enormous
oil consumption, and the blue
cloud of smoke from the exhaust.
Returning to the mentioned DTCs,
we can immediately suspect a malfunction of the turbine Bypass
valve which diverts exhaust gases
(see how Supercharger/Turbines
work in the Automobile electronics
& 4-stroke engines).
 The cause of insufficient turbine
charging can be carbon deposited
on both sides of the blades or turbines Bypass valve and its mechanism. Carbon deposit build up on
blades, housing and the turbine
inlet is caused by worn out engine
with excessive oil consumption and
large amount of oil vapour on the
engine vent. As the engine
breather hose is connected to the
turbine intake, the carbonized oil
vapour forms deposit inside the
turbine. Larger quantities of deposits can slow down the turbine,
and sometimes even partially or
completely disable its rotation. Another cause may be a partially
opened Bypass valve, in which case
the exhausts gases are not directed
to drive a turbine, but a certain
amount of gases go directly into
the exhaust system by passing the
turbine. Bypass valve malfunction
is usually associated with accumulated soot, which prevents in a
timely manner complete opening
or closing the flow of exhaust gases
to a turbine.
 Described problem with a Bypass
valve will be also the cause of first
DTC. If the valve does not, when
needed, diverts the exhaust gases
by the turbine, the turbine will
reach too high speed, and develop
excessive air pressure to the engine
intake system. If the problem does
not lie in accumulated soot, which
prevents proper operation of the
valve, we should look for potential
failure of mechanism which controls the valve. If we find the valve
mechanism in order, we should
look for the problem in the valve
actuator which can be operated by
vacuum or solenoid (like the principle the EGR valve).
 If we want to clean the carbon
deposits from the turbine and disengage Bypass valve mechanism, it
is advisable to use a liquid to dissolve carbon deposits and do not
attempt to disassemble the turbine,
as it will cause turbine imbalance.
Other parts of the mechanism as-
 85
sociated with the valve could be
disassembled if necessary. On following images we see the turbine
with vacuum operated Bypass
valve lever which is adjustable.
 When solving the second problem with insufficient turbine
charging, one should bear in mind
the possibility of Intercooler blockage due to the oil deposited from
the engine breather, and carbon
deposits on the walls of the cooler.
 Wideband O2 sensor with 5 wires
 So far we have mentioned the O2
sensor or lambda probe with 1-4
wires which works as electrochemical generators with the output generated voltage of 0.2-0.9V.
This type of sensor on the engine is
certainly of revolutionary importance for the correction of fuel-air
mixture. However, the signals received by the ECU simply consist
of information YES or O, or 1 or
0. Thus, the excess voltage generated from 0.45 V will give the information of high concentration of
carbon monoxide in the exhaust
gases, or too rich mixture. Voltage
below 0.45V will indicate the excess amount of oxygen in the exhaust gases, or too lean mixture.
By constant mixture adjustments,
the ECU will try to maintain the
ideal ratio, in which case we shall
have output voltage of about 0.45V
on the control probe. Striving for
the ideal engine operation, maximum efficiency and minimum fuel
consumption, manufacturers have
developed a new type of O2 sensor
that will signal the deviation of
fuel injected in each point of engine operation. A new generation
of O2 sensor, also known as the
Wideband sensor, is installed in almost all types of newer production
cars. The main difference between
this and the previous sensor is,
that in this case we have a power
supply to the sensor (depending on
model) 5V from ECU, instead of
generated voltage from the sensor
to the ECU. A significant difference was achieved in transmission
speed of information and the sensor operating temperature, which
is nearly doubled with the sensor
heater. Operating O2 sensor temperature ranged around 400 ° C
and now is about 800 ° C.
 As we said, unlike the standard
86
Lambda probe which generates a
higher or lower voltage, depending
on the mixture, Wideband sensor,
also called A/F (Air/Fuel) sensor,
will provide a voltage signal which
is precisely related to the air-fuel
ratio at the time of measurement.
The output voltage of the sensor
will be converted by an electronic
circuit in the sensor to variable
electrical signal which can flow in
two directions (positive or negative). Electrical signal proportionally increases in the positive direction as the mixture becomes
leaner. In the moment of
Stoichiometric ratio of fuel-air
mixture 14.7:1, which is also
known as the Lambda, the current
ceases to flow in either direction.
When the mixture becomes too
rich, the current changes direction
and flows in a negative direction.
 ECU supplies the sensor with
voltage of 2.6, 3.3 or 5V
(depending on the type of vehicle)
trough the two wires and monitors
the sensor output trough the two
other wires. The output signal of
the sensor is processed in the ECU
and can be read by diagnostic device as Air/Fuel ratio or as a voltage signal, what depends of the
type of device and programs we
use. If we read the probe signal in
voltage, value below specified voltage will indicate the rich mixture
and the values above specified will
indicate the lean mixture. Thus,
vice versa from the previous type
of sensor. In some cases, the ECU
will make a signal conversion, and
device will read the value in the
same way as it does on old type of
O2 sensor. This modification was
done due to the law which provides the reading of all values
related to ecology, with the OBD II
scanners. The operating principle
of this type of sensor is quite more
complex than the previous one, but
not so important to be completely
understandable by mechanics. So,
let's just say that only one cell of
sensor works in the same way as it
does on the older type, and the
other one on the principle of
2ernst Effect, or thermo-electric
effect which further processes the
amount of oxygen in the exhaust
gases and provides more precise
information. The most common
problems of this type of sensor are
associated with defective sensor
heating element without which the
sensor can not work even when
engine reaches the operating temperature. Finally, we should not be
surprised if we encounter a Wideband sensor with six-wires that has
the same function as the one with
 87
five. However, in the case of sensor
replacement, we shall certainly use
the appropriate one.
 Evaporative Emission Control
System (EVAP)
 The system which ventilates the
fuel vapors from the fuel tank may
give more headaches, if the DTC
turns out associated with it, than
solving some other more serious
problem.
 This system controls the fuel vapors in the fuel tank and prevents
them to escape in the atmosphere
as harmful gases formed by fuel.
ECU or PCM monitors the eventual failure of the system. If a defect is detected, the system turns
on the MIL (Check Engine). Failure of EVAP system can be caused
by a trivial omission i.e., insufficiently tightened tank cap. However, just by tightening the cap, we
will not get rid of the DTC and the
MIL. Engine computer does not
respond immediately to changes in
the system, but monitors the system for a while during the driving.
 The most common problems associated with EVAP system are
connected with the Purge Valve
malfunctioning. This valve allows
the fuel vapor to enter into the engine inlet manifold. Bad condition
of system hoses or faulty fuel tank
cap will also play a significant role
in DTC appearance. One of the
common codes encountered is
P0440, which warns us about a serious leak from the system. This
DTC is usually a result of a lost or
loose fuel tank cap, or serious
damage of the cap seal. The trouble codes P0443 and P0449 are
also common, and directing to the
malfunctioning of the Purge Valve.
Both errors are relatively easily
solved. In the first case, we shall
check the fuel tank cap and possible damages of the system hoses.
In the second case, we shall check
the Purge Valve and most probably
solve the problem.
The trouble code which we certainly do not want to see is labeled
P0442. This code indicates a very
small leakage from the system,
which is almost impossible to find
by visual inspection, as the hole is
no bigger than a pin head. In such
case, we will be forced to use, socalled, smoke machine. Every system has a connector for testing
88
purpose where is possible to attach
the stem hose from relatively simple apparatus and fill the system
with smoke under a low pressure.
Sometimes, such devices have the
UV colors and leakage can be detected with UV detector or simply
by following the appearance of
smoke on the hoses.
 EVAP system completely eliminates the harmful gases from the
fuel tank. Accumulated gases
stored in EVAP Vapor Canister will
be released into the engine intake
manifold through a Purge Valve.
The valve will open when engine
reaches operating temperature
and higher engine RPM when
gases will burn in the engine cylinders.
 So far, we could conclude that
the EVAP system is fully sealed
and there is no vent from the reservoir, except during the Purge
Valve opening when gases are let
to the engine. It is understandable
that in such circumstances vacuum
would be created in the fuel tank
after a certain amount of fuel is
consumed, and the fuel pump
would no longer be able to supply
the engine with fuel. The older
types of cars (pre-OBD II system)
had a tank cap with a spring valve
which opened due to the negative
pressure and let the air from the
atmosphere into the tank until
equalization of pressure was
achieved. In EVAP system, the
equalization of pressure is
achieved through the Vapor Canister and EVAP vent solenoid.
 So, let's go now trough the
EVAP system, from the fuel tank
to the engine. The reservoir is designed in a way that the upper part
has an additional space for expanded volume of fuel at higher
temperatures without fear of fuel
overflow in the EVAP system. Fuel
tank cap seals completely after
closing and has no vent. Vapors
from the tank do not go directly
into the system, but through the
separator Liquid-Vapor Separator,
which is located at the top of the
tank. Vapor enters the separator
and the fuel is dripping toward the
bottom of the separator and back
into the tank, while the vapor is
leaving trough the hose to the Vapor Canister. If we encounter a
problem that fuel overflows to the
canister, we can suspect the fuel
outflow blockage from the separa-
 89
tor in the fuel tank. The attached
sketch shows the one of the simple
separator, and one should not be
surprised if some other type of
separator is installed. In any case,
it always comes down to the same
principle. Separator allows the vapor flow towards the canister and
the fuel back into the tank.
 Vapor Canister is a plastic or
metal container, usually located
somewhere in the corner of engine
compartment. The interior of the
container is partially filled with
carbon material which acts like a
sponge and absorbs the vapor
from the fuel tank. During the fuel
evaporation while the vehicle is
stationary, the vapor is leaving the
fuel tank and remains in the canister until we start the engine and
reach the operating temperature,
when the Purge Valve opens and
the engine draws the gases in and
burn them in the engine cylinders.
 ECU will monitor the system
only if the amount of fuel in the
tank is between 15-85% of its capacity. The reason is simple. If we
have a full tank, evaporation will
be insignificant. If we have an
empty tank, empty space in the
tank will absorb the fuel vaporization.
 EVAP Vent Solenoid will allow
the entry of air into the system in
case of large negative pressure in
the fuel tank.
 ECU Flashing and Mapping
 And here we meet one more
phrase which is impossible to
translate in two words and make it
understandable. If we look in the
dictionary, we find several meanings for the word Flash. Each of
these meanings can be used depending of the sentence concept. In
our case, we should comprehend
what the author wanted to say
with this phrase. Thus, the ECU
Flashing could be explained as
quick going over the already installed program in the ECU with
the new one, which contains additional or revised information or
parameters. Sometimes this term
is equated with the term reprogramming. This, by no means, is
the same, and therefore we use the
term Flashing. When reprogramming, the memory is always formatted, all data is removed from it
and new program installed. When
we do Flashing, already installed
application is used, and with a new
program we are just changing certain settings by quick flashing
 Vapor Canister
90
through the existing program and
updating it with new data and corrected software errors. Because of
such procedure, term Flashing has
been used.
 ECU Flashing is not always
linked, as it is commonly thought,
by modifying the program to increase the power. The comparison
can be found in Windows programs. In an effort to launch the
software on the market as soon as
possible there is always possibility
of some oversights which are additionally corrected by certain upgrades or updates. So we had the
so-called Windows 98. Second Edition and Windows XP Service Pack
2, Pack 3, etc. which have been
used for programs corrections.
When we are talking about cars,
the situation is similar. A vehicle
leaves the factory with an installed
program, which after a few tens of
thousands kilometers, or other unforeseen driving circumstances
shows imperfect. Such imperfections are usually related to the
EGR valve, electronically controlled variable camshafts, etc.
amely, when automobile computer is programmed, the ideal
parameters are taken in consideration. These parameters change
during the various driving regime,
and due to the delays of engine actuators after a certain period. To
deal with these situations, the car
manufacturers are offering modified programs to flash the ECU.
This is mainly a simple procedure
through the designated interface.
Similar to the diagnosis, the program takes us through the Flashing process, and installs itself a
new or corrected program fragments in the ECU.
 Apart from described ECU
Flashing and correcting or repairing installed applications processed by the vehicle manufacturer,
Flashing can be done with purpose
to increase the engine power. Here
we have to know that manufacturer has pulled out the optimal
maximum power which will,
among other things, meet regulatory standards related to ecology.
Certainly, when the power was
calculated, the engine lifetime was
taken in consideration. It is not
unknown, that from any engine,
especially ones with Turbo or Super Charger, can be additionally
achieved 15-40% of power. Before
we proceed with such process, it
would be wise to ask ourselves why
the manufacturer did no do it.
Those who have been mastered the
principle of engine operation, will
be aware that the increase in engine power will overload its elements: pistons, bearings, clutch ...
Therefore, the conclusion is simple. Significantly increased engine
power, overloads the engine parts
more than it was foreseen, and we
can expect a very short engine lifetime. Furthermore, by changing
the parameters, we shall most
likely go beyond the allowable
emissions and therefore passing
any technical test will be very
doubtful. In other words, if we intend to increase the engine power
for more than ten percent, we
 91
must be aware that in addition to
modifying the software, we have to
do and the hardware too. This
means, that we have to consider
the cost of replacing a standard
piston with modified. It is not rare
case that the crankshaft connecting rods have to be replaced too. It
should be added the cost of a new
(stronger) clutch assembly and
modified oil and engine cooling
system. The modified exhaust
manifold with the entire exhaust
system which will allow the proper
flow of additional amount of exhaust gasses is also not a negligible
item. Other words, it is very expensive game. But this is not the
end of the investment. Other parts
on the vehicle are designed to resist the power of factory-built engine. After we boost the engine
power, we shall have to work on
the vehicle suspension and braking
system which will not be efficient
with new higher engine performances.
 Even if increasing the engine
power by modified software is not
recommended, let’s say a few
words about this procedure for
those who can not resist this challenge from pure enthusiasm, regardless of possible negative consequences. On the market we can
find several types of interfaces
with programs to increase engine
power. In addition to the interfaces and programs for a particular vehicle models, there are those
which cover a larger number of
car models. Commonly encountered ECU Flashing interfaces:
CMD Flash, Galletto, KWP 2000
Plus... If we are going into such
experiment, it would be advisable
to use programs already prepared
for specific vehicle. First what we
have to do is to check (usually indicated in the program), if there is a
possibility to save original program in our computer before we
go on with Flashing. This option
allows us to return the original
program in ECU, if for any reason
we are not satisfied with the new
version. If we go into the process
without being able to save the
original program, we will have to
contact official service to install
back the original program, and
pay for it.
 Flashing procedure with readymade software is fairly simple.
Connecting the interface is identical to the diagnostic device connection, and the program takes us
through the process. A more complex procedure is called Mapping,
whose name derives from the program map with a number of values
which can be changed. Unlike
Flashing with ready-made software, mapping is a more complex
procedure, and we should definitely not play with it, unless we do
not know exactly what we are doing. The most common result of
improperly performed mapping is
the rough engine running and the
whole bunch of problems in the
best case. Inability to start the engine after incompetently performed mapping is more than
common. But if we have saved the
original program in our computer,
92
we shall be always able to install it
back in the ECU.
 If we use the interface KWP
2000 Plus, its package includes the
program with listed types of automobiles on which the Flashing can
be done. Besides the program
where ECUs and vehicles are
listed, we shall get an additional
list of vehicles on CD. After each
type of vehicle on the list and the
specified ECU, we shall se remark
from which is visible whether is
possible to previously store the
original program or not. If there is
no possibility to save the original
program, it is advisable to quit
Flashing. If our car has been
found on the list with the possibility of saving the program, plug the
interface in the DLC, start the program and select the type of car
from the list. By starting the program, process of reading the
EEPROM chip in the ECU begins
(EEPROM explained in Automobile electronics & 4-stroke engines).
If we doubt the identity of the
specified ECU in the program and
the one in our car, in the next window we shall choose the option
IFO and wait for the program to
read a data from the ECU. After
scanning, in the following window
we shall see the data and type of
ECU in the vehicle. These data
should be stored in a separate
folder (yellow envelope icon in My
Documents) in the computer, so that we can install
it back if necessary. During
the various program phases,
we shall be warned to switch
the ignition on or off. After
we have saved original data,
we select our vehicle again,
open a prepared program
from offered option, and
check whether the type of
ECU in a new window is
identical with the one in
original program which we
have saved. If the numbers
are identical, we shall continue with programming. If
the numbers differ, we better give up, because the program is obviously intended
for some other ECU. After
installation is completed,
switch the ignition off, click
OK, wait for ten seconds
 93
and take the car for test. o matter what at a first glance it looks
very simple, before moving to the
described procedure, instructions
have to be studied thoroughly to
prevent any possible mistake. For
example, we can find the warning
that on some VAG vehicles instrument panel has to be disconnected
by removing the fuse, in order to
perform the ECU Flashing.
 At the end of this chapter, let's
take a look to one concrete example of flashing Mitsubishi and Subaru with a program made just for
them. As it is the case with the diagnostic tool intended for testing
only certain brands of cars, similar
situation is with Flashing programs and interfaces. Such programs provide far more options
than those which cover the entire
range of vehicles. In this case, besides the installation of existing
modified program, we have the
possibility of entering the values of
our own choice, or so called mapping.
 After starting the program, in
the window we can see the upload
of all necessary software tools for
Flashing. In the upper part of the
program we can find the options
icons used in the Flashing process.
With the Open ROM option we are
opening the program for ECU
Flashing. With the Save ROM as
option we can save the changes
which we might added in the program. With option Read from
ECU, we are entering into the
ECU and reading the existing program. By clicking on Write to ECU,
we are writing a new program in
ECU. Test Write to ECU allows us
to test the installation of new program. This procedure is identical
to the option Write to ECU with the
difference that the program is not
written into the engine computer,
but just the simulation. Compare to
ECU option compares the
ECU program with a program that we want to write
and installs the modified
data only.
 After connecting to the
vehicle, icon Read from ECU
glows. Clicking on the icon,
select from a provided list
the car model we want to
flash. By clicking on Read,
data starts transferring from
ECU to our computer. After
completion of transfer, we
have a complete data view on
94
the monitor. These are data and
the parameters which are installed
in the ECU and have to be saved.
Clicking on the Save ROM as select
a location on the disk, let’s say My
Documents, and save data by clicking on Save.
 Thus, as previously mentioned, the safest way is installation of modified ready-made
programs. Those who wish to
play with mapping by typing
their own chosen values will
have to study quite a lot of material in order to successfully
do the mapping. This article
will certainly be useful to those
who wish to experiment by using ready-made flashing programs. Those more ambitious
will have to work on further
education. Below on the left we
see the fuel map with fuel mixture values which can be adjusted at different engine
RPM. In every checkbox values are changed by simply procedure, moving them towards
the plus or minus. Similar
maps are used for ignition timing correction, opening and
closing turbo-charger’s bypass,
limitation of maximum RPM
and setting a number of others
 95
parameters.
 Immobilizer
 Here we have also an expression
which is derived from Latin word
Immobile. For those who are not
quite familiar with its meaning,
comparative words would be: motionless, immovable, stationary,
static etc. Thus, the term Immobilizer can be interpreted as a device
which disables
something to
move, or in our
case, disables engine to start.
 Early models of
immobilizers were
quite simple devices, which disabled engine to
start by cutting the electrical circuit on ignition coil or ignition
module, electric starter, fuel pump
etc. Today, these devices are far
more sophisticated and connected
with the ECU. As there are nowadays a number of different models
of immobilizers which are constantly being improved, in this
chapter, we shall describe the basic functioning of such devices in
today's automobiles. If we want to
deal with the problems associated with this system, it
will be often necessary to
use the literature of the car
that we work on. In any
case, as in the other car
components, it is necessary
to know the basic operating
principle, so that we are
able to start from somewhere. At
the beginning is important to note
that the immobilizer is not associated with the remote door locking
control, or with the remote alarm.
These facilities incorporated in the
ignition key are sometimes confusing, but immobilizer is always a
separate device. On the photograph we see the key with an electronic circuit for remote alarm
and central locking, and a special
section with a microchip linked
solely to the immobilizer. Immobilizer microchip is located in the
corner of the key housing, while
the rest of space is used to accommodate the electronic circuit for
the remote alarm and door locking.
 To begin with, let’s list the components of such a system, starting
with the ignition key which is
known to us with its mechanical
96
properties enabling us to unlock
the steering wheel lock and turning ignition switch on. On cars
with immobilizer, ignition key is
called a Transponder. This name is
a compound of two words:
TRA2Smitter and ResPO2DER.
Of course, these two words are not
originally written in this way, the
letters are highlighted for easy
identification of the compound.
Transmitter and Responder belong
to a group of electronic devices
which are communicating with radio frequency, or identifying by
technology RF-ID (Radio Frequency Identification). Since the
microchip embedded in the ignition key acts as Transmitter and
Responder, a term Transponder
was obviously the most suitable
name for this electronic circuit.
 Transponder is powered from
the induction coil in the ignition
lock (Antenna Coil) and does not
need batteries. It is not uncommon
that problem occurred in immobilizer is often associated with an
empty battery in the ignition key.
If the key has the ability to control
central locking and alarm, then it
needs battery to power the electronic circuit. In other words, by
removing the battery from the ignition key, we will not be able to
remotely lock and unlock the car
and turn on and off alarm, but we
will start the engine without any
problems. Transponder supplied
with the vehicle is also called Master key. The loss of the main key
causes extremely delicate situation,
which usually results with a considerable loss of time and financial
cost. For this reason, it is advisable
to make a copy of the Master key
and store the original key at home.
The process of copying, or programming the Master key is quite
simple. Programming instructions
are usually found in the owner’s
manual which is supplied with the
vehicle. If this manual is accidently
lost, the instructions can be found
in various auto data, or with little
effort on Internet. Of course, it is
necessary to obtain the original
key through an authorized dealer.
Such key comes mechanically
Coil
Modul
 97
processed for the lock of particular
vehicle. The basic program is also
installed in the microchip, but it
has to be encoded. On the other
hand, the market offers so-called
uncut or blank keys for certain
types of cars. Such keys are much
cheaper than original, but are they
reliable? Blank key can be mechanically cut by a sample of the
Master key in the workshops specialized in copying cars keys. After
mechanical treatment, the encoding procedure is the same as with
the original key already processed
by factory.
The coil on the steering lock powers Transponder by incorporating
both inductive coils (second coil is
placed in the transponder). The
primary coil on the ignition steering lock or, more
known as a Coil
antenna or Transceiver, exchanges
data by radio frequency between
the Transponder
and immobilizer
control module.
Antenna coil consists of copper coils and an integrated circuit, or microchip, which
creates a high frequency AC voltage, and communicates with a
transponder. Data exchange between the transponder and Coil
Antenna occurs when key is turned
in the lock. On some models, data
exchanges start as soon as key is
inserted into the lock.
 The indicator light on the instrument panel indicates the immobilizer activation and also warns of
possible errors. Activation of the
immobilizer is usually accompanied by even flashing, while the
eventual defect is manifested by
constant light or blink in intervals
which are also DTC codes. The
same indicator light can simultaneously alert about the functions
of certain alarm devices activations: the door lock... However, all
 Modul
 Radio signal
ECU Coil Two-way signal
98
devices which are connected to the
indicator light are not in connection with the immobilizer. A similar function of the signal lights we
meet in the cars where only one
light warns us about worn out
brakes, insufficient volume of
brake oil or disengaged handbrake.
 Unlike the older cars models, today's vehicles Immobilizers are
connected to the engine computer
(ECU or PCM). By activating Immobilizer after removing the key
from the steering wheel lock, the
ECU will (depending of the type of
vehicle) immobilize or disable: injectors, spark plugs, starter, fuel
valve on the diesel engine etc. The
Immobilizer module can be separate unit or integrated in the ECU.
 Well, let's see the process of Immobilizer deactivation: By inserting or turning the key in the lock,
begins the process of verification
or checking. Immobilizer module
sends a series of numbers over the
Coil Antenna to the Transponder.
Transponder returns the identification number to the module and
calculated response to the received
numbers. Electronic Transponder
chip supplies condenser with
power where an induced voltage is
stored. Module checks the received
identification code and compares it
with the registered number in its
memory, and also checks the calculated response. Once the module
finishes checking, it sends identifying information to the ECU where
it is compared with stored codes.
After comparison, the ECU sends
an identification code to the module where it s compared with a
code stored in the Immobilizer
module. After completion of
checking, the module returns an
identification code to the ECU. If
verification of identification has
passed successfully, the indicator
light turns off and the ECU deactivates all obstacles to start the engine.
 As we see in this very complex
system of protection, the ECU and
immobilizer are closely related.
Even so close related, that on large
number of today's cars it is not
possible to replace just the module
or ECU, but both. But even this is
not always the rule. In some car
models it is possible to change the
ECU and program the immobilizer
system in the ECU via the module
with the original (Master) key. The
only component which is not subject to programming is the Antenna coil, and can be replaced
without fear of unwanted consequences. As already mentioned, if
we want to solve the problem related to Immobilizer, and if it is not
of trivial nature, we will have to
study the manufacturer's literature and follow instructions. Successfully resolved or diagnosed
problem on the one type of vehicle,
does not guarantee success on another. As with a diagnosing the
fault on engine electronic system,
and here we can read the error by
decrypting the number of flashings
on the signal lights or by scanning
through the OBD II connector.
 Knowing that many small work-
 99
shops are using second-hand parts,
and what will happen in the future
too, here is an example of replacing a defective ECU with a secondhand one from another car. Knowing how the immobilizer works, we
shall certainly insist on buying
ECU which has a belonging immobilizer module and key or Transponder. To make our work easier
and reduce the costs, it is not necessary to buy a complete steering
lock. We can install other ECU
into the vehicle, attach the corresponding module to an existing
wiring and the existing coil antenna, and a microchip installed in
the key which we got with the
ECU, just switch with the one in
original car key. Thus, replaced
ECU will communicate with the
corresponding module and transponder microchip, saving us trouble to change the steering wheel
lock and key which usually opens
the car door and often activates
the car alarm.
 Let’s see one example of key programming without using an interface and program. Primarily we
have to check the possibility of
such programming. Information
about manually programming can
be found in the owner’s manual
which comes with the vehicle,
workshop books for a specific vehicle or other auto data. Described
procedure was found in the database and it is foreseen for coding
Mazda 6, 1.8, 2002-07. This procedure is used in case of Immobilizer
system malfunctioning and new
keys programming. The system
malfunctioning is manifested by
light flashing or constant light,
which may be due to a number of
causes. In other words, if there has
been confusion in communication
between the ECU, module and
Transponder for any reason, resulting with inability to deactivate
the Immobilizer, such a possibility
of manually resetting (if provided)
will be of great help to quickly resolve the problem. Certainly, we
are talking about software problems and not those related to
physical defect of one of the system
components.
 To carry on with such procedure
we need to have two originally
programmed keys obtained with
the vehicle. Each of these operations must be completed within
thirty seconds from the end of the
previous one. In the lock we insert
original key number 1 and switch
ignition on. Leave the light on the
instrument panel to light up for
three seconds, after which it turns
off. Within four seconds ignition
has to be turned off, and the key
number 1 removed from the lock.
Insert the original key number 2 in
the lock, switch ignition on and
repeat the previous procedure. If
we are programming new keys, the
process has to be repeated with
each key, bearing in mind that we
have to do it within thirty seconds
after the previous procedure is
completed. In this case we can program up to eight keys. Thus, before we ask someone for help to
program the keys with appropriate software and interface, it is ad-
100
visable to check the possibility of
manually programming.
 On cars with no possibility of
manually programming, appropriate interface and software has to
be used. Here we shall not describe
the key programming process with
help of interface and program.
There has been said quite a lot
about the use of interfaces and diagnostic programs. Working with
key coding programs is quite similar to the mode of diagnostic programs. Of course, before using the
program it is necessary to study
the instructions which come with
the program. Following the instructions, the program takes us
through the programming process.
As the programs are modified day
after day, we will find programs
on the market for certain types of
cars, and those universal covering
a number of vehicles. In addition,
these programs sometimes offer
significantly more options than
just encryption keys. On the left
photo we see the possibility of errors detection and cleaning, erasing the memory from ECU, entering new data, etc. In any
case, before we decide to
play around with some
Immo software options,
inevitably, should study
the instructions and warnings which guide us
through the program, because in most cases there is
no return after the program phases are wrongly
determined.
 Servicing technicians,
who are now or will be tomorrow, managers or
workshop owners have to
know something about dishonest, criminal actions
which are not uncommon
in workshops all over the
world. As it is more or less
well known, vehicles are
stolen today with the original key, instead by wiring
connections as seen on
movies. How we can conclude from this text, such
theft is absolutely impossi-
 101
ble for vehicles with integrated Immobilizer. However, it becomes
quite clear that if costumer leaves
the vehicle in the workshop with
the master key, there is enough
time to make a duplicate key from
the original. When we have a cut
key by original one, we see how
easy is to program it manually or
by interface and program. We can
only imagine the value of such duplicate key on the "market".
 Many will say that in addition to
owning a coded key is difficult to
jump over the activated alarm on
the vehicle. So, let’s say a few
words about it too. Organized
groups of cars thieves are
equipped today with very expensive hardware and software equipment. One of the easiest ways to
obtain the original key we just described. Another way is to decrypt
the code sent by Transponder with
a help of the laptop equipped with
Microreader-TV, which can catch
radio frequency from Transponder. One option to capture radio waves is sitting next to the
driver when starting the engine
and the other is by sitting next to
the car owner who has a car key
on the table or in a pocket. By
sending signals over a laptop, similar to the one via the coil antenna,
transponder sends back a response
to a laptop. Program in the laptop
identifies the code required by
module and ECU to deactivate immobilizer. When we have a code
saved in the laptop, the whole
thing becomes much simpler.
Steering lock is unlocked by existing mechanical key or by force,
and the laptop sends a signal to the
Immobilizer module. In the same
way the alarm radio frequency can
be caught, and even simpler than
Immobilizer. For communication
with the Transponder we should be
very close to the chip because its
broadcast distance is limited only
to twenty centimeters. Radiofrequency remote transmitter
which deactivates car alarm has
broadcasting distance considerably increased. It is enough to be
near the car to catch a signal
which will be deciphered in a laptop program. This information is
very useful to dealers and car owners, who will, knowing how the
codes are obtainable, pay attention
to unknown persons who are using
laptops in their close distance, particular in the vehicle. For that reason, it is quite understandable why
car manufacturers are putting so
great effort to add complexity of
codes which are emitted by radio
frequency. But as we see, for every
poison there is antidote.
 Additional protection from car
theft
 Knowing that there is a possibility to copy the key and obtain the
protective code from Immobilizer,
we often come into a situation that
we are asked to add more protection against the vehicle theft. Certainly, for this purpose a handful
of additional and expensive equipment can be found on the market,
which are again more or less based
102
on the remote control and are no
more reliable than those installed
by factory. Therefore, in this article we will describe the installation
of a simple but effective electromechanical theft protection system
which is conceptually designed by
the author of this book. Shown and
described solution certainly does
not have to be understood as a
revolutionary, because similar solutions can be often encountered in
vehicles. However, in addition to
existing solutions, it is distinguished by very good performance, effective design, simplicity
and cheapness. In addition to learn
in this chapter how to additionally
protect the car from theft, we shall
understand the role of the relay
with multiple terminals in a circuit. So let's start from the beginning.
 Today, the market offers a whole
range of gadgets and devices for
additional protection against the
vehicle theft. These products are
designed for older vehicles which
have not factory-built protection,
and new models with built-in protection.
 It is well known that cars and
motorcycles are stolen today regardless of coded keys and alarms.
Such theft is never violent, but
very sophisticated. Codes are intercepted by electronic devices,
followed by starting engine with
already prepared key. We have to
be aware of fact that Crime is a
craft, and theft rarely occurs spontaneously, by the way, or by using
a suitable opportunity. Thieves are
learning fast with great effort and
are usually well organized into
small groups, where everyone performs his job. One of the tasks of
such groups is to make contact
with employees subject to criminal
activities employed in the car services, car washes, hotels, car
parks, etc. (statistical data). In
these places, car owner leaves the
car keys, and often remote device
or a code for alarm deactivation.
In other words, everything one
 103
needs to make a key print (let’s say
in clay) and decrypt electronic
protection. ext step is quite easy,
knowing where the owner leaves
his vehicle, one of the group members comes with prepared key and
code deactivating device, and without fear or difficulties drives the
vehicle away. For this reason, additional protections are offered to
lock wheels, gearbox, block the engine, etc. One of the reasons why
the owners do not use extra protection from theft is a price of such
devices. Therefore, this article provides instructions for making a
very effective additional protection, whose price does not exceed
fifty dollars and does not take
more than couple hours of work.
Hereinafter, with described protection system against the theft is
possible to deactivate any engine
component which is powered by
current when starting the engine.
These components include: coils,
relays electric starter, electric fuel
pump, solenoid fuel valve on diesel
engines, etc. By breaking the circuit on one of these elements, engine start is disabled, while all
other lights and instrument panel
remain in function. Thus, regardless of the possession of original
key and alarm deactivator, engine
starting is disabled. The same applies to vehicles without alarm
when attempted to be violently stolen by breaking the steering lock
or bridging ignition wires. By removing the steering lock barrier
and bridging ignition wires, the
engine will not start. One might
ask, why such idea if so ingenious,
is not already on the market, and
whether this additional protection
can be deactivated, knowing that
we are dealing with professional
thieves. othing is impossible, not
even disabling this protection.
However, how demanding is such
work for thieves?
 First, to activate this additional
protection we shall install an electric lock which is used on cash registers in shops, cafes... This lock
has a cylindrical key which is difficult to copy. In addition, if we
leave the vehicle at the above mentioned places, we are leaving protection deactivated, and there is no
need to leave its key with the vehicle. So, if the master key has been
copied as well as alarm code, there
is no chance to copy cylinder key
of installed additional protection.
Again the question: can this additional lock be destroyed the same
as the ignition lock. Well, it will be
a problem without serious tools.
Cylindrical key does not provide
the ability of inserting special tools
and violently turning the lock or
pulling out the lock cartridge. If
we have installed the lock on the
hard metal of the instrument panel
or the central console, any attempt
of demolishing it, will be unsuccessful. The forehead of the lock in
which the key is inserted, is very
slightly convex and can not be
gripped by pliers or any other
similar tools. If the back of the
lock is reinforced with wide
washer before the nut which secures the lock, there is no possibil-
104
ity of violently pulling or levering
it out. The only option to deactivate the system is approaching the
lock from the rear side and connecting wires. But, we shall certainly take this option into account
when installing the lock. With a
little more effort, we shall find
very inaccessible place on the inner side of the instrument panel or
central console. When installing
the lock, we shall partially disassemble the central console or instrument panel to secure the lock
from inner side. This means that
thief should do the same job to get
hold of the rear side of the electric
lock. Conclusion: giving up the
idea of stealing.
 On the shown diagram we see a
way of connecting additional protection. In this case we are breaking the circuit on the ignition coil,
but in the same way we connect
positive wire with any other electrical element. Having broken the
original circuit which activates an
engine actuator, we have disabled
its function. Activation and deactivation of connected element will be
controlled by a locked or unlocked
position of electric locks. So, let's
start the installation process.
 The electric lock can be purchased in electrical shops. The
same is used in the cash drawers in
the shops, restaurants, etc. When
purchasing the lock, one should
take into account that the key can
be taken out in both positions,
locked and unlocked. In fact, on
some locks, the key can be removed only in locked position.
Price of the lock is about ten dollars. After appropriate lock is
found, we shall visit the shop with
bolts and nuts and buy a washer
with 19 mm bore which is the diameter of the lock. This washer
will additionally secure the lock
from violent extracting from the
bore.
 On the instrument panel or central console, we shall find a place
to accommodate the electric lock
which will be inaccessible from the
rear side. At this position we shall
drill the 19 mm hole, insert the
lock in it, reinforce it with washer
and tighten the nut.
 In the auto parts store we shall
look for 30 amps five terminals
relay. We have to make sure that
terminals are labelled with 30, 85,
86, 87 and 87A, as there are identical relays with markings 87 twice
(without A). Relay price ranges
from 5 to 10 dollars. It is advisable
to buy a more expensive relay
from reputable manufacturer, be-
 105
cause this cheaper alternative does
not meet the specified strength and
cause problems, especially if we
use it on stronger power consumer. Usually there is a possibility of buying a relay with housing
which can be attached to the car
body by screw. Such relay will be
the most suitable for installation.
Those who do not want to install
the warning light can use the relay
with 4 terminals, 30, 85, 86 and 87.
The fifth terminal is used for
warning light when the system is
activated. If the car already has a
built-in alarm indicator light, we
shall use four 4 terminal relay and
ignore connecting the lamp shown
on the sketch. The relay can be attached to the car body under the
instrument panel, central console
or inside the engine compartment.
If we are going to install the warning light, we have to look for LE
diode 12 V in the store with electronic goods. Illuminated part of
the LED is typically 5-6 millimeters in diameter. At a suitable
place on the instrument panel will
shall drill the appropriate hole and
insert the LED from inner side.
Prior to insertion, couple drops of
glue have to be put on the LED
rim to be fixed in the bore.
 When buying relays and LED,
we shall ask for fuse with housing
with value of 10-20 amps depend-
106
Ing of consumer which is powered
by electricity. In any case, we can
not go wrong if we use a stronger
fuse. The photo shows two types of
fuses. The first one is round with
glass or ceramic fuse, while the
other one has a housing to accept
the standard fuse used in today’s
cars. If we have to choose between
these two, preferable would be the
second one which, when burned,
can be found in vehicle spare bulbs
set, or in the nearest gas station.
 Of course, we should not forget
to obtain sufficient quantity of
wires, which is sold by meter.
Length of needed wire, we can
roughly calculate, if we determined elements position of the entire assembly. In the sketch we can
see two thicknesses of wires that
should be taken into account. For
thicker wire, we can use quadrature of 2 mm, and 1 mm for the
thinner. To make proper connection, we shall also need wire terminals and insulating tape.
 ow, when we have obtained all
necessary material, we can start
connecting components. Let's start
with the relay. Placing it somewhere under the hood or under the
instrument panel, and securing it
somewhere with the screw, we can
spread wiring towards other components, starting with terminal 30
on the relay. To this terminal we
are connecting constant power,
from battery or fuse box. For this
connection we shall use thicker red
wire to which we connect the fuse
in serial circuit. When pulling out
the power from fuse box, we
should make sure that we have
chosen source with constant
power. This means, that the wire is
live when the ignition is switched
completely off. Terminal 30 and
85, we shall bridge with thinner
red wire. Terminal 87A, we shall
connect with positive LED terminal using thin red wire. On the
drawing we can notice shorter and
longer LED terminals. Longer
wire is always a positive terminal
on LE diode. So keep in mind
when shortening the contacts to
remember which wire is positive
terminal. Thus, the red thin wire
from 87A is connected to LED
positive terminal. Thin black wire
connects diode ground terminal
and vehicle ground (any metal
part of the body). We are continuing with the thick red wire from
terminal 87 to the engine component which we supply with power,
in this case, ignition coil positive
terminal.
 ow we have to connect the electric lock. With thinner black wire
we are connecting one terminal to
 107
the ground and the other to the
relay terminal 86. If we have properly connected sketched circuit,
theft protection system must work.
Positioning the key to the locked
position, the LED will illuminate
or blink (depending on the type of
diode) and the thicker red wire
which is connected to the coil will
have no power and ignition is disabled. Positioning the key to
unlock position, LED will turn off
and the coil wire will be energized
enabling engine to start. Do not
pay much attention to locked or
unlocked position of the electric
lock, as it depends of lock purpose,
in our case this is irrelevant, one
position is on and the other is off.
How the system works? The relay
diagram shows terminal 30, to
which we have brought a constant
power, connected with terminal
87A when electric lock is turned
off. Thus, current flows undisturbed from terminal 30 to terminal 87A and to the LED positive
terminal, whose negative wire is
connected to the ground. The circuit is closed and LED illuminates.
At the same time, inactivated relay
does not connect terminals 30 and
87, which supplies with power
electric consumer (here we have
coil) and engine start is disabled.
 Turning the key in the opposite
position, we have brought the
negative pole from the lock to the
relay terminal 86 and closed the
circuit between the terminals 85-
86 and activated relay solenoid.
Electromagnet core is attracted,
contacts 30-87A are disconnected
and contacts 30-87 are connected.
In this position the circuit is interrupted and LED turns off. Circuit
between terminals 30-87 is closed
and the ignition coil is energized.
 Concept, design and sketches
by R. Marin.
108
 Radio decoding
 Default radio encoding in the vehicles was introduced in order to
protect them from theft. The assumption that radios are unusable
without a valid code should discourage thieves. Radio sets are
mostly blocked immediately after
the interruption of power circuit,
and on some models with short delay. amely, interrupted power
indicates that radio is removed
from the car. If it is removed by
the owner or service, there will be
no problem about entering code
after re-installation. Code usually
consists of four digits which are
written in the owner’s hand book
or in documentation of purchased
radio.
 It often happens that owner loses
the code with the time. The problem appears when replacing the
battery or disconnecting it for
various reasons. Such a situation
requires contacting the car or radio manufacturer to obtain needed
code. After the owner’s particulars
are checked up, the code will be
given to the vehicle owner. When
we say verification of ownership, it
means checking up information
about the owner or a radio, if
separately purchased, the vehicle
identification number or VI2 and
radio serial number. This procedure is usually simple, but sometimes gets awkward. Therefore, in
this section we shall briefly describe radio decoding procedure,
which works on most radios.
 Decoding code applies only to
specific radio. So, to get the code,
we have to know the serial number, and sometimes the model of
apparatus. Here the whole thing
becomes a bit complicated, because we need to draw out the radio from its position in order to
read the numbers from the label
on its chassis. If the label is accidently snatched, on most radios
the serial number is engraved on
the radio chassis. In today's car
looks almost impossible to remove
the radios from the dashboard as
there are no screws, and the whole
assembly looks like it was cast
from a single piece. Therefore, before we get busy, it is recommended to study the principle of
radio extraction, and, if accessible,
 109
use the drawings from the manual.
Such procedure is quite simple,
but it has to be known. We shall
also need some simple tools
which can be self made.
 Before we start extracting
the radio in order to read
the serial number, it is recommended to go trough the
possible available literature
(sometimes found in the vehicle) to find the possible
availability of serial number
through the radio display.
In the lower photo we see
the radio installed in Ford
vehicle which does not have
to be removed. In the vehicle handbook we shall find
the instructions which say:
switch on the radio, hold
down the button number 6
and press the button number 2. After that, the radio
serial number should appear on the display.
 When we write down the
numbers from extracted radio, we can return the radio
to its place and go on finding the activation code. As it
was the case before, for each
procedure on an electronic
system of the car, we need
programs, and often the
Internet. If we do not have a
program for radio decoding,
it can be often found on the
Internet. By typing the term
Car Radio Decoding, we can
find dozens of sites which
offer online decoding by the
serial number (immediately
returning the code after entering
and submitting the serial number).
Certainly, such a service has to be
110
paid about ten dollars by credit
card. However, if we type the term
Car Radio Decoder free download,
with a little effort and will, we
shall find this option too. Why
with the little effort? Because the
Internet offers so much for free.
But when we come to the
downloading procedure, there is
only possibility to download demo
versions, while the full version has
to be paid. Even this is not a bad
option if it is a good program
which we shall frequently use, and
charge our services. However, as I
said, those with little more patients
will find Freeware programs. One
such program is shown in the following decoding procedure.
 So, as we see in the program
photo, the process is very simple.
In this case we have chosen the
brand of Becker radios, and in the
newly opened window we type the
radio serial number. When clicked
on Calculate the program prints
out the radio activation code.
Sometimes, we will have to repeat
the procedure because of incorrect
calculations or more codes which
can be calculated by program regarding entered serial number, but
it just takes few more minutes of
work.
 In the next example we see the
selection of radios selected by the
brand of vehicle (in this case Daewoo) where the procedure is also
simple. But in the following example, Ford calculator, we are offered
several options. In the first option
we are asked for Ford code from
PCB or Printed Circuit Board. This
seven-digit number is printed on
the main board inside radio, or we
enter a serial number of the circuit
board. Once we enter the numbers, click Calculate and radio activation code appears. In the second option we are asked for Ford's
serial number with the prefix, or
the letter before the numbers, and
calculating the code with three or
four digits. Thus, if we do not
know exactly what we are doing,
we will play around with all three
combinations. Of course, first with
the simpler ones if we do not have
Ford's serial number.
 ow when we have an activation code, it has to be
entered to the radio. If we
do not have any instructions
and this seemingly simple
operation can give a good
deal of trouble. In fact, just
writing the code is not a
problem, because the numbers are entered by using
the numbered buttons on a
radio which are also used
for direct selection of radio
 111
programs. However, each radio
has a specific procedure for entering codes depending on the model
and year of the car production, if
the radio is factory-installed. To se
how it is done, let’s describe two
examples of entering the
codes in VW cars of different
ages.
 In the first example, according to the instructions, radio
has to be turned on. The display shows the mark SAFE.
After three seconds, the mark
is replaced by a numerical
designation 0001. Typing the
buttons from 1-4, for direct
radio program selection, write
a four-digit code which we got
from program calculator. After entering the code, press the
right side of the button SEEK
for two seconds until the audio
signal is heard. If we have entered the wrong code by any
chance, display will shows the
mark SAFE again, and procedure has to be repeated. After
two wrong codes entering, we
will have to wait at least for an
hour before we go again with
the procedure.
 In the second example, turn
on the radio and observe the
display label SAFE. Press the
MODE and SCA2 button until
the numerical designation
0001 shows. Enter the code as
previously described, and
again press the MODE and
SCA2 buttons until you hear
the audio signal.
 As we see from these examples, even when we have the radio
activation code, it is not so simply
to enter it without a valid instruction. However, in the lack of instructions used by the car owner,
which is usually found somewhere
112
in the gloves compartment, we
shall find them, with a little effort,
on the Internet.
 Car parking sensor system
 Today, we are witnessing increasingly complex car enhancements in order to maximize driving safety. One such device is a
sensor system and corresponding
ECM for safe car parking. The
sensors are usually mounted on the
rear of the vehicle, and it is not uncommon, to find them placed on
the front of the vehicle too.
 Ultrasonic sensors are commonly
embedded in the cars bumpers and
emitting high frequency sounds
inaudible for the human ear.
When sound struck the barrier it
bounces back creating an echo
which the same sensor receives
back. Knowing the speed of sound
value, computer, or module of this
assembly will calculate the distance between the sensor and the
object which vehicle approaches.
As vehicle approaches the object
behind or in front, the return of
high frequency sound will be
faster, it also means a shorter distance. As the width of ultrasound
waves is rather limited, the
bumper is mounted with up to
four sensors to cover all angles of
the vehicle. Depending of the embedded system, method of alerting
the distance barriers is different.
On most vehicles the warning is
audible with different intensity of
sound which increases as we approaching the obstacle. On some
more expensive models displays
are build by which we can track
distance in meters from the obstacle. In very luxurious car models,
beside sensors the cameras are
built-in through which we monitor
the video projection of the situation behind the vehicle.
Someone will say that
cameras are luxury considering that there are
already sensors which
warn us about the obstacle. But, like everything
else and these sensors
have disadvantages. Ultrasound will ricochet
back toward the sensor,
if we approach more or
less vertical and flat surRiverse
 light
Sensors ECM
 Display
 113
face. But in the case of conical surfaces, protrusions, etc. the sound
will be bounced in another direction and the sensor will not detect
it. This means that camera system
will be highly reliable on the parking, where we are approaching another car or the wall.
 However, besides relying on the
sensors when parking in various
yards and similar places, it is very
recommendable to turn the head
back and record the area behind
the car. Furthermore, even in ideal
parking situations, it is not advisable to rely exclusively on sensors.
The speed of sound varies with different weather conditions. The
parking system computer or ECM
calculates the distance by the return speed of ultrasonic waves
which are defined by speed of
sound determined at sea level at a
temperature of 21°C. This means
that measurements may vary by
inches, depending on conditions.
For this reason, most of these systems will warn the driver, usually
by continuous and amplified audio
signal to a maximum closeness to
the obstacle, which usually means
about twenty inches of space between the vehicle and obstacles.
 In addition to ultrasonic sensors,
and electromagnetic sensors are
used. These sensors produce a
magnetic field behind the vehicle
controlled by the ECM. Driving
backward and encountering an
obstacle, there will be a distortion
of the magnetic field. Based on the
data of distorted magnetic field,
the ECM will calculate the distance
from the vehicle barriers. In electromagnetic sensors, measurements are more accurate than ultrasound, and the critical distance
can be reduced to ten inches, and
even less. Besides being more accurate in measuring, electromagnetic
sensors will detect any obstacle behind the vehicle, regardless of obBat
Sonar
Ultrasound
Sensors
 ECM
Rear view mirror with display
 Ultrazvučni senzori
114
ject’s form.
 When activating the parking system by selecting the gear lever to
reverse position, ultrasonic sensors
will warn us constantly about the
distance from obstacles, no matter
whether we are in motion or not
Activated sensors continuously
transmit waves and ECM calculates the distance from obstacles
measuring the speed of waves returning to the sensors. This will
not be the case in electromagnetic
sensors. If we stop driving in reverse, this type of sensor will stop
warning us of an obstacle. The moment when the vehicle has
stopped, the magnetic field becomes steady with no changes. As
soon as we start moving again,
magnetic field becomes disturbed
and signalling starts again.
 To install ultrasonic sensors, we
will have to drill four holes in the
bumper and insert sensors in them
in a way that the surface of the
sensor heads, which are emitting
and receiving ultrasonic signals,
are visible. The sensors are usually
positioned on each
side of the bumper
and two on the
middle section, in
order to cover all
angles of the rear
side of the vehicle.
Electromagnetic
sensor, or sensors,
may be placed on
the inner side of the
bumper and do not
have to be visible. Both types of
sensors are connected to the ECM
which processes the received data.
Processed data can have output as
an audible warning signal of the
distance between car and barriers,
or sent to the display on the instrument panel transformed to the
numbers which define the distance.
 As a separate unit, the ECM
must have the power supply and
ground. Wire which activates a
system is usually connected to the
vehicle tail light where reverse
light is positioned too. Selecting
gear lever in reverse, we have activated reverse light and thus automatically the system parking
ECM.
 As well as the newer types of
cars already come with built-in
parking systems, the same can also
be retrofitted. With a set which
contains the sensors, ECM and cables, we usually get a special drill
bit to drill the appropriate holes in
the bumper, and the wiring diagram. If we purchase a more expensive installation set, in most
cases we are supplied with display
 Electromagnetic sensor taped across the
inner side of the bumper.
 115
which works on the Bluetooth principle (wirelessly). Installation is
fairly simple. We have to drill the
holes in the positions sketched on
supplied instructions, install the
sensors in them and place the
ECM set somewhere inside the car
at the rear end. Connect the sensors with module to which we have
previously brought the power and
ground, and system activation wire
to the reverse light. If we are installing electromagnetic sensor system, even drilling is not required
because it usually sticks to the inner side of the bumper. Briefly described installation relates to the
universal parking sensor kits. If
we want to use already provided
wiring for parking system installation, we shall look for a set already
designed for installation in a particular type of vehicle. We also
need to know that the electromagnetic sensor, which is usually supplied as tape, will not work glued
to a metal bumper. It will also be a
problem with drilling holes for the
ultrasonic sensors on the metal
bumper. Today, the metal bumpers are rarity, but they can be
found on some car models, so it
had to be mentioned.
 What to say about diagnosing
the possible failure on parking system. If it is a factory-built system,
errors can be read by diagnostic
device. If it is subsequently embedded system, fault diagnosis will depend of the system class or category. Cheaper units just do not
provide the possibility of diagnosis.
In such cases we will try to find the
fault by checking the power, system activation over the reverse
light and checking the sensors with
multimeter. With more expensive
kits we usually get calibration and
fault diagnosing program which
usually communicates with our
laptop wirelessly. amely, these
devices have the ability to be calibrated after installation. Calibration refers to the value of the sensors readings and those shown on
the display and the possibility to
determine the critical points when
approaching an obstacle.
 At the photo below, we see the
one of better parking units. In addition to the sensor, this device is
supplied with the camera which is
installed on the rear of the car and
rear view mirror which is also the
monitor. The connection between
the monitor and the ECM establishes on the principle of Bluetooth.
As we see, the set includes needed
drills too.
116
 Control Module or ECM repair
 One of the frequent questions
asked today by a car technicians,
hobbyists and enthusiasts is:
whether is possible and how to fix
the engine control module ECU/
PCM or ECM of ABS, SRS, air
conditioners, etc.
 As already mentioned in this,
and in previous book, it is primarily necessary to determine whether
the problem is related to a possible
malfunction of the control module
or some other electronic element.
We know that the definition of
DTC is never specific, but shows
the possibility of problems related
to sensors, actuators, connectors,
wiring and finally the possibility of
ECM malfunctioning.
 Therefore, let's mention one example from the practice which
gave a lot of headaches to mechanics. On the VW Golf 1.4 from 2005
the DTC appeared related to a
problem with the MAP sensor. It
was quickly moved to solving the
problem by replacing the sensor
and believing that problem will be
solved. Such action often results
with the elimination of failure. But
what if not, as it was the case here.
The sensor was replaced, but the
MIL was still on, and the same
DTC showed up again. After a
brief consultation, the team concluded that a problem lies in faulty
ECU which has to be replaced by
new one. Knowing that this is not a
small investment, the team decides
to ask for help. Advice was similar
to those described repeatedly in
this book, and earlier release Automobile electronics & 4-stroke engines. If we know how the MAP
sensor works, we can do some
checking before we decide to replace the ECU. First, we should
check if there is a power supply on
sensor from ECU. If there is a
power supply, what is the output
voltage from the sensor at different engine RPM. If we have obtained adequate values by measuring, we are suppose to check if
these values are coming to the
multi pin terminal connector on
the ECU. Only when convinced
that the ECU receives a valid signal from the MAP sensor, we can
conclude that we are dealing with
malfunctioning ECU. Of course,
before we do anything else, we
have to check the ground connection of the ECU. In described case,
the problem was lying in the sensor power supply. By using a voltmeter, conclusion was made, that
there is no power supply on sensor
connector. It is still not a reason to
question the validity of the ECU.
Voltage was also measured at the
ECU terminal which supplies the
sensor with power. When than a
surprise, the team which had quite
difficulties with this problem,
measured the output voltage of 5V
on ECU terminal which supplies
the MAP sensor with power. At the
beginning, a very complex problem suddenly becomes simple. If
there is voltage at the module terminal, there must be on a sensor
too. A wiring check up showed the
damaged wire which was causing
 117
the problem. In addition to damaged wires, the problem could lie
in the oxidized terminals in the
multi pin connector or in the sensors connector.
 Here we have quite clear message. To be able to solve the problem, we have to know how the sensors or actuators work. If we have
mastered theoretical principles of
the MAP sensor, we know that the
sensor is supplied with voltage of
5V, and output voltage from the
sensor has a value of 0.5-5V, depending of air pressure. But how
do we find the appropriate terminal on the ECU? The one of the
ways is to follow the coloured
wires from the sensor to multi pin
connector on the ECU. This
method is sometimes impossible.
Therefore, we will have to obtain
an electronic management diagram for the vehicle we work on.
As with other specifications, the
scheme will be found in the workshop manual or in one of previously mentioned car data bases. In
the upper diagram we see a schematic view of electronic management of our VW Golf, which will
 be of significant help in verifications. First, we see that IAT sensor
is integrated in the MAP sensor
and connected to the same connector. Blueprint will help us to find
out which wire colour belongs to
which sensor. On the right
enlarged sketch, we see the terminals numbers of each of these two
sensors.
 If after performing the necessary
checks on the wiring and sensors
we still come to the conclusion that
the ECU is faulty, what to do. As
we can conclude from the previous
texts, the ECU is a very complex
set of hardware and software. Engaging in its repair requires quite
a knowledge and equipment. Still,
not everything is so black. If the
ECU has not been produced so
that it can not be opened and its
interior completely covered with
liquid rubber compound, there is a
possibility to observe individual
electronic element within it and
check its possible faultiness. In this
case we will have to obtain a diagram which will help us in locating
the sectors within the module. Returning to the previous case of the
MAP
IAT
ECU
118
MAP sensor, assuming that we had
no power on the ECU terminal, we
shall focus on sector within the
module guided by the location of
terminal on ECU multi pin socket
connector.
 In the above picture we see the
ECU roughly divided into sectors.
Processor and memory are located
in one half, while the other half is
divided to the sector of incoming
information obtained from the
sensors Input, and the sector of
outgoing information which ECU
sends to the actuators Output.
Problems associated with the processor and memory we will not be
able to detect, nor repair it. However, the most common
causes of problems in the
ECU are related to the
malfunction of individual
resistors, capacitors and
transistors which we also
call relays. If we open the
ECU by separating the
upper and lower protective cover, usually secured
with only four screws, we
have a very clear view of
all electronic elements
which are soldered on the
printed circuit. We shall carefully
examine entire ECU in order to
spot any irregularity visible by
eye. We can often see charred elements or printed circuit. Knowing
that we have a problem with the
MAP sensor power supply, we
shall focus on that sector following
the lines which are connected to
the sensor power supply terminal
on the multi pin connector. Those
more experienced will measure the
values of resistors, capacitors and
transistors in the sector. If we encounter by measuring faulty element, we shall replace it with a
new one. If the marks on the defective element are not destroyed,
there should not be a problem to
obtain a replacement part.
 Faulty elements, in most cases,
are spotted by visual inspection.
On the next photo we see the leaking capacitor whose electrolyte destroyed the printed circuit below
it. Replacing such a faulty capacitor usually solves the problem. But
what if the printed circuit is destroyed? Those a little more skilled
 119
with a soldering gun will bridge
the damaged printed circuit with a
wire and solve the problem. ext
photo shows the transistor which is
formally destroyed. With a bit of
luck, just by replacing transistor,
in this case we have solved seemingly quite a serious problem.
 In the following situation the
ECU problem was solved on the
vehicle with V8 engine, whose new
ECU costs quite a lot. The problem
was the lack of spark on the one of
the engine cylinders. By checking
the ignition coil on that cylinder as
well as wiring, it was concluded
that problem lies in the ECU. Fortunately for car owner, the module
has been designed to be disassembled if needed, and thus
an insight into the situation within it. Each ignition coil has a transistor
or a relay inside the
module. By visual inspection, it was obvious
that one of the eight
transistors is burned.
By replacing transistor,
the problem was solved.
The photo was taken after
the transistor replacement,
so the picture we see shows
a situation with the new
transistor labelled with arrow. But if we take look at
the plastic lid which covers
transistors, we can notice a
trace of brown colour on
the fourth position which
has left burned transistor. I
believe that these examples
show the possibilities to
deal with problems of faulty modules. Other failures of control
modules can be solved only by specialized companies. If the failure is
not related to the mentioned peripheral elements within the module, one should have very serious
equipment, software and databases in order to test the module.
Among other instruments, it is essential to have the simulator to
simulate the signals which ECU
receives from sensors and instruments to register the signals sent
towards the actuators. It is quite
obvious that values and programs
are not the same for all vehicles,
thereby making the job even more
difficult. The next photo shows one
120
of the devices used when the control module has to be repaired.
 Being aware of extraordinary
complexity of modern technology
in today’s and tomorrow’s cars, it
is understandable that it is impossible to expect from the car services completely mastering all professions involved. However, in order to be able to solve the problems related to maintenance and
repair of modern cars, at least
what we can do is to be familiar
with the basic new technology.
 In this chapter we saw the possibility of solving some problems related to vehicle control modules.
Described examples are seemingly
simple, because we found problems by visual inspection and repaired them. In these cases we had
lucky circumstances to spot the
capacitor and transistor faults
visually. But this is not always the
case. Control module failures are
usually caused by disorder of software, which is usually solved by
Flashing. Problems are very rarely
associated with processor or memory failure, and if so, these modules will probably have to be replaced. The most frequent problems, as described, are associated
with the ECM electronic peripheral elements. Knowing how complex is module structure, we will
not go further in details studying
them and explaining schematically. For the failures that we can
repair in the control module, the
basic knowledge of electronics is
quite sufficient. Thus, as it has
been partially described in the
book Automobile electronics & 4-
stroke engines, in simple terms,
processor activates transistors located inside the module and transistors are activating actuators.
Transistors in a circuit are using
resistors and capacitors. Defect in
any of these elements will cause a
failure of particular sector. Malfunction of electronic elements
may not be visible. Therefore, if
we suspect the faultiness of particular sector in the module, we
will have to test the elements in
this part of the printed circuit.
Therefore we will concentrate on
the purpose of mentioned electronic elements and principle of
testing them, as they are usually
the cause of failure.
 Transistor testing
 Here we shall say a few words
about the basic principle of transistor functions, as they are commonly present in the automobile
modules. Transistor, or even called
the relay, is working on a similar
principle as already described
 121
electrical relay. It is used for two
basic purposes, as a switch or amplifier. In automobile modules it is
mainly used as an electronic switch
or relay. We will not go into the
transistor material structure but
only in its working principle. On
the first picture we see several
types of transistors which vary in
their strength. Transistors with a
greater flow capacity of electricity
are subject to larger scale of
warming and are usually attached
by a screw to the cooler. We will
mention only two types of transistors that are the most common,
2P2 and P2P or 2egativePositive-2egative and Positive2egative-Positive. The difference
between these two types of transistors is in the opposite direction of
the circuit.
 Transistor is made up of three
parts connected to each other, and
we call them: E Emitter, B Base
and C Collector. In some diagrams
these marks are also known as:
Source, Gate and Drain. On 2P2
transistor, current comes to E terminal and leaves from C terminal.
When transistor is switched off, its
central part, or B Base, functions
as an insulator and the circuit is
interrupted. On 2P2 transistor
symbol we see diode (arrow) on
Emitter. It means that current can
only flow in one direction, from
the Emitter to the Collector. On
P2P transistor, the situation is reversed. When voltage comes at B,
the current flows between the
Emitter and Collector. If we use
transistor just as a switch or relay,
the voltage at terminal B will be
defined by a constant value. If we
want to leak lower or higher current value trough the transistor, it
will be regulated by lower or
higher voltage at the B terminal.
In other words, with the higher
voltage on B terminal, more current flows between terminals E
and C. Thus, the ability of the
transistor is a possibility to leak
greater amount of current
(depends of transistor capacity)
between terminals E and C, being
activated by very small voltage
trough the terminal B.
 On following drawing we see
transistor in the circuit used as a
switch. One may wonder why we
need a transistor as a switch, when
we already have one in the same
circuit, which we use to activate
transistor via the B terminal. Well
here's an example: On the
E B C
122
dashboard we have a number of
small switches which operate all
kinds of electrical consumers. If
consumers were activated directly
by switches, they should be much
more robust to leak enough current. If we connect these switches
over transistors, as shown in the
sketch, we can use so-called microswitches through which runs a
very small voltage and current,
but with enough power to activate
transistor through which will flow
enough power to run the consumer. Such transistor’s characteristics allow us to activate consumers using the voltage produced
by solar cells and other sources
with low voltage values. In our
case, processor will be able to run
the actuators using very low voltage across the transistors.
 On the lower sketch we used a
sliding resistor or potentiometer to
regulate the voltage at terminal B
of the transistor. By increasing the
voltage at terminal B, we are regulating the flow of current through
the transistor, thus increasing the
intensity of the light bulb, and vice
versa. On the first photo of transistor samples we see that all transistors have three terminals. However, transistors located in the
metal casing, sometimes have only
two terminals. It means that one of
the terminals, E or C, is connected
to the transistor housing, as it is
the case in the lower diagram with
the terminal C.
 ow that we know how transistor works and what is its purpose
we need to know how to test it. For
testing electronic elements we used
a multimeter before. This is the
one of the essential instruments
that we have to have among
the others. Transistor can
be checked with an ohmmeter, but it is advisable to use
a multimeter with option of
diode testing. As shown in
previous photos, defective
transistor is usually noticed
by visual inspection. How-
+
-
B
E
C
C
E
B
 123
ever, if we doubt its validity, regardless of its physical condition,
we shall make the following measurements. For proper measurement of any electronic element, it
must be disconnected from the circuit. If we use an ohmmeter, the
voltage on probes has to be taken
into account, because transistor
can be damaged by the higher
voltage than it is intended for. By
switching the multimeter selector
on the diode symbol, we can begin
with the measurement. As we are
testing a diode, polarity has to be
switched while measuring, because, as we know, the diode lets
electricity trough only in one direction.
 Either way that we turn the multimeter probes poles, between terminals E and C must not be a current flow. Between terminals B
and E or B and C, current must
flow in one direction, depending
on which direction diode leaks
electricity. Different parameters
then above indicate transistor malfunction. On sketches we see, terminals are marked by the letters
E, B and C in some kind of order.
In practice, transistors do not have
a standard for terminals, so when
measuring, we do not know which
is which terminal. However, since
we now know how transistor
works, it will not be a problem,
with a little effort and help of multimeter, to determine terminals.
Let's start with the assumption
that our middle terminal is B.
Connect positive probe to the middle terminal and negative to the
one end and than to the other. Repeat the same procedure with reversed polarity, negative to B and
positive to one and than to other
end. If we hit the B terminal and
transistor is in order, in one of the
tests we shall have a flow of current between terminal B and the
one of the end terminals, which is
one E and the other C.
B B
B B
E
E
E
E
C
C
 C
C
 2o current flow
 Current flow
Transistor test by changing polarity
124
 Resistor testing
 In previous sketches, we can see
that in a transistor circuit, resistors are connected too. In order to
define the voltage at transistor terminal B, resistors are used with
specific resistance value. If we assume that for any reason, resistor
connected in series with the terminal B is faulty, we can simply conclude that transistor also can not
function. Faulty resistor will break
the circuit to B terminal and transistor will not be activated. The
even worse option is the short circuit inside the resistor. If such a
resistor regulates the voltage at
terminal B, we can surely expect
transistor failure due to excessive
voltage on the B terminal, which
damaged it. On the next sketch we
see one, schematically shown, electronic circuit which uses several
resistors in circle to regulate the
value of the circuit. Defective or
abnormal value of each resistor
will affect the validity of entire
electronic circuit, and can damage
other electronic components in the
circuit. It is difficult to suggest disconnecting each resistor and measure its value. However, if there is
a little doubt in their correctness,
and such intervention is cost effective.
 Resistor, regardless of the material from which it was made (coil,
carbon ...) has the primary function of creating desired (previously
defined) resistance in a circuit. Resistor testing is performed again
with multimeter selected to the option labeled resistance (Ω). By simple test of resistance we will determine whether resistance exists at
all, do we have the open-circuit or
short circuit within resistor. Of
course, if we obtain these two last
results, resistor is faulty. If measuring shows any value of resistance, we can assume that resistor
is in order. So, if we have an open
circuit, the instrument will not respond when we connect the probes
to the resistor terminals. If there is
a short circuit inside the resistor,
the instrument will have a maximum deflection. If resistor is correct or partially correct, the meter
will read some sort of value in
Ohms. If we find faultiness by
measuring resistor, we shall replace it with a new one with identical markings. If we suspect a
measured value, we shall have to
use resistor values table. Resistors
do not have values written in numbers, but in the colored lines on
them. If we want to know the value
of resistor which is measured, we
shall use the shown table, or any
other which can be downloaded
 125
from the Internet.
 On the above sketch we see an
example of reading the resistance
value, using the table. If our measured value is within the limits of
tolerance comparing with value in
the table, resistor is in order. If the
value differs significantly,
the resistor has to be replaced with new one.
 If we take a look at the
value table, we see that each
color on the resistor has the
value in numbers from 0 to
9. The value of the first two
colors shows the value in
Ohms (Ω). Kiloohms and
Megaohms (kΩ or MΩ) are
determined by the following
color, with whose value is
multiplied previously read
number. For example, if we
have a resistor
with four colors
and read value
of two first colors is 25 and after comes the
black color, the
total value is
25Ω. However, if
instead of black,
orange color follows, the total
value is 25kΩ ...
The following
marking on the
resistor indicates
the predicted
resistance tolerance in percent.
In this case the
tolerance is plus/minus 5%. On the
resistor marked with six colors, we
can see the heat coefficient as the
final mark.
 At the lower photo we see an example of checking resistor with
multimeter.
Oznaka s 4 boje
Oznaka s 5 boja
Oznaka sa 6 boja
 25kΩ ± 5%
 460kΩ ± 1%
 276Ω ± 5%
 1. broj 2. broj 3. broj
 Temp.
 Zlatna Zlatna
Srebrna Srebrna
 Množitelj Tolerancija
126
 Capacitor testing
 As in previous examples, and
here we will concentrate on capacitor basic functions and testing.
This basic knowledge of described
electronic elements will be sufficient to solve the problem in control modules which can be detected
and repaired by ourselves.
 Capacitor has the ability to store
electricity. Electrolytic capacitor
consists of two metal foils (anode
and cathode) and the insulator between them. One foil is connected
to the negative terminal and the
other to positive. Rolled foils are
placed in
a cylind r i c a l
housing
f i l l e d
w i t h
electrolyte. If
we connect cap a c i t o r
to the
battery,
it will be
charged
until capacitor voltage equals with
the battery voltage. If we connect
charged capacitor to the electrical
consumer, a rapid discharge will
occur. A typical example of capacitors usage is the camera flash.
When flash is switched on, capacitor is on charge. The signal light
flashes until capacitor is fully
charged, or voltage in capacitor
equals with battery voltage. By
pressing the button for taking
photo, flash lamp connects with a
capacitor and rapid discharge of
high intensity occurs. How intensive is discharge we can see when
lightning from the clouds which we
also call the capacitor.
 Capacitor has defined voltage
and capacity which it can handle.
Capacity is expressed in farads. In
our case, we will meet capacity expressed in microfarads (µF), although capacity can be expressed
in nanofarads (nF) and picofards
(pF) also. To have a picture why
capacity is expressed in microfarad, let’s say that one farad occupies the volume of one medium
size fire extinguisher. If we divide
this volume by one million, we will
get a value of one microfarad. Of
course, this is just an illustrative
example.
 Except of, as we said, storing energy, capacitor has the ability to
leak alternating current signal, regardless of being fully charged
with direct current and stopped
absorbing when voltage was equalized. Capacitor will also serve as
protection of other elements in an
electronic circuit, absorbing all DC
 - Terminal
 + Terminal
 Insulator
 Foil
 Aluminum
 Plastic
 127
voltage irregularities. either here
we shall go deeper into the schematic representations of capacitors
or the reasons why nor where they
are placed in modules circuits.
This job is done by the experts in
structural laboratories. For us, is
sufficient to know how particular
electronic elements work, which
purpose they serve, how identify
them and examine their validity,
or failures which are the most
common causes of control module
malfunctioning. Certainly, those
with more will and enthusiasm can
go deeper into this matter, but
they also have to be aware of its
complexity, which entails a lot of
learning.
 On the first photo we see electrolytic capacitor and the small ones,
which in themselves do not have a
liquid electrolyte. The first type of
capacitor we shall meet more often
as it has a larger capacity. Unlike
resistors, capacitors are found
with labelled values in figures and
by letters, like 6.5V and 200µF. On
the other smaller capacitors, the
value is expressed in codes, due to
the small printing surface. Displayed label on the condenser with
a code 104W, we shall interpret as
follows: first two digits indicate the
numerical value of 10. The third
digit is the multiplier and indicates
the number of zeros to be added.
Code letter behind the numbers
indicates the tolerance value in
percentage. As with resistors, and
here, if needed, we can use the table to decrypt the value, as well as
the interpretation of other marks:
the thermal tolerance, insulators
codes, etc. But at our level of possible repairs it will not be necessary,
because we will provide replacement by reading the label on the
faulty capacitor.
 Looking back at the first image,
we notice that one terminal of the
electrolytic capacitor is longer
than the other. Here we have the
same situation as with the diode, a
longer terminal means positive (+).
Sometimes, we shall find polarity
indications of the condenser housing. Thus, when replacing condenser, polarity has to be taken in
consideration. This second type of
smaller capacitors with no liquid
electrolyte does not have determined polarity, and terminals have
the same length. Such capacitor
can be connected either way.
 As we mentioned earlier in this
chapter, a defective capacitor will
be usually spotted by careful visual
inspection. Leakage from the capacitor is one of the most common
causes of failure. The electrolyte
can leak significantly, but can also
leave almost invisible traces of
electrolyte on the top or bottom of
the capacitor. In addition to leakage, we can notice bent top or bottom surface of the capacitor,
which are normally flat, and also
indicates a defective capacitor.
However, besides the visible causes
of failure, there is a possibility of
damaged metal foil or insulator
inside the condenser, which will
cause a reduction in capacity or
short circuit. Thus, if we doubt the
correctness of capacitors and see
128
no physical signs of malfunction,
we shall have to proceed with capacitor testing, using multimeter
again.
 As in previous tests, we will disconnect capacitor from the circuit
in order to make measurements.
Measuring can be performed by
instruments intended for this purpose. As in most cases, we do not
have instruments for precise measurement of individual electronic
element, and therefore we shall use
the Ohmmeter on our multimeter.
Before performing the test, it is
recommended to discharge the capacitor. In our case, we can not
really experience the shock of capacitor discharge through us, but
if it is a stronger capacitor in the
circuit of 220V, the consequences
may be, say at least, uncomfortable. If we create a short circuit
between the capacitor terminals
with insulated pliers or a screwdriver, capacitors will be completely discharged. The measurement of capacitor accuracy, we do
in the following way: connect the
multimeter probes to capacitor terminals. Deflection of the pointer
must be in the right direction towards the resistance value of zero.
After that, the pointer must be deflected in opposite direction of the
maximum resistance value. If we
get this result, capacitor is in order. If the pointer does not move,
it means that we have a broken
circuit in the capacitor. If the
pointer shows full deflection to the
right side where the resistance
value is zero and stays there, the
capacitor is a short-circuited and
defective in both cases. These
measurements are generally reliable when testing capacitor. For
accurate capacity measurement,
adequate instruments are required.
 At the end of this chapter, it is
worth to mention a little trick on
issues related to software problem
in modules, which in most cases
helps. Sometimes we find the DTCs
which just do not make any sense
and warn us about failure of something that has not even built in a
car, as well as warnings about the
lack of communication within the
electronic management, etc. Before
we seek for help, or go alone in
Flashing, it is recommended to disconnect the battery for half an
hour. After re-connecting the battery, the control module will be
reset and thus eliminate possible
software errors which occurred
 Testing capacitor with instrument
intended for this purpose.
 129
for any reason. Such problem we
often have on home computer. In
inability to solve the newly generated problem at the computer, we
usually use the Restart or Turn Off
option. When program starts
again, everything is as it is suppose
to be.
 Cruise control
 As we see from the title, Cruise
control in a literal translation
would mean the control of cruising
or some sort of travelling around
control. ame Tempomat which is
also used for this device, does not
tell us much about the device to
which it relates, because its
translation
would be,
some kind
of the
rhythm control or... So,
here is a descriptive meaning of
this device name.
 Cruise control is a known device
which has been incorporated in
American cars for decades, and its
purpose is to predefine the vehicle
speed on long distance, mainly on
highways. We all, more or less,
know that distance of hundred
miles from A to B on American
continent, is negligible compared
to the European vision of such a
distance. In order to enable the
driver as comfortable position as
possible during extended travelling, car designers have developed
a device with possibility to define
the vehicle speed and thus avoiding constantly keeping foot on accelerator pedal. As motorways in
Europe are expanding, this device
is lately popular there too, and we
often find them embedded in cars
intended for the European market.
 Like other appliances, cruise
control have evolved over the
years to such an extent that they
are now almost in a state to operate the vehicle automatically. But
let's start with the older models of
Cruise Control units, which will
facilitate our understanding of the
principles of modern devices in
today's automobiles.
 Testing capacitor with Ohmmeter.
130
 As we said, cruise control allows
us to define the travelling speed of
the vehicle. For example, if we
drive fifty miles per hour and turn
on the device, module or ECM will
remember and keep the speed by
the actuator connected to the
throttle butterfly or acceleration
pedal. If we want to accelerate for
overtaking, or for any other reason, we can do this by pressing the
accelerator. If we release the pedal
after accelerating, the car will continue driving at the speed at which
we have previously defined. When
brake pedal or clutch is pressed,
the device will automatically deactivate. Once we do not want to use
Cruise Control any more, we will
simply turn it off at the command
panel, which is located next to the
steering wheel.
 In the above picture we see a
typical Cruise control command
switch with options: O2-OFF,
RES/ACC (resume or return to the
default/speed up) and SET/COAST
(set/reduce speed). O2-OFF switch
is used to turn the cruise control
on and off. In some vehicles this
option does not exist, device is activated by pressing the option SET
and automatically turns off by
pressing the brake or clutch pedal.
By pressing RES/ACC or the SET/
ACC option, we are commanding
the module to remember the current speed at which we want to
continue driving. With the same
command we can increase travelling speed while driving. In other
words, if we want to increase the
travelling speed, we do not have to
press the accelerator and reset the
speed, it is sufficient to hold the
button, or by typing it, accelerate
the vehicle to the desired speed. If
we have by any chance turned off
the cruise control and turned it on
again, preset speed can be recovered by pressing the option RES or
Resume. Holding down the command with the option Coast, the
car will slow down in the same way
as it does when accelerator pedal is
released. By typing this command,
vehicle speed will be reduced accordingly. When typing commands, speed usually increases or
reduces for one to two miles, or we
would say, per click. For accurate
instructions how to use the Cruise
control device via the command
switch, it is advisable to read the
owners manual booklet supplied
with the vehicle. The marks on the
command are not standardized, so
each manufacturer entered its abbreviations and has different ways
of management. In this example
we have commands: RES/ACC and
SET/COAST, while in some other
vehicle we will find commands:
SET/ACCL, RESUME and COAST.
In any case, it is the same thing but
different commands control mode.
 131
 On the above sketch we see all
the elements of Cruise Control device. In this case the actuator is
used to control the throttle pedal
and is regulated by vacuum. For
this type of cruise control we need
a vacuum, which can be obtained
from the engine intake manifolds
on gasoline engines, vacuum pump
on diesel engines or a separate vacuum pump as shown at the sketch.
If we use the vacuum from the engine, instead of sketched pump,
there will be a valve installed controlled by ECU to regulate the vacuum flow. With the command assembly mounted on lever next to
the steering wheel, vehicle speed is
determined. Having received our
command, the module will control
the vacuum power by which actuator pulls the throttle cable in position to achieve a given speed. Vacuum servo actuator consists of a
chamber divided in two parts by
diaphragm or membrane. The vacuum pulls the diaphragm which is
connected to the accelerator cable.
Of course, on shown pulley we
have two cables which regulate the
position of throttle, one from the
actuator and the other from the
accelerator pedal. Vacuum power
defined by module, will pull the
cable just as much as it is necessary to obtain a specified car
speed. In addition to the command
circuit assembly, the module is
connected with the inductive vehicle speed sensor. So, whichever
commands we send to the module,
it will always know the vehicle
speed and understand our requirements for adjusting the travelling
speed, slowing down or speeding
up. When brake or clutch pedal is
pressed, the valve will open and
allow the entry of atmospheric air
into the system and automatically
deactivate the actuator. Left withSpeedometer Command switch ECM
Stop
 light
 Brake
 Clutch
Vacuum servo
 actuator
Vacuum pump
 Valve
Accelerator
cable pulley
 Stop
switch
132
out a vacuum or negative pressure,
the diaphragm returns to its original position and releases the throttle cable instantly. At the same
time, the ECU receives a signal
through the electrical switch incorporated in the valve and turns off
device. If we look at the sketch
carefully, we notice that in this
case, when the brake or clutch
pedal is pressed, vacuum from system is liberated, but module does
not receive an electrical signal to
deactivate device. It means, that
with this device we can press the
clutch or brake pedal slightly, and
the system will be not deactivated
because all switches are connected
in series. Only after the brake and
clutch pedals are pressed, the electrical circuit is closed through the
stop switch and circuit breakers in
both valves on pedals. As it can be
expected, each manufacturer has
developed its own operating principle of Cruise Control system with
the belief that this is just the most
convenient one.
 The principle of cruise control is
basically always the same or similar. On new car models, the ECM
will be connected to multiple
sources of information about the
vehicle movement in order to provide better and safer driving. In
these new car models, instead of
the vacuum actuator an electric
motor will regulate the throttle
butterfly opening, while in the car
with the electronic accelerator
pedal signal transmission to the
throttle step motor, opening will
be solved through the ECU. In
such a vehicle, sliding resistors are
used instead of cable, which send a
signal to the engine module about
the thrust on the accelerator pedal.
In the same way, the cruise control
module will send information to
the ECU.
 By the development of technology, today's cruise control system
devices have reached a remarkable
level, and tomorrow…? The cruise
control system essentially remains
unchanged except that is electronically perfected. On newer car
models, sensors are built-in to
measure the distance up to 150
meters between the driven vehicle
and one moving ahead. The minimum distance between vehicles is
programmed in the device module.
But for those with higher demands, there is a possibility of adjusting the distance, from maximum also called comfortable to the
 Vacuum actuator
 Electric
 actuator
 133
medium or normal, and the shortest one called sport. Selection of
distance will depend of the driver,
or of his judgement about the response in case of unforeseen situations and behaviour of drivers in
vehicles in front of him. Guided by
determined distance, Cruse control
module will reduce the vehicle
speed on the base of received signal from the sensor which measures vehicles distance. Having
achieved a given distance, the car
will adjust the speed to the vehicle
moving ahead. If the vehicle ahead
increases its speed, the sensor will
provide such information, and
module will increase the speed of
our vehicle also, taking into account determined distance, and if
there is no threat this speed will be
set as travelling default speed.
Unavoidable crash
Reaction starts
Adjusted speed to
the vehicle ahead
Steering and keeping distance
Defined speed
70 km/h
134
 This sophisticated equipment will
be of great benefit to those distracted while driving. In addition
to the sensors monitoring the distance between the vehicles in motion, they are able to detect a vehicle ahead which is stationary.
Thus, coming to
an crossroads
where the vehicle
has stopped in
front of us, the
module will receive the sensor
signal about the
stopped vehicle
and the possibility of critical distance, as well as the information of
no action taken by the driver in
terms of the expected slowdown or
braking with respect to the situation. In such circumstances, the
cruise control module connected to
the engine module and ABS, will
warn the driver with
flashing and audible signals, slow down the vehicle, and if necessary stop
it. If the module detects a
subsequent reaction of
the driver, it will suspend
all actions provided for
such situations.
 Diagnosing the Cruise Control
system on newer vehicles is achievable with OBD II scanner, as its
module is connected to the engine
module. Certainly, as in previous
cases, the diagnostic device foreseen for particular type of vehicle
will be far more extensive in the
diagnostic sense, than universal.
Problems on old types of cruise
controls are usually associated
with worn out vacuum hoses, actuators diaphragm, vacuum valves
or vacuum pumps. Problems with
the proper vacuum sealing and
worn actuators membranes do not always result in complete failure of
cruise control system. On
the contrary, more often
is the case of much lower
speed than we determined, due to the significantly weakened vacuum
in the system.
 135
 Start/Stop system
 Today's and tomorrow's automobile technicians must be reconciled with the fact that they will
frequently encounter modified existing systems, as well as brand
new ones. Mastering the basics
through these three books, there
will be no difficulties in mastering
the principles of operation of each
new system, with the help of available literature and software.
 In this example we see a new system frequently built in the new vehicles, with the purpose of saving
in fuel consumption and further
emissions reduction. Designers
have calculated
that this system
can save 5-14% in
fuel consumption,
and thereby simultaneously reducing emissions
of harmful exhaust gases. This
system is called
Stop/Start or Start/
Stop. When brake
pedal is pressed
and the vehicle
completely stops,
engine is automatically turned off,
and re-started by releasing the
brake pedal or by pressing the accelerator.
 Of course, this system is not effective when driving on the open
road, but it is certainly efficient in
city driving, especially during the
rush hours when vehicles are repeatedly stationary for several
minutes. This system operates
quite simple, but it was modified
by time as all other systems. Engine module was added by program to stop and start the engine,
and is conducted according to information received from the wheel
136
speed ABS sensor, pedal sensors,
gear change lever neutral sensor
and CKP sensor which tells the
ECU the engine RPM. By pressing
the brake pedal, the ECU will register a vehicle slow down and wait
for information from the ABS sensors that vehicle has completely
stopped, as well as the fact that the
transmission is in neutral position
and the engine revs are at a minimum. Depending of program, the
ECU will wait about five seconds
and then stop the engine. Again
depending of program, the ECU
will turn on the engine after the
brake pedal is released or by
pressing the accelerator. The program which turns the engine off
and on will vary on automatic or
manual transmissions.
 Like all other systems which have
disadvantages despite their positive characteristics, this one also
has not been spared from negative
consequences. The firs problem we
see in the noise when starting the
engine frequently with conventional electric starter, and increased consumption of electricity
from the battery. Furthermore,
there is a problem with deactivation of all engine-driven aggregates. To solve these problems, a
series of modifications are made,
where certain aggregates are powered by electric motors. Power
steering, previously hydraulic, becomes electric. An additional vacuum pump driven by an electric
motor is added, or an additional
vacuum tank is mounted for power
brakes and others vacuum operated actuators. All this requires an
adequate source of electricity, so it
is necessary to provide vehicle with
better battery. These modifications
and investments are cost effective
when it comes to the environmental effect that is achieved with
this system. The analyses showed
very positive results and effectiveness of this Idle-Stop system, and
serial standard installation began
first in American vehicles followed
by MII Cooper since 2007,
Audi's A3, A4 and A5 from 2009,
Mazda 3 by the end of 2009 and a
number of other manufacturers.
 In attempts of solving the mentioned problems associated to aggregates driven by engine in one
way or another, big step has been
made by modifying the starter motor. The first step was the production of quieter classic starter motor with the new transmission and
coupling system. However, as the
modification did not turn out with
the expected effect, the new idea
was born, to start the engine completely silently with electric starter
integrated in the alternator. On
the following sketch and photograph we see an integrated starter
in the alternator which turns the
engine silently by the belt.
 Solution of
i n t e g r a t e d
starter in the
alternator is
satisfactory
for starting
the engine silently, but
there is still a
 137
major problem of power consumption. Therefore, this system has a
built-sensor which monitors the
power consumption from battery.
If there is excessive power consumption due to the frequent engine starting and other electrical
consumers used during the engine
idle, the ECU will shut down the
Start/Stop system until the battery
is sufficiently charged.
 This problem was solved by the
experts of Mazda vehicles manufacturer on diesel engines. Instead
of turning the engine with an electric starter, they did it by turning
the engine with the engine piston
on power stroke. How
does it work? In simple words, using the
information from CKP
sensor, ECU exactly
knows which piston
was on power stroke
when engine was
turned off. Thus, in the
cylinder on the power
stroke, the air is compressed and waiting for fuel to be
injected. When command to start
the engine is received, the ECU
will inject the fuel into the cylinder. Due to the thrust, piston will
turn the crankshaft and the engine
continues burning mixture in
other cylinders. This technology
has passed all tests and the engine
is supposed to start in record time
of 350 milliseconds, or one time
faster than turned on by an electric starter. o doubt that this system is functioning perfectly, if the
engine is in such state too. But,
what happens if engine is partially
worn and compressed air exits
through the leakages
beside the pistons and
valves? Probably, the
only solution is one
combined system with
an electric starter
which will help in such
cases.
 This is a good example of the necessity to
understand and improve the knowledge
about the DTC's related to this or similar
systems.
138
 Regenerative braking system
 In chapter Stop/Start system we
have mentioned the problem of
electricity consumption when the
engine is turned off and consumers
are turned on. Trying to solve this
problem, car manufacturers have
not only overcome this problem,
but generated so much extra electricity with regenerative braking
system that fuel consumption is
significantly reduced on cars
where this system is installed.
 Those, who are engaged in vehicle maintenance for longer period
of time, will remember the cars
with carburettors which did not
have idle controlled by ECU, but
manually adjusted. When idling
had to be adjusted, we should take
in consideration electrical consumers used during the night or cold
and rainy weather. Such consumers are: lights, heater, wipers, fan
coolers, etc. amely, when greater
amount of electricity is needed, the
alternator creates stronger magnetic field, and thus makes greater
resistance on the engine crankshaft pulley which drives the alternator. Due to the
great resistance, more
power was needed to
drive the alternator
and the consequence
was RPM drop up to
ten percent, and
sometimes more,
which depended of
the number of consumers and the engine power. So, we can conclude
that the fuel consumption increased proportionally with the
number of electrical consumers
involved. Simply said, the fuel used
for power to drive the alternator
could be used to drive the car.
Power used to drive the alternator,
could give us some extra mileage,
and by simple mathematics, save
on fuel.
 As in all other cases, the solution
here is relatively simple. Change is
primarily made on alternator concept which is in this case called a
variable. Its primary function remains unchanged. However, by
releasing the accelerator pedal, the
ECU receives information about
the engine braking and redirects
the alternator function. During the
engine deceleration, the alternator,
by the orders from ECU, increases
the magnetic field and generates a
voltage of 25V. However, where to
store this excess energy? For this
purpose, an increased capacity capacitor is used, with extremely
rapid charging and discharging.
Electricity stored in the capacitor,
will be, when needed, converted by
the DC/DC converter to the value
 139
of 12V, and distributed to
recharge the battery and
run the electrical consumers. Knowing how often we
use the engine in city driving to slow down, we can
assume that the capacitor
will accumulate more than
enough power to run all
consumers when engine is
turned off by the Start/Stop
system. Obviously, this is
the ideal solution for solving the
aforementioned disadvantage of
Stop/Start system, but where is the
savings in fuel? We have concluded that alternator requires a
certain power to be driven. To get
this power from engine, some
amount of fuel has to be burned.
Having a sufficient amount of energy stored in the capacitor, ECU
will deactivate the alternator when
accelerating and relive the engine
of extra load usually created by
alternator. Only after the battery
discharges below the permissible
limits due to long rides on the open
road, where we rarely use the engine to slow down, the ECU will
activate the alternator. Vehicle engine relieved of alternator load,
could contribute to the savings in
fuel consumption up to 10%. This
conclusion was made by engineers
after series of tests and measurements.
 In the upper part of the shown
drawing, we see the situation when
slowing down with the engine, and
when the engine energy is used to
activate the alternator and produce additional amount of electricity. Electricity is stored in the capacitor and trough the converter
distributed to the battery and electrical consumers.
 The lower part of the drawing
shows the situation when accelerating or driving, when ECU deactivates the main function of the alternator, and all consumers are
supplied with electricity from capacitor and battery.
 HHO
 From all three books is evident,
that, among other things, the
theme of reducing the fuel consumption exists from the beginning of automobile industry. Today's cars achieve minimum fuel
consumption in relation to performances and power developed.
This all is due to the development
of electronics which is increasingly
present in automobile control
management. Enjoyment in driving within the specified consumption limits for a specific vehicle, we
can only achieve with correct driving regime. However, this world
would not go forward if there are
140
no people who work tirelessly to
improve the existing solutions,
even if it is often unsuccessful.
First example is the gas conversion
system which exists on market for
decades. Gas powered vehicles are
quite common, and its principle is
known to most of us. However, today we can find a number of products which supposedly reduce the
fuel consumption. These are the
various versions of electronic devices that affect the molecular
composition of the fuel, pills that
enhance the properties of the fuel,
air intake spiral routers, etc. one
of these devices have proved conclusively effective. Basically it always comes down to a theoretical
explanation based on the laws of
physics and chemistry. Of course,
in these explanations are taken
into account only the parameters
which correspond to those who offer such products, while all the
negative effects of such devices are
not mentioned.
 In recent years the media spins
very intriguing title: Driving a car
on water. There are several different versions of this title, but all
boil down to the same meaning.
Well, let’s see what is it all about.
 Of course, it would be absolutely
wrong to understand the meaning
of this title literally. either internal combustion engine can run on
water, nor can the fuel be mixed
with water. Thus, the water
through a chemical process is used
as an alternative source of additional fuel added to conventional
fuels. Once we mention the chemical process and water, association
with electrolysis comes automatically. Exactly, this is what it is all
about. Knowing that we need electricity for electrolysis, there was a
doubt about this project in very
beginning. amely, there is a well
known interpretation that electrolysis can not possible produce
more energy than was used in its
process. When we draw extra electricity from the generator, we have
to provide extra power to drive it,
as already explained. But, are the
laws of physics finally defined?
 So, driving on water comes to the
following: By installing the conversion kit, water transforms to HHO
or Brown's gas. For this electrochemical process electricity is required, and it is only obtainable
from the car battery. An alternative source of electrical energy can
be solar cells available on the market, and are typically built on top
of the car. Brown's gas acts as a
stimulant to conventional fuel, and
fed separately into the engine intake manifold. Going through the
engine intake manifold, HHO acts
as an oxidant and improves combustion efficiency and reduces
emissions of harmful exhaust
gases. However, we should not understand all this so easily, because
it appears that a number of problems related to car electronics
management may occur, as it is
not provided for such modifications. The problem is present in
the ignition timing, higher engine
temperature etc. So, any modification entails a number of side ef-
 141
fects, or, simpler called, problems.
 Many will ask, what is the difference between HHO and H2O as in
both cases we have two atoms of
hydrogen and one atom of oxygen.
H2O is the chemical formula for
water molecule in which one oxygen atom is attached to two hydrogen atoms. HHO is a mixture of
hydrogen and oxygen in the gas
form with the ratio of 2:1.
 HHO system, in theory, is very
simple. It consists of an electrically
powered electrochemical generator, which in process extracts
HHO gas from water. The gas is
distributed from the generator to
the engine intake manifolds and
engine idling port. Simple vacuum
valve regulates HHO entry to one
side or the other.
 It is not disputed, that this system theoretically increases the
combustion efficiency and also
lowers fuel consumption. But,
could this generator produce a sufficient amount of gas, and in what
time. What is the electrical power
consumption? If there is enough
energy from the alternator, why is
recommended installation of additional solar energy or stronger alternators? What is the real effectiveness of this system in terms of
fuel savings? How all of this affects
the operation of the engine? Are
there side effects...?
 These are all questions that
never had really given convincing
answers. But either way, this system is installed in vehicles and is
being modified day after day in
terms of making more efficient
HHO gas generator and proper
dosage in relation to the engine
RPM.
 On the following sketches we see
the functioning principle of HHO
gas generator with other simple
elements built into the vehicle. The
photograph shows more effective,
so-called, dry generator.
HHO
into the engine
intake manifold
Minus electrode
extracts oxygen
Electrolyte:
distilled water &
nitrous hydroxide
HHO gas
Plus electrode
extracts hydrogen 