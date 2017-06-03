# -*- coding: utf-8 -*-
 
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
 
# 라이브러리 및 디스플레이 초기화
pygame.init()

screenWidth = 1680
screenHeight = 1080
screen = pygame.display.set_mode((screenWidth, screenHeight), FULLSCREEN | DOUBLEBUF)
 
# 폰트 로딩 및 텍스트 객체 초기화
fontObj = pygame.font.Font("font/D2Coding.ttc", 32)

# Create TextInput-object
textinput = pygame_textinput.TextInput()
textinput.font_family = "font/D2Coding.ttc"
# 사운드 파일을 로딩
#soundObj = pygame.mixer.Sound('music.mp3')
currentStation = ''

def main(): 
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
          currentStation = textinput.get_text()

      if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
        exit()

    

    screen.fill(BLACK)  # 화면을 검은색으로 지운다
 
    # Feed it with events every frame
    textinput.update(events)
    # Blit its surface onto the screen
    screen.blit(textinput.get_surface(), (500, 200))

    # 텍스트 오브젝트를 출력
    message_to_screen('현재 역 이름: ', WHITE)
 
    pygame.display.flip()  # 화면 전체를 업데이트
    clock.tick(TARGET_FPS)  # 프레임 수 맞추기

def get_current_station():
  return currentStation

def text_objects(text, color):
  textSurface = font.render(text, True, color)
  return textSurface, textxSurface.get_rect()

def message_to_screen(msg, color):
  textSurf, textRect = text_objects(msg, color)
  textRect.center = (350, 223)
  screen.blit(textSurf, textRect)

if __name__ == "__main__":
    main()
