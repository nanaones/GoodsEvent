# Requirement Description
1. The operator can start or stop the event.
2. Participants can not participate in the event after the event stopped.
3. The operator can change the event status from stop to start.
4. Participants participate in the event by submitting a message, message should be a number within certain range.
5. Paticipants can submit a message multiple times, and the message is updated with the latest submission. Multiple submittion does not increase the chance of win.
6. A winner is selected each time the designated function is called, and the result should be appended to the list. There must be a way to list up the winner list. 

***
# Development Environment
- OS : ubuntu 18.04 (Docker = Ubuntu 18.04.1 LTS)
- python : 3.6.6
- T-bears : v1.0.6.1 (Docker)
***
# Methods
```
def owner_check(self) -> None:
```
- Verify SCORE execution permissions.

```
@external
def event_start(self) -> None:
```
- Start the event. Only the owner can change.

```
@external
def event_stop(self) -> None:
```
- Stop the event. Only the owner can change.

```
@external
def join_event(self, _join_message:int) -> None:
```
- Enter the optional value _join_message when participating and participate in the event.

```
@external
def raffle(self) -> str:
```
- Only the owner is executable. Select the Winner of the Event.
  
```
@external(readonly=True)
def count_join_user(self) -> str:
```
- Shows the number of event participants.

```
@external(readonly=True)
def show_event_winner(self) -> str:
```
- Shows the number and wallet address of the event winners.

```
@external(readonly=True)
def check_join_message(self, _join_address:str = None) -> str:
```
- Allows you to see the value of the participant's selected response. If there is no wallet address to inquire, the user's response value that caused the transaction is returned. If you enter the wallet address to query in _join_address, it prints the message you entered when you joined the event.
  
```
@external(readonly=True)
def check_event_state(self) -> str:
```
- Outputs the open/close status of the current event.
***

# Author
> nomadconnection Techsupport TEAM. (bjlee)
