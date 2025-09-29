import math
import pygame
from classes import ultrasonicsensor,graphics,robot

MAP_DIMENSIONS = (600, 1200)


#graphic of env

gfx= graphics(MAP_DIMENSIONS,'robot.png' ,'ROOM.png')

#lets position robot at
start = (100, 200)
#size of robot
bot= robot(start,0.0025*3779.52 )


#initialising the sensor
sensor= 250, math.radians(40)

sonic= ultrasonicsensor(sensor, gfx.map)

dt= 0
clock = pygame.time.Clock()

running= True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
    
    dt= clock.tick()/1000
    last_t= pygame.time.get_ticks()

    gfx.map.blit(gfx.m_img, (0,0))
    
    bot.kinematics(dt)

    gfx.draw_robot(bot.x, bot.y, bot.heading)
    pts_cloud= sonic.sense_obstacles(bot.x, bot.y, bot.heading)

    bot.avoid_obst(pts_cloud, dt)

    #gfx.sensor_reading(pts_cloud)
    pygame.display.flip()