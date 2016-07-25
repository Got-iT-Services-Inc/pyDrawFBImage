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

   class pySprite(pygame.sprite.Sprite):

      def __init__(self,sImg="",sColor=(0,0,0),sRect=(0,0,0,0)):
         super().__init__()
         self.imgLoc = sImg
         self.color = sColor
         self.rect = None
         print ("pySprite: sRect: " + str(self.rect))
         self.update(sRect)

      def update(self,sLocation=(0,0)):
         if self.imgLoc != "":
            self.image = pygame.image.load(self.imgLoc).convert()
            rTmp = self.image.get_rect().size
            self.rect = (sLocation[0],sLocation[1],sLocation[0] + rTmp[0], sLocation[1] + rTmp[1])
         else:
            self.image = pygame.Surface(self.rect)
            self.image.fill(self.color)
            rTmp = self.image.get_rect().size()
            self.rect = (sLocation[0],sLocation[1],sLocation[0] + rTmp[0], sLocation[1] + rTmp[1])
         self.rect = pygame.Rect(self.rect)


   class pyText(pygame.sprite.Sprite):

      def __init__(self,dScreen,rLocation,sText,sSize,cColor,sFont="Arial",bCenter=True,bAntialias=True,
        OffSet=(0,0),bBold=False):
         #self.Debugger = pyDebugger(self,True,False)
         #self.Debugger.Log("Initializing Text Sprite...\n  *Text: " + sText + "\n  *Size: " + str(sSize) +
         #   "\n  *Color: " + str(cColor) + "\n  *Font: " + sFont + "\n  *Location: " + str(rLocation[0]) +
         #   "(W) " + str(rLocation[1]) + "(H)")
         super().__init__()
         self.font = pygame.font.SysFont(sFont, sSize,bold=bBold)
         self.color = cColor
         self.text = sText
         self.pos = rLocation
         self.screen = dScreen
         self.offset = OffSet
         self.antialias = bAntialias
         self.center = bCenter
         self.update()

      def update(self):
         self.image = self.font.render(self.text, self.antialias, self.color)
         self.rect = self.image.get_rect()
         if self.center == True:
            self.rect.x = (self.pos[0]/2) - (self.rect.width/2) + self.offset[0]
            self.rect.y = (self.pos[1]/2) - (self.rect.height/2) + self.offset[1]
         else:
            self.rect.x = self.pos[0] + self.offset[0]
            self.rect.y = self.pos[1] + self.offset[1]

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
         self.All_Sprites = pygame.sprite.Group()
         self.gBackground = None
         self.clock = pygame.time.Clock()
         self.clock.tick(1)

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


   def DrawBackgroundImg(self, ImgPath, bUpdateScreen = True):
      self.Debugger.Log("Loading Background Image...", endd="")
      try:
         self.gBackground = pygame.image.load(ImgPath)
      except Exception as e:
         self.Debugger.Log("Failed!")
         self.Debugger.Log(str(e))
         return False
      self.Debugger.Log("Success!")
      self.Debugger.Log("Background Image Attributes (" + str(self.gBackground.get_rect()) + ")")
      self.FBScreen.blit(self.gBackground, self.gBackground.get_rect())
      if bUpdateScreen:
         pygame.display.flip()

   def DrawImg(self, ImgPath,sLocation=(0,0)):
      self.Debugger.Log("Loading Image...", endd="")
      iTmp = pygame.image.load(ImgPath)
      iTmp.x = sLocation[0]
      iTmp.y = sLocation[0]
      self.All_Sprites.add(iTmp)
      iTmp.draw()
      self.Debugger.Log("Success!")

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

   def FillSurface(self,sSize, sColor):
      sTmp = pygame.Surface(sSize)
      sTmp.fill(sColor)
      return sTmp

   def Update(self):
      if self.gBackground != None:
         self.FBScreen.blit(self.gBackground, self.gBackground.get_rect())
         
      self.All_Sprites.draw(self.FBScreen)
      #self.Debugger.Log("Count" + str(len(self.All_Sprites)))
      #pygame.display.flip()



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
