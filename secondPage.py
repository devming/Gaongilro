# -*- coding: utf-8 -*-
import os 
import sys
import pygame
import pygame_textinput
from pygame.locals import *

# 초당 프레임수를 정의
TARGET_FPS = 30
 
clock = pygame.time.Clock()
 
MIDDLE = 0
LEFT = 1
RIGHT = 2

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 

# 라이브러리 및 디스플레이 초기화
pygame.init()

screenWidth = 1900#1680
screenHeight = 1024#1080
screen = pygame.display.set_mode((screenHeight, screenWidth), FULLSCREEN | DOUBLEBUF)
 
# 텍스트 좌표
textPointCurStation = (screenHeight/2, 100) # 현재 역 550
textPointNextStation = (150, 300) # next
textPointPrevStation = (950, 300) # prev

# 폰트 로딩 및 텍스트 객체 초기화
fontObj = pygame.font.Font("font/D2Coding.ttc", 128)
fontSmallObj = pygame.font.Font("font/D2Coding.ttc", 32)

def main(): 
  # 메인 루프
  direction = MIDDLE
  while True:
    events = pygame.event.get()

    screen.fill(BLACK)  # 화면을 검은색으로 지운다
    for event in events:
      # 이벤트를 처리하는 부분
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
 
    # 키보드 이벤트 처리
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          exit()

        elif event.key == K_p:
          direction = RIGHT
        elif event.key == K_q:        
          direction = LEFT
        else:
          direction = MIDDLE
        

    if direction == LEFT:
      render_go_left_image()
    elif direction == RIGHT:
      render_go_right_image()
      
 
    # custom 메소드 호출, textinput 그려준다.
#    render_text(events)			# 100 line

   
#    render_arrow()

    message_to_screen(load_cur_text(), WHITE, textPointCurStation, True)
    message_to_screen(load_next_text(), WHITE, textPointNextStation, False)
    message_to_screen(load_prev_text(), WHITE, textPointPrevStation, False)
 
    pygame.display.flip()  # 화면 전체를 업데이트
    clock.tick(TARGET_FPS)  # 프레임 수 맞추기


_image_library = {}
def get_image(path, angle):
  global _image_library
  image = _image_library.get(path)
  if image == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    _image_library[path] = image
  return pygame.transform.rotate(image, angle)

leftArrow = (25, 600)
rightArrow = (625, 600)
middleMic = (250, 600)

leftAngle = 0
rightAngle = 180
def render_go_right_image():
  screen.blit(get_image('images/arrow.png', leftAngle), leftArrow)
  screen.blit(get_image('images/arrow_red.png', rightAngle), rightArrow)

def render_go_left_image():
  screen.blit(get_image('images/arrow_red.png', leftAngle), leftArrow)
  screen.blit(get_image('images/arrow.png', rightAngle), rightArrow)

def text_objects(text, color, isCurrent):
  if isCurrent:
    textSurface = fontObj.render(text, True, color)
  else:
    textSurface = fontSmallObj.render(text, True, color)
  return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, p, isCurrent):
  textSurf, textRect = text_objects(msg, color, isCurrent)
  textRect.center = (p[0], p[1])
  screen.blit(textSurf, textRect)

def load_cur_text():
  textMsg = '사당'
  return textMsg

def load_next_text():
  textMsg = '낙성대'
  return textMsg

def load_prev_text():
  textMsg = '방배'
  return textMsg

if __name__ == "__main__":
  main()
