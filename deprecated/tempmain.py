# -*- coding: utf-8 -*-
 
import sys
import pygame
from pygame.locals import *
 
# 초당 프레임수를 정의
TARGET_FPS = 30
 
clock = pygame.time.Clock()
 
 
# 색 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
 
# 마우스 버튼 인덱스 정의
LEFT = 1  # 왼쪽 버튼에 대한 버튼 인덱스
RIGHT = 3  # 오른쪽 버튼에 대한 버튼 인덱스
 
# 라이브러리 및 디스플레이 초기화
pygame.init()
screen = pygame.display.set_mode((1080, 720), FULLSCREEN | DOUBLEBUF)
 
# 이미지 파일을 로딩
#img = pygame.image.load('images/image.jpg')
rightArrow = pygame.image.load('images/arrow.png') 
rightRedArrow = pygame.image.load('images/arrow_red.png')

# 폰트 로딩 및 텍스트 객체 초기화
fontObj = pygame.font.Font('font/HUDaku.ttf', 32)
textSurfaceObj = fontObj.render('Hello Font!', True, GREEN)
textRectObj = textSurfaceObj.get_rect();
textRectObj.center = (150, 200)

# 사운드 파일을 로딩
#soundObj = pygame.mixer.Sound('music.mp3')

def main(): 
  # 메인 루프
  while True:
    for event in pygame.event.get():
      # 이벤트를 처리하는 부분
      if event.type == QUIT:
          pygame.quit()
        sys.exit()
 
    # 키보드 이벤트 처리
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          exit()
        # 오른쪽 키가 눌리면 사운드를 플레이한다
      #    soundObj.play()
 
    # 마우스 이벤트 처리
    if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
      # 왼쪽 버튼이 눌렸을 때의 처리
      print ("left mouse up (%d, %d)" % event.pos)
    elif event.type == MOUSEBUTTONUP and event.button == LEFT:
      # 왼쪽 버튼이 떨어졌을 때의 처리
      print ("left mouse down (%d, %d)" % event.pos)
    elif event.type == pygame.MOUSEMOTION:
      # 마우스 이동시의 처리
      print ("mouse move (%d, %d)" % event.pos)
 
 
  # 게임의 상태를 업데이트하는 부분
 
  # 게임의 상태를 화면에 그려주는 부분
 
 
  screen.fill(BLACK)  # 화면을 검은색으로 지운다
 
  pygame.draw.rect(screen, GREEN, pygame.Rect(10, 0, 20, 10)) # 두 점을 지나는 선을 그린다
 
  # 수동으로 점 찍기
  pixelArray = pygame.PixelArray(screen)
  pixelArray[5][5] = RED
  pixelArray[10][10] = RED
  del pixelArray
 
  # 이미지 파일 그리기
#  screen.blit(img, (50, 100))
  
  screen.blit(rightArrow, (250, 40))
  screen.blit(rightRedArrow, (50, 40))

  # 이미지 파일 회전하여 그리기
  x = 70
  y = 50
  degree = 0
  deploy_arrow(x, y, rightArrow, degree)
  degree = 180
  deploy_arrow(x, y, rightRedArrow, degree)
#  rotated = pygame.transform.rotate(img, degree)
#  rect = rotated.get_rect()
#  rect.center = (x, y)
#  screen.blit(rotated, rect)
 

  # 텍스트 오브젝트를 출력
  screen.blit(textSurfaceObj, textRectObj)
 
  pygame.display.flip()  # 화면 전체를 업데이트
  clock.tick(TARGET_FPS)  # 프레임 수 맞추기


def deploy_arrow(x, y, img, degree):
  rotated = pygame.transform.rotate(img, degree)  
  rect = rotated.get_rect()
  rect.center = (x, y)
  screen.blit(rotated, rect)

if __name__ == "__main__":
    main()
