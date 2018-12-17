from iconservice import *

TAG = 'GoodsEvent'

class GoodsEvent(IconScoreBase):

    _EVENT_STATE    = 'event_state'
    _JOIN_MESSAGE   = 'join_message'
    _CANDIDATE_LIST = 'candidate_list'
    _EVENT_WINNER   = 'event_winner'
    
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

        # Stores evet status. True:Event OPEN, False:Event CLOSE
        self._VDB_event_state = VarDB(self._EVENT_STATE, db, value_type=bool)

        # Stores {sender_address : message} key/value pairs. 
        # Message must be an integer between 1 ~ 7.
        self._DDB_join_message = DictDB(self._JOIN_MESSAGE, db, value_type=int)

        # Stores paticipants list. Same address should not be stored in duplicate.  
        self._ADB_candidate_list = ArrayDB(self._CANDIDATE_LIST, db, value_type=str)

        # Stores the list of winners. No duplicate addresses are permitted.
        self._ADB_event_winner = ArrayDB(self._EVENT_WINNER, db, value_type=str)
        
    def on_install(self) -> None:
        super().on_install()
        self._VDB_event_state.set(False)
        
    def on_update(self) -> None:
        super().on_update()
        
    def owner_check(self):
        if self.msg.sender != self.owner:
            revert('Permission Denied.')
        
    @external
    def event_start(self):
        self.owner_check()
        self._VDB_event_state.set(True)
    
    @external
    def event_stop(self):
        self.owner_check()
        self._VDB_event_state.set(False)
    
    @external
    def join_event(self, _join_message:int):

        # Implement This  
        # Check prerequisite. Event status must be True.
        #
        #if not ( ) : revert('Event Closed.')

        # Implement This  
        # _join_message must be a number between 1 to 7.
        #
        #if ( ) or ( ) :
        #    revert('Check your Message Value...')

        # Implement This 
        # 1. Get messager sender address, and store it as a string. 
        # 2. If the address is not in the _DDB_join_message, 
        #    add the adress in the _ADB_candidate_list. 
        # 3. Add/Update the sender's message in the _DDB_join_message, 
        #
        #_sender_address = str( )
        #  
        #if self._DDB_join_message[ ] == 0:
        #    self._ADB_candidate_list.put( )
        #
        #self._DDB_join_message[ ] = ( )
        pass
        
    @external
    def raffle(self):
        # Implement This
        # Make sure the message sender is the contract owner.
        #
        #self.( ) 

        # Implement This 
        # Event status must be closed. 
        # 
        #if ( ): revert('Please close the event first.')

        # Get the number of participants.
        # Revert if the participants number is zero.
        _join_count = len(self._ABD_candidate_list)

        if _join_count == 0: revert('Candidate list is empty.')

        # Use tx hash to generate a pseudo-random number to pick an address among candidates.  
        _get_random = int.from_bytes(self.tx.hash, byteorder='big', signed=False) % _join_count

        # Add the selected address to the _ADB_event_winner. 
        self._ADB_event_winner.put(self._ADB_candidate_list[_get_random])
        
        # Remove the address from the candidate list. 
        # Note that pop(index) is not supported in ArrayDB.
        if _get_random == 0:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[1:_join_count]

        elif _get_random == _join_count -1:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_join_count - 1]

        else:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_get_random]\
                                     + list(self._ADB_candidate_list)[_get_random + 1 : _join_count]

    # Returns the total number of participants.
    # Since the winner is subtracted from the initial candidate list, 
    # the number of candidatess and the number of winners are added.
    @external(readonly=True)
    def count_join_user(self) -> str:
        return str(len(self._ADB_candidate_list) + len(self._ADB_event_winner))
        pass
        
    @external(readonly=True)
    def show_event_winner(self) -> str:
        return "Count=[%s], Address LIST=%s"\
               %(str(len(self._ADB_event_winner)),\
                 str(list(self._ADB_event_winner)))
        
    @external(readonly=True)
    def check_join_message(self, _join_address:str = None) -> str:
        # Implement This 
        # _join_address is an optional value. If empty, use message sender address.
        #
        #if not _join_address: _join_address = str( )
        
        # return joiner's message
        _get_msg = self._DDB_join_message[_join_address]
        
        if _get_msg == 0: return "Address(%s) has not joined the event."%(_join_address)
        return str(_get_msg)
        
    @external(readonly=True)
    def check_event_state(self) -> str:
        if self._VDB_event_state.get(): return "Event Opened."
        
        return "Event Closed."
