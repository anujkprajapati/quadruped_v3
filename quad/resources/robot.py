import pybullet as p
import numpy as np
import os
from quad.resources.trajectory import Path


class Robot:
    def __init__(self,client):
        self.client = client
        f_name = os.path.join(os.path.dirname(__file__), 'custom_robot.urdf')
        self.robot = p.loadURDF(fileName=f_name, basePosition=[0,0,0.205], physicsClientId=client)
        self.jointArray = [1,2,3,5,6,7,10,11,12,14,15,16]
        # self.end_eff = [4,8,13,17]
        self.path = Path()
        
    def get_ids(self):
        return self.client, self.robot
    
    def apply_action(self,action,theta):
        #action is SL, phi, height for each leg
        #use IK to calculate joint angles for each leg: target = list of 12 floats
        # 
        # target1 = p.calculateInverseKinematics(self.robot, self.end_eff[i],)
        # 
        # print(f'welcome to apply action')
        SL1 = action[0]
        SL2 = action[3]
        SL3 = action[6]
        SL4 = action[9]
        phi1 = np.round(action[1],4)
        phi2 = np.round(action[4],4)
        phi3 = np.round(action[7],4)
        phi4 = np.round(action[10],4)
        height1 = action[2]
        height2 = action[5]
        height3 = action[8]
        height4 = action[11]

        h01 = SL1/2*np.cos(phi1)
        h02 = SL2/2*np.cos(phi2)
        h03 = SL4/2*np.cos(phi3)
        h04 = SL4/2*np.cos(phi4)
        k01 = SL1/2*np.sin(phi1)
        k02 = SL2/2*np.sin(phi2)
        k03 = SL3/2*np.sin(phi3)
        k04 = SL4/2*np.sin(phi4)
        pos,_, ha,hb,hc,hd = self.get_location()
        # get_obs hx1,hx2...posx,posy,etc
        posx = pos[0]
        posy = pos[1]
        hx1 = ha[0]
        hx2 = hb[0]
        hx3 = hc[0]
        hx4 = hd[0]
        hy1 = ha[1]
        hy2 = hb[1]
        hy3 = hc[1]
        hy4 = hd[1]

        h1 = hx1-posx + h01
        h2 = hx2-posx + h02
        h3 = hx3-posx + h03
        h4 = hx4-posx + h04

        k1 = hy1-posy + k01
        k2 = hy2-posy + k02
        k3 = hy3-posy + k03
        k4 = hy4-posy + k04

        # l = 0.005
        

        x1,y1,z1 = self.path.get_pt(h1, h01, k1, k01, height1, theta,1)
        x2,y2,z2 = self.path.get_pt(h2, h02, k2, k02, height2, theta,2)
        x3,y3,z3 = self.path.get_pt(h3, h03, k3, k03, height3, theta,3)
        x4,y4,z4 = self.path.get_pt(h4, h04, k4, k04, height4, theta,4)


        target1 = self.path.invkin(x1,y1,z1,1)
        target2 = self.path.invkin(x2,y2,z2,2)
        target3 = self.path.invkin(x3,y3,z3,3)
        target4 = self.path.invkin(x4,y4,z4,4)
        
        target = target1 + target2 + target3 + target4
        # print(f'the target is {target}')

        p.setJointMotorControlArray(self.robot, self.jointArray, controlMode=p.POSITION_CONTROL,
            targetPositions=target, physicsClientId=self.client)

        p.stepSimulation()
        
        
        
    def get_location(self):
        pos,ori = p.getBasePositionAndOrientation(self.robot, self.client)
        h1 = p.getLinkState(self.robot,4, self.client)[0]
        h2 = p.getLinkState(self.robot,8, self.client)[0]
        h3 = p.getLinkState(self.robot,13, self.client)[0]
        h4 = p.getLinkState(self.robot,17, self.client)[0]
        orient = p.getEulerFromQuaternion(ori)
        orientation = np.round(orient,4)
        return pos,orientation,h1,h2,h3,h4

        
    def get_obs(self):
        status = p.getJointStates(self.robot, self.jointArray,physicsClientId=self.client)
        linear,_ = p.getBaseVelocity(self.robot, self.client)
        obs = [t[0] for t in status]

        return obs, linear