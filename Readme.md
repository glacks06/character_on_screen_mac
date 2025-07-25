화면 속에서 움직이는 캐릭터(도로롱)
=
## 기본 설명
도로롱 캐릭터가 화면상에서 움직임.

가만히 있는 상태와 달리며 움직이는 상태로 나뉨.

앞으로 가능하면 기능을 더 추가해볼 예정.

## GitHub
GitHub repo 주소
<pre><code>https://github.com/glacks06/character_on_screen_mac.git</code></pre>

git clone 명령어
<pre><code>git clone https://github.com/glacks06/character_on_screen_mac.git</code></pre>

## exe 파일에 대해
pyinstaller를 통해 exe파일 생성
명령어는 아래와 같음
<pre><code>
pyinstaller --onefile -w \
  --name 도로롱 \
  --icon main.icns \
  --add-data "run1.png:." \
  --add-data "run2.png:." \
  --add-data "idle1.png:." \
  --add-data "idle2.png:." \
  main.py
</code></pre>

단, 각 OS에서 만든 실행파일은 해당 OS에서만 실행 가능.
현재 프로젝트는 mac용.