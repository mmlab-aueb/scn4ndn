# SCN4NDN Experiment scenarios
## About
These are SCN4DN experiment scenarios and their corresponding scripts

## Scenario 0: The baseline scenario
### Description
This is a baseline scenario used as a reference for the rest of the experiments. This scenario includes
a Producer script (located in the folder Producer01) and a Consumer script (located in the folder Consumer). 
The Producer script advertises `ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com` name prefix. Initially, the Consumer 
script sends an interest message for that prefix. The first that packet arrives that includes the content item's metadata. 
These metadata indicate that the content item includes 10 chunks. Then, the Consumer script requests chunks one by one, 
i.e., it requests the second chunk after the first chunk has arrived, and so forth.  

## Scenario 1: Use of multisource for content retrieval acceleration
### Description
This scenario experiments with the use of multiple sources (multisource), that are used simultaneously for receiving an item.
For this experiment we extended our reference scenario to include another Producer (located in the folder Producer02). This producer 
advertises the same content item using a different name prefix, however the two content items are linked through their metadata.
As in the reference scenario, the Consumer script sends an interest message for the prefix advertised by Producer01. 
The first packet that arrives includes the content item's metadata. These metadata indicate that the content item includes 10 chunks, 
as well as that the item has an alternative name. Then, the Consumer script requests half of the chunks using the original name, and 
at the same time it requests the rest of the chunks using the alternative name.

### Outcome
The requested item is received almost two times faster compared to the baseline scenario

## Scenario 2: Recover from network failure using multisource
### Description
This scenario experiment the the use of multisource to recover from network failures at the application layer. 
The setup of this experiment is the same as in scenario 1. However, in this experiment the Consumer script uses 
the alternative name as a backup solution. Producer01 is configured to stop responding to new interests after 
transmitting the 5th chunk. At this point, the corresponding interest 'times out' and the Consumer requests 
the rest of the chunks using the alternative name. The new interests are received by Producer02.

### Outcome
The Consumer starts receiving the requested item from Producer01. After receiving the fifth chuck a
`InterestTimeout` exception occurs. Then the Consumer continues receiving the requested item from Producer02