from iconservice import *

TAG = 'GoodsEvent'

class GoodsEvent(IconScoreBase):

#
    _EVENT_STATE    = 'event_state'
    _JOIN_MESSAGE   = 'join_message'
    _CANDIDATE_LIST = 'candidate_list'
    _EVENT_WINNER   = 'event_winner'
    
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

        # True:Event OPEN / False:Event CLOSE
        self._VDB_event_state = VarDB(self._EVENT_STATE, db, value_type=bool)

        # {ADDRESS:Answer Optional Message(exam. 1 ~ 7)}
        self._DDB_join_message = DictDB(self._JOIN_MESSAGE, db, value_type=int)

        # [ADDRESS_1, ADDRESS_2, ...] -> Not to be duplicate address
        self._ADB_candidate_list = ArrayDB(self._CANDIDATE_LIST, db, value_type=str)

        # Event winner Address [ADDRESS_1, ADDRESS_2, ...]
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

        # is Event started ?
        if not self.________________.get(): revert('Event Closed.')

        #join_message is the number of dice.
        if _join_message _____ _join_message ___ :
            revert('Check your Message Value...')

        #set property
        #msg has two kind of property
        _sender_address = str(self.msg.______)

        if self._DDB_join_message[_sender_address] == 0:
            self._ADB_candidate_list.put(_sender_address)

        self._DDB_join_message[_sender_address] = _join_message
        pass
        
    @external
    def raffle(self):
        # Make sure the message sender is owner.
        self.___________()

        # is Event started ?
        if self.________________(): revert('Please close the event first.')

        # Make sure there are no participants.
        # first, count participants.
        # second, if participants count number were 0( you can use len(Array DB)), close the event. with revert.
         ___________ = len(self.___________________)
         if ___________ == 0: revert('Candidate list is empty.')

        #Divide Hash to get the random value.
        _get_random = int.from_bytes(self.tx.hash, byteorder='big', signed=False) % _join_count

        # Pop(index) is not supported.
        self._ADB_event_winner.put(self._ADB_candidate_list[_get_random])
        if _get_random == 0:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[1:_join_count]

        elif _get_random == _join_count -1:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_join_count - 1]

        else:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_get_random]\
                                     + list(self._ADB_candidate_list)[_get_random + 1 : _join_count]

    # Responds to the current number of people.
    # Since the winner is subtracted from Array, the number of participants and the number of winners must be added.
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
        # Find joiner's address
        if not _join_address: _join_address = str(self.msg.______)
        
        # return joiner's message
        _get_msg = self._DDB_join_message[_join_address]
        
        if _get_msg == 0: return "Address(%s) has not joined the event."%(_join_address)
        return str(_get_msg)
        
    @external(readonly=True)
    def check_event_state(self) -> str:
        if self._VDB_event_state.get(): return "Event Opened."
        
        return "Event Closed."