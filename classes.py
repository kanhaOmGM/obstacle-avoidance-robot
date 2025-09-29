import numpy as np
import math
import pygame

def distance(pt1, pt2):
    pt1= np.array(pt1)
    pt2= np.array(pt2)
    return np.linalg.norm(pt1-pt2)

class robot:
    def __init__(self, startpos, width):

        self.m2p= 3779.52 #standard per meter to pixels

        #robot dimensions
        self.w = width
        self.x= startpos[0]
        self.y= startpos[1] 
        self.heading= 0 #robot's orientation in radia

        self.vl= 0.01*self.m2p #meters/sec
        self.vr= 0.01*self.m2p #meters/sec

        self.maxspeed= 0.03*self.m2p #predefined min and max speed
        self.minspeed= 0.03*self.m2p
        self.min_obs_dis= 100
        self.count_down= 5 #s
         # Obstacle avoidance parameters
        
    
    def avoid_obst(self, pts_cloud, dt):

        closest_obs= None
        dist= np.inf #dist from robot to be infinie

        if len(pts_cloud) > 1 :
            for pt in pts_cloud:
                current_dist = distance([self.x, self.y], pt)
                if dist > current_dist:
                    dist= distance([self.x, self.y], pt)
                    closest_obs = (pt, dist)
            if closest_obs[1]< self.min_obs_dis and self.count_down>0:
                self.count_down-=dt
                self.move_backward()
            
            else:
                self.count_down= 5
                self.move_for()

            # The correct approach is to use the count_down variable to manage a state machine. The robot should only attempt to move 
            # forward if the timer has fully reset and there are no obstacles nearby. Otherwise, it should continue its avoidance
            # #  maneuver until the timer is at zero.
            # if self.avoiding:
            #     if self.count_down > 0:
            #         self.count_down -= dt
            #         self.move_backward()
            #     else:
            #         # backoff finished
            #         self.avoiding = False
            #         self.move()
            # else:
            #     # if obstacle too close → start avoidance
            #     if closest_obs and closest_obs[1] < self.min_obs_dis:
            #         self.avoiding = True
            #         self.count_down = 2  # backoff time (seconds)
            #         self.move_backward()
            #     else:
            #         self.move()


    def move_backward(self):
        # making it move backwards ub circular trajectory
        self.vr= -self.minspeed
        self.vl= -self.minspeed/2
    
    def move_for(self):
        self.vr= self.minspeed
        self.vl= self.minspeed

    def kinematics(self, dt):

        self.x+= ((self.vl+self.vr)/2)*math.cos(self.heading) * dt
        self.y-= ((self.vl+self.vr)/2)*math.sin(self.heading) * dt #to account for the inverted world frame of computer y axis inverted
        self.heading+= (self.vr - self.vl)/self.w * dt

        if self.heading > 2*math.pi or self.heading<-2*math.pi:
            self.heading= 0

        self.vr= max(min(self.maxspeed, self.vr), self.minspeed)
        self.vl= max(min(self.maxspeed, self.vl), self.minspeed)

        
class graphics:
    def __init__(self, dimensions, robot_img, map_img):
        pygame.init()

        self.black= (0,0,0)
        self.white= (255,255,255)
        self.red= (255,0,0)
        self.green= (0,255,0)
        self.blue= (0,0,255)
        self.yellow= (255,255,0)
        

        #load imgs
        self.robot = pygame.image.load(robot_img)
        self.m_img = pygame.image.load(map_img)

        #dimensions
        self.dimensions = dimensions
        self.height, self.width= self.dimensions

        #window
        self.map= pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.m_img, (0,0))

    def draw_robot(self, x , y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect= rotated.get_rect(center= (x,y))
        self.map.blit(rotated, rect)

        # def sensor_reading(self, pts_cloud):
        #     for pt in pts_cloud:
        #         pygame.draw.circle(self.map, self.blue, pt, 3, 0)

class ultrasonicsensor:

    def __init__(self, sensor_r, map):
        self.sensor_r= sensor_r
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map
    
    def sense_obstacles(self, x, y, heading):
        
        obstacles= []
        x1, y1 = x, y
        #start angle
        s_angle = heading - self.sensor_r[1]
        #final angle, their difference is the ark of sweep by the sensor
        f_angle= heading + self.sensor_r[1]

        for angle in np.linspace(s_angle, f_angle, 10, False):

            x2 = x1 + self.sensor_r[0]*math.cos(angle)
            y2= y1 - self.sensor_r[0]*math.sin(angle)

            for i in range(0,100):
                u = i/100
                x= int(x2 *u + x1*(1-u))
                y= int(y2 *u + y1*(1-u))

                if 0 < x <self.map_width and 0< y < self.map_height:
                    color= self.map.get_at((x, y))
                    self.map.set_at((x,y), (0,245,233))

                    if (color[0],color[1],color[2]) == (0, 0, 0):
                        obstacles.append([x,y])
                        break
        return obstacles


