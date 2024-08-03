# 스피드키노 예측
동행복권 스피드키노 번호 예측, 당첨번호 체크, 원하는 날짜 당첨번호 저장, 중복 당첨 회수 조회.

# 사용법  
### 파이썬과 포이트리 설치  

- `poetry update` 
- `poetry shell`

원파는 파일 실행.


# 파일설명

### check_win.py  
![alt text](images/markdown-image.png)  
해당 번호가, wins.json 파일안에 있는지 조회  

### test_check_2.py
wins.json 에서 중복 당첨 회수 조회

### colling_login_test.py
스피드키노 당첨번호 전체 조회해서 wins.json 에 저장  

- 스피드키노 당첨번호 조회하려면 로그인해야함.  
- `config.ini` 에 아이디와 비밀번호 저장해야함.  

### convert.py
`wins.txt` to `wins.json`