# -*- coding: utf-8 -*-
import os 
import sys
import pygame
import pygame_textinput
from pygame.locals import *

# 초당 프레임수를 정의
TARGET_FPS = 30
 
clock = pygame.time.Clock()
 
 
# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
# 텍스트 좌표
textPointCurStation = (350, 823) #현재 역
textInputPointCurStation = (500, 1000)
textPointLine = (350, 873) #호선
textInputPointLine = (500, 100)
textPointDirection = (350, 923) #direction
textInputPointDirection = (500, 1000)

# input flags
curFlag = True
lineFlag = False
directionFlag = False

# 라이브러리 및 디스플레이 초기화
pygame.init()

screenWidth = 1900#1680
screenHeight = 1024#1080
screen = pygame.display.set_mode((screenHeight, screenWidth), FULLSCREEN | DOUBLEBUF)
 
# 폰트 로딩 및 텍스트 객체 초기화
fontObj = pygame.font.Font("font/D2Coding.ttc", 32)

# Create TextInput-object
#curStationTextinput = pygame_textinput.TextInput()
#curStationTextinput.font_family = "font/D2Coding.ttc"
#lineTextinput = pygame_textinput.TextInput()
#lineTextinput.font_family = "font/D2Coding.ttc"
#directionTextinput = pygame_textinput.TextInput()
#directionTextinput.font_family = "font/D2Coding.ttc"

textinput = pygame_textinput.TextInput()
textinput.font_family = "font/D2Coding.ttc"

# 다음으로 넘길 전역 변수
currentStation = '' # 다음역
line = 0 # 호선
direction = -1 #방향(상행=1, 하행=0)

# guide 메시지
textMsg = ''

def main(): 
  curFlag = True
  lineFlag = False
  directionFlag = False
  # 메인 루프
  while True:
    events = pygame.event.get()

    for event in events:
      # 이벤트를 처리하는 부분
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
 
    # 키보드 이벤트 처리
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          exit()
        if event.key == K_RETURN:          
          if curFlag:
            currentStation = textinput.get_text()
            curFlag = False
            lineFlag = True
            textinput.input_string = ''
          elif lineFlag:
            line = int(textinput.get_text())
            lineFlag = False
            directionFlag = True
            textinput.input_string = ''
          elif directionFlag:
            direction = int(textinput.get_text())
            directionFlag = False
            textinput.input_string = ''
            #TODO: 다음 화면으로 넘어갈 로직 짜기
            
        
      if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
        exit() #end of line for loop...

    screen.fill(BLACK)  # 화면을 검은색으로 지운다
 
    # custom 메소드 호출, textinput 그려준다.
    render_text(events)			# 100 line

    # 텍스트 오브젝트를 출력
    if curFlag:
      textMsg = '현재역: '
    elif lineFlag:
      textMsg = '호선: '
    elif directionFlag:
      textMsg = '우측=상행선이면 1 아니면 0: '

    message_to_screen(textMsg, WHITE, textPointCurStation)
 
    pygame.display.flip()  # 화면 전체를 업데이트
    clock.tick(TARGET_FPS)  # 프레임 수 맞추기

def get_current_station():
  return currentStation

def text_objects(text, color):
  textSurface = fontObj.render(text, True, color)
  return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, p):
  textSurf, textRect = text_objects(msg, color)
  textRect.center = (p[0], p[1])
  screen.blit(textSurf, textRect)

def render_text(events):
  # Feed it with events every frame
  textinput.update(events)

  # 점 찍힐 위치 설정 
  if curFlag:
    point = textInputPointCurStation
  elif lineFlag:
    point = textInputPointLine
  elif directionFlag: 
    point = textInputPointDirection

  # Blit its surface onto the screen
  screen.blit(textinput.get_surface(), point)

if __name__ == "__main__":
  main()
