#! /usr/bin/env python3
import os
import sys
import inspect
import pygame
import time

sCurPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#For Module Libraries
#sys.path.append(sCurPath + '/pyConfig')
sys.path.append(sCurPath + '/pyDebugger')


from Debug import pyDebugger


class pyDrawFBImage():

   def __init__(self):
      self.Debugger = pyDebugger(self,True,False)
      self.Debugger.Log("Starting pyDrawFBImage...For drawing to framebuffer devices...")
      self.Debugger.__LogToFile = False #self.Config.Get("Debug_File")
      self.FBDev = "/dev/fb0"
      if not self.CheckDisplay():
         self.Debugger.Log("Failed to find suitable video drivers...Exiting...")
         sys.exit()
      else:
         self.Debugger.Log("Initializing framebuffer driver...")
         self.FBSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
         self.Debugger.Log("Size of display set w(" + str(self.FBSize[0]) + "), h(" + str(self.FBSize[1]) + ")...")
         self.FBScreen = pygame.display.set_mode(self.FBSize, pygame.FULLSCREEN)
         self.Debugger.Log("Screen set...")
         self.Debugger.Log("Initializing font module...")
         pygame.font.init()

   def CheckDisplay(self):
      disp_no = os.getenv('DISPLAY')
      self.Debugger.Log("Checking for display type...")
      if disp_no:
         self.Debugger.Log("Running X...This is for framebuffers...")
      else:
         self.Debugger.Log("We're Not running X...Check for framebuffers...")
         drivers = ['directfb', 'fbcon', 'svgalib']
         self.Debugger.Log("Attempting to set frame buffer device...")
         os.putenv('SDL_FBDEV', self.FBDev)
         if os.getenv('SDL_FBDEV') == self.FBDev:
            self.Debugger.Log("Framebuffer device set correctly...")
         else:
            self.Debugger.Log("Framebugger device set to '" + str(os.getenv('SDL_FBDEV')) + "', could not change!")
         bFound = False
         for driver in drivers:
             if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
             try:
                pygame.display.init()
                bFound = True
                self.Debugger.Log("Using " + str(driver) + " framebuffer driver...")
                break
             except pygame.error:
                self.Debugger.Log("Driver: " + str(driver) + " failed...")
                continue

         if not bFound:
            self.Debugger.Log("No suitable video drivers found!")
            return False
         else:
            return True

   def DrawImg(self, ImgPath):
      self.Debugger.Log("Loading Image...", endd="")
      self.Img = pygame.image.load(ImgPath)
      self.Debugger.Log("Success!")
      self.ImgRect = self.Img.get_rect()
      self.Debugger.Log("Image Attributes (" + str(self.ImgRect) + ")")
      self.FBScreen.blit(self.Img, self.ImgRect)
      pygame.display.flip()

   def DrawText(self, sText,rLocation=(300,300), sFont="monospace",iFontSize=15,iColor=(255,255,255),vCenter=False,hCenter=False,bClear=False):
      pyGFont = pygame.font.SysFont(sFont,iFontSize)
      lblText = pyGFont.render(sText,1,iColor)
      if vCenter:
         rLocation = (rLocation[0], (self.FBSize[1] / 2) - (lblText.get_rect().height / 2))
      if hCenter:
         rLocation = ((self.FBSize[0] / 2) - (lblText.get_rect().width / 2), rLocation[1])
      #if bClear:
      
      self.FBScreen.blit(lblText,rLocation)
      pygame.display.flip()

   def FillScreen(self, sColor):
      self.FBScreen.fill(sColor)



if __name__ == '__main__':
   c = pygame.time.Clock()
   c.tick(3)
   #Main program loop
   while True:
      DFBI = pyDrawFBImage()
      DFBI.FillScreen([0,0,0])
      DFBI.DrawImg("/opt/PiStat/temp/fbi1.png")
      #pygame.display.flip()
      time.sleep(2)
      #break
