# -*- coding: utf-8 -*-
import os 
import sys
import pygame
import pygame_textinput
import shortest_path as sp
import json
from pygame.locals import *
import threading 

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
textPointCurStation = (565, 100) # 현재 역 550
textPointCurStaNumber = (348, 100) # 현재 역 550
textPointPrevStation = (320, 400) # prev
textPointNextStation = (710, 400) # next

# 폰트 로딩 및 텍스트 객체 초기화
fontObj = pygame.font.Font("font/D2Coding.ttc", 80)
fontMediumObj = pygame.font.Font("font/D2Coding.ttc", 56)
fontSmallObj = pygame.font.Font("font/D2Coding.ttc", 32)

fp = open('datas/data.json', 'r')
initData = json.loads(fp.read())    
fp.close()

initStation = initData["curStation"]
initLine = initData["line"]
initDirection = initData["direction"]

prevStation = '의왕'
nextStation = '화서'

direction = MIDDLE
isShown = False
def main(): 
  # 메인 루프
  global isShown
  global direction
  
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
        elif event.key == K_m:
          isShown = True
          direction = MIDDLE
          direction = sp.speak_destination(initStation, initLine, initDirection)
        else:
          direction = MIDDLE
    ################ Handle Events ###################    
    #start_timer()
    
    if isShown and (direction != MIDDLE):
      timer=threading.Timer(1, start_timer)
      timer.start()
      isShown = False

#    if direction == LEFT:
#      render_go_left_image()
#    elif direction == RIGHT:
#      render_go_right_image()
    
 
    # custom 메소드 호출, textinput 그려준다.
#    render_text(events)			# 100 line

   
#    render_arrow()
    render_base_images();
    message_to_screen(initStation, WHITE, textPointCurStation, 0)
    message_to_screen(nextStation, WHITE, textPointNextStation, 2)
    message_to_screen(prevStation, WHITE, textPointPrevStation, 2)
    message_to_screen("153", WHITE, textPointCurStaNumber, 1)
 
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

leftArrow = (100, 600)
leftAngle = 0
rightArrow = (709, 600)
rightAngle = 180
middleMic = (250, 600)
#posCircle = (screenHeight/2, screenWidth/2)


posBlank = (300, 50)
posStationName = (230, 220)
posCircle = (230, 320)
posTellDestination = (330, 450)
posMic = (479, 615)

def render_go_right_image():
  screen.blit(get_image('images/gray.png', leftAngle), leftArrow)
  screen.blit(get_image('images/red.png', rightAngle), rightArrow)

def render_go_left_image():
  screen.blit(get_image('images/red.png', leftAngle), leftArrow)
  screen.blit(get_image('images/gray.png', rightAngle), rightArrow)

def render_base_images():
  screen.blit(get_image('images/blank_circle.png', 0), posBlank)
  screen.blit(get_image('images/sta_name.png', 0), posStationName)
  screen.blit(get_image('images/circle.png', 0), posCircle)
  screen.blit(get_image('images/text_tell_destination.png', 0), posTellDestination)
  screen.blit(get_image('images/mic.png', 0), posMic)

def text_objects(text, color, size):	#size는 작을수록 크다.
  if size == 0:
    textSurface = fontObj.render(text, True, color)
  elif size == 1:
    textSurface = fontMediumObj.render(text, True, color)
  else:
    textSurface = fontSmallObj.render(text, True, color)
  return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, p, isCurrent):
  textSurf, textRect = text_objects(msg, color, isCurrent)
  textRect.center = (p[0], p[1])
  screen.blit(textSurf, textRect)

count = 0
def start_timer():
  global count
  count += 1
  
  if direction == LEFT:
    render_go_left_image()
  elif direction == RIGHT:
    render_go_right_image()

  if count == 5:
    isShown = False
    count = 0
    timer.cancel()

if __name__ == "__main__":
  main()
