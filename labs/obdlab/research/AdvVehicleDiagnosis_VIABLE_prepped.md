---
title: "Advanced Vehicle Diagnosis (BMW/ISTA) — VIABLE extract"
source: "OCR txt, BMW Service training, ISTA-era (post-2007). Petrol 1990-2010 scope filter applied."
note: "Only the generic diagnostic-METHOD section is viable for 4DLab. ISTA tooling, NED test plans, fault-memory UI, bus systems (CAN/FlexRay/MOST/Ethernet), chassis & body are OUT and excluded here. See AdvVehicleDiagnosis_ANALYSIS.md."
optimized_for_llm: true
---

# Advanced Vehicle Diagnosis (BMW/ISTA) — VIABLE extract

## C1 — Understanding Diagnostics & the 5-step Diagnostic Plan
Trial and error creates inconvenience for the Customer and the Service Department when misdiagnosis or longer waits occur as the technician tries different repair attempts. This is against BMW’s promise to the customer to “Fix it right the first time, on time, every time”.
If the vehicle is not repaired efficiently the productivity of the technician suffers. Taking some time at the beginning to plan a diagnostic course of action can help give structure to what may appear in the beginning to be a chaotic situation.
As future systems increase in complexity so does their dependency on the Diagnosis Program as the principle tool for troubleshooting. However, the importance of understanding the calculated steps of a basic troubleshooting plan is just as important as before.
There will always be instances where the Test Modules provided by ISTA need to be supplemented by a thoughtful diagnostic plan that is created by the skilled technician. A parallel diagnostic plan that includes proper recording of test data along with the Diagnosis Program is a good habit to follow every time that troubleshooting is required.
A successful diagnostic plan will:
  •    Save repair time.
  •    Satisfy the customer by reducing vehicle down time.
  •    Increase Center profitability.
  •    Increase technician pride and earnings.

        Diagnostic Plan

The Diagnostic Plan consists of 5 steps:
  1.    Verify the Customer Complaint -“Experience the Symptom!”
  2.    Analyze the Problem.
  3.    Isolate the Problem.
  4.    Repair the Problem.
  5.    Verify the Repair.

    Verify the Customer Complaint: Experience the symptom!

Most troubleshooting starts the moment you receive a written description of the customer complaint. The complaint is the customer’s description of a symptom that they are experiencing with the vehicle.

■ Symptom
A symptom is any circumstance, event or condition that accompanies something and indicates its existence or occurrence.


There may be multiple symptoms that are created with one problem.
An example is a defective thermostat: If the thermostat is stuck open the heater output will be insufficient, also, if the engine can never reach operating temperature then fuel mileage and performance will suffer. Which one of these complaints (symptoms) would lead you to the problem faster?
What is important to remember is that the customer may only complain about one symptom. It is the job of the technician to be a detective and carefully observe. There may be another symptom not complained of that directly points to the root cause of the problem.

■ Steps to Verify the Complaint
  •    Before getting in the vehicle, review the R.O., confirm this is the correct vehicle.
  • Is any additional information needed about the complaint? Certain questions to the customer can help narrow this step.
  • Is the problem intermittent? What are the conditions (roads, temp., speed, etc.)? What is the frequency of the occurrence?
  • Test drive if drivability related or the conditions require, duplicate conditions as stated by customer.
  •    Was the complaint reproduced?
  •    Is knowledge of system or vehicle sufficient?
  • Review reference training material and owner’s handbook for a description of feature operation.
  • Research complaint in SIB’s.
  •    Research past repair history on vehicle.

    Analyze the Problem

After verification of the complaint, analyze the problem. Use all resource available to aid in system diagnostics:
  •    Vehicle Fault Memory
  •    ETM, Repair Manual, SIB, etc.
  •    Vehicle Repair History
  •    Training Handouts
  •    Round Table Information
  •    Hotline
  •    Known Good Vehicle

Analyzing the problem allows for the development of a repair plan.


■ Steps in Analyzing the Problem
  •    Perform a Short Test.
  •    Does an SIB pertain to this vehicle?
  •    Refer to the Function Description for additional system information.
  •    Is a test plan available for this system?
  •    Use fault symptom selection.
  •    Perform Diagnosis Request.

    Isolate the Problem

To isolate the problem is “to place apart from others”.
The object here is to zoom in on the problem area. It is easy to be overwhelmed by a problem, just reaching for an ETM can add to the confusion. ISTA provides automatic tests in test modules to aid in the determination of the exact area or cause of the problem.
The elimination of components from the diagnostic trail, shortens the path.
The first question asked should be:
  •    Is the problem Hydraulic, Mechanical or Electrical?
Save time by NOT testing components that could not create the problem.

■ Steps in Isolating the Problem
  •    Use Test Modules.
  •    Perform electrical tests with the IMIB or a DVOM.
  •    Consult fault charts in Repair or Diagnostic Procedures Manuals.
  •    Control Module Self Diagnosis.
  • Use appropriate special tools (e.g. battery draw tester, tank leakage adapters, breakout boxes, etc.).
  • Substitute a known good part.

                                         Workshop Hint                                           
If a TEST PLAN is not available:                 If a TEST PLAN is available:                   
•    Think about the system in its entirety.     •    Do not skip steps.                        
•    Be sure the normal operation is understood. •    Never assume results without doing a step.
•    Develop a PLAN.                             •    Recheck your work.                        
•    Use all available resources.                                                               
•    Don’t try to diagnose the entire system at                                                 
once, break it into manageable chunks.                                                          
•    Check the easy things first. It would waste                                                
time to install the breakout boxes to find a                                                    
bad bulb.                                                                                       



    Repair the Problem

Repair the problem using approved repair techniques and parts. Having verified, isolated and analyzed the problem the last step is to repair or replace the component. Before installing that shiny new part, take one last step back from the vehicle to ask a final set of questions.
  •    Could another component have caused this part to fail?
  •    Were all the instructions in the Test Plan or Diagnostic Procedures followed?
  •    Is there anything that might have been overlooked?
Confident that the proper diagnosis has been made, complete the repairs.

■ Steps to Repairing the Problem
  •    Follow the instructions in the repair manual.
  •    Refer to Construction Groups in the microfiche if necessary.
  •    Follow specific guidelines for wire harness repair or replacement.
  •    Make proper adjustments after installing the part.
  •    Perform Coding or Programming if required.
  •    Make sure another problem is not created in performing this repair.

    Verify the Repair

Always recheck for the complaint under the same conditions used to verify.
The object is to prove the problem does not resurface.
  •    Clear the fault codes.
  •    Test drive the car.
  •    Check for re-occurring fault codes.
  •    Clear adaptations if necessary.
  •    Recheck the part installation for missing bolts or tie wraps.



    Workshop Hints


                                • Follow repair or replacement procedures as detailed in TIS.
                                • Use only genuine parts.


## C2 — The I.P.O. Principle (Input -> Processing -> Output)




Control modules receive information from sensors advising them of certain operating conditions. This information is identified as Input to the control modules. The Input continually informs the control modules of conditions that may be changing.

The control module then process the Input information comparing it to programmed responses or commands based on every possible operating condition. The control module decides based on the programming and the Input conditions which output signal to operate.

The control module, based on the processing that has occurred, then sends a signal to a component changing the status of that component. The components respond to the output signal of the control module.

This is known as the I.P.O. Principle.
