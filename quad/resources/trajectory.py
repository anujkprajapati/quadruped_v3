import math
import numpy as np


class Path:
    def __init__(self):
        pass
    

    # def get_location(odd,n_step,count,posx):
        
    #     stride = 0.05
    #     height = 0.03
    #     # basex = n_step/count * stride
    #     basex = posx + stride
    #     theta = n_step%count * np.pi
    #     if odd ==0:
    #         # zdirection
    #         h2z = 0.05
    #         h3z = 0.05
    #         h1z = 0.05 + height*np.sin(theta)
    #         h4z = 0.05 + height*np.sin(theta)

    #         #xdirection
    #         h1x = basex + 0.102 - stride/2 * np.cos(theta)
    #         h4x = basex - 0.102 - stride/2 * np.cos(theta)
    #         h2x = basex + 0.102
    #         h3x = basex - 0.102

    #     else: 
    #         # zdirection
    #         h1z = 0.05
    #         h4z = 0.05
    #         h2z = 0.05 + height*np.sin(theta)
    #         h3z = 0.05 + height*np.sin(theta)

    #         #xdirection
    #         h2x = basex + 0.102 - stride/2 * np.cos(theta)
    #         h3x = basex - 0.102 - stride/2 * np.cos(theta)
    #         h1x = basex + 0.102
    #         h4x = basex - 0.102
    #     # print(f'the count is{count}')
    #     return h1x, h2x, h3x, h4x, h1z, h2z, h3z, h4z


    def inv2d(self,x,y):
        a=0.1
        b=0.1
        
        maxdist = a**2 + b**2
        dist2 = np.clip(x**2 + y**2, 0, maxdist)
        theta3 = np.round(np.arccos((dist2 - maxdist)/(2*a*b)),4)
        theta2 = np.round((np.arctan2(y,x) - b*np.sin(theta3)/(a+b*np.cos(theta3))),4)
        return theta2, theta3
    
    def invkin(self,x,y,z,leg):
        if leg==1:
            X = (x-0.1)/0.1
            theta1 = np.round(np.arctan2((y+0.05),z),4)
            Z = z/0.1/np.cos(theta1)
            theta2, theta3 = self.inv2d(X,Z)
            return theta1, theta2 - 0.5, theta3 + 1
        elif leg==2:
            X = (x-0.1)/0.1
            theta1 = np.round(np.arctan2((y-0.05),z),4)
            Z = z/0.1/np.cos(theta1)
            theta2, theta3 = self.inv2d(X,Z)
            return theta1, theta2 - 0.5, theta3 + 1
        elif leg ==3:
            X = (x+0.1)/0.1
            theta1 = np.round(np.arctan2((y+0.05),z),4)
            Z = z/0.1/np.cos(theta1)
            theta2, theta3 = self.inv2d(X,Z)
            return theta1, theta2 + 0.5, theta3 - 1
        elif leg ==4:
            X = (x+0.1)/0.1
            theta1 = np.round(np.arctan2((y+0.05),z),4)
            Z = z/0.1/np.cos(theta1)
            theta2, theta3 = self.inv2d(X,Z)
            return theta1, theta2 + 0.5, theta3 -1

    def get_pt(self,h,h0,k,k0,height, theta,leg):
        l =0.005
        if theta<100:
            
            if leg==1 or leg==4:
                th = theta*np.pi /100
            else: 
                th = 0

        else:
            if leg==3 or leg==2:
                th = (theta-100)*np.pi/100
            else:
                th=0

        x = h + h0*np.cos(th)
        y = k + k0*np.cos(th)
        z = l + height*np.sin(th)
        return x,y,z











        