from iconservice import *

TAG = 'GoodsEvent'

class GoodsEvent(IconScoreBase):

    # 키 값으로 사용할 문자열 소개
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
        # event_state 확인 -> False 인 경우[참가자 모집 종료] revert
        # if not self._VDB_event_state.get(): revert('Event Closed.')

        # 파라미터 _join_message 확인 -> 1 보다 작거나 7 보다 큰 경우 revert
        # if _join_message < 1 or _join_message > 7:
        #     revert('Check your Message Value...')

        # 트랜잭션 생성자의 이벤트 참가 여부 확인 및 아직 참갛지 않은 경우 추가 -> 해당 참가자의 메시지 수정
        # _sender_address = str(self.msg.sender)
        # 
        # if self._DDB_join_message[_sender_address] == 0:
        #     self._ADB_candidate_list.put(_sender_address)
        #     
        # self._DDB_join_message[_sender_address] = _join_message   
        pass
        
    @external
    def raffle(self):
        # 스마트 컨트랙트 소유자 확인 -> owner_check()
        # self.owner_check()

        # event_state 확인 -> True 인 경우[계속 참가자 모집 중] revert
        # if self._VDB_event_state.get(): revert('Please close the event first.')

        # 참가자가 없는 경우 -> revert
        # _join_count = len(self._ADB_candidate_list)
        
        # if _join_count == 0: revert('Candidate list is empty.')

        # 정상적으로 진행되는 경우 승자 뽑기 -> 소스코드 유지 + python 리스트 pop(index) 미지원에 따른 구현 설명
        _get_random = int.from_bytes(self.tx.hash, byteorder='big', signed=False) % _join_count
        
        self._ADB_event_winner.put(self._ADB_candidate_list[_get_random])
        
        if _get_random == 0:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[1:_join_count]

        elif _get_random == _join_count -1:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_join_count - 1]

        else:
            self._ADB_candidate_list = list(self._ADB_candidate_list)[0:_get_random]\
                                     + list(self._ADB_candidate_list)[_get_random + 1 : _join_count]
        
    @external(readonly=True)
    def count_join_user(self) -> str:
        # 현재까지 참여한 인원의 수 [아직 후보 리스트에 있는 인원 수 + 승자로 선정된 인원 수]
        # return str(len(self._ADB_candidate_list) + len(self._ADB_event_winner))
        pass
        
    @external(readonly=True)
    def show_event_winner(self) -> str:
        # 승자 리스트
        return "Count=[%s], Address LIST=%s"\
               %(str(len(self._ADB_event_winner)),\
                 str(list(self._ADB_event_winner)))
        
    @external(readonly=True)
    def check_join_message(self, _join_address:str = None) -> str:
        # _join_address -> 조회하는 사람의 주소로 설정(파라미터 디폴트 값에 self.** 사용할 수 없어서...?)
        # if not _join_address: _join_address = str(self.msg.sender)
        
        # 조회하는 사람의 메시지 확인
        _get_msg = self._DDB_join_message[_join_address]
        
        if _get_msg == 0: return "Address(%s) has not joined the event."%(_join_address)
        
        return str(_get_msg)
        
    @external(readonly=True)
    def check_event_state(self) -> str:
        # 이벤트 참가 가능 여부 확인
        if self._VDB_event_state.get(): return "Event Opened."
        
        return "Event Closed."