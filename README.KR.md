# Overview
 > ������ Ŀ�´����̼������� ���� �߼� �̺�Ʈ�� ����� ����Ʈ ��Ʈ��Ʈ ����.
***
# Requirement Description
1. ��ڴ� �̺�Ʈ ����/���Ḧ ������ �� �ִ�.
2. �̺�Ʈ ����� �����ڴ� �̺�Ʈ�� ������ �� ����.
3. �̺�Ʈ ���� ���� �� ���� �������� ������ �� �ִ�.
4. �����ڴ� ������ ���� ���� �� �Ѱ����� �����ϰ� ��ȣ�� �޼����� ������ �̺�Ʈ�� �����Ѵ�.
5. �̺�Ʈ�� �ߺ� ������ �� ������ ��÷�� �ߺ� ����� �� �� ����.
6. �ߺ� ������ �亯�� �ֽ����� ���� �ȴ�.
7. �̺�Ʈ ��÷�� �Ѹ� ��÷�Ѵ�.
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
- SCORE ���� ���� Ȯ��.

```
@external
def event_start(self) -> None:
```
- GoodsEvent SCORE�� open ��. �����ڸ� ���� ����.

```
@external
def event_stop(self) -> None:
```
- GoodsEvent SCORE�� close ��. �����ڸ� ���� ����.

```
@external
def join_event(self, _join_message:int) -> None:
```
- ������ �ɼų��� ���� _join_message�� �Է¹ް� �̺�Ʈ�� �����Ѵ�.

```
@external
def raffle(self) -> str:
```
- �����ڸ� ���� ����. �̺�Ʈ ��÷�ڸ� ����. �ѹ��� �Ѹ��� ��÷�ڸ� �̴´�.
  
```
@external(readonly=True)
def count_join_user(self) -> str:
```
- �̺�Ʈ ������ ���� ����Ѵ�.

```
@external(readonly=True)
def show_event_winner(self) -> str:
```
- �̺�Ʈ ��÷�� ���� ��÷���� ���� �ּҸ� ����Ѵ�.

```
@external(readonly=True)
def check_join_message(self, _join_address:str = None) -> str:
```
- �������� �ɼų��� ���� ���� Ȯ���� �� ����. ��ȸ�ϴ� �����ּҰ� ���� ��� Ʈ������� �߻���Ų ������ ���� ���� ��ȯ�ϸ� 
  ��ȸ�� ���� �ּҸ� _join_address�� �Է��ϸ� �̺�Ʈ ������ �Է��ߴ� �޼����� ����Ѵ�.
```
@external(readonly=True)
def check_event_state(self) -> str:
```
- ���� �̺�Ʈ�� open/close ���¸� ����Ѵ�.
***

# Author
> nomadconnection Techsupport TEAM. (bjlee)
