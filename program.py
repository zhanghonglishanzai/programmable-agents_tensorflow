import tensorflow as tf 
import numpy as np
import math

# Parameter
order_num=2;

class Program:
  def __init__(self,sess,state_dim,obj_num,fea_size,Theta,program_order,postfix):
    self.sess = sess;
    self.state_dim = state_dim;
    self.fea_size=fea_size;
    self.obj_num=obj_num;
    self.order_num=order_num;
    self.Theta=Theta;
    self.program_order=program_order;
    self.postfix=postfix;
    self.p = self.compile_order();

  def compile_order(self):
    self.Theta=tf.reshape(self.Theta,[-1,self.obj_num,6]);
    self.Theta=tf.transpose(self.Theta,perm=[0,2,1]);
    self.Theta=tf.unstack(self.Theta,6,1);
    # temporary ordering
    p_1=tf.multiply(self.Theta[0],self.Theta[3]);
    p_1=p_1+self.Theta[5];
    p_2=tf.multiply(self.Theta[1],self.Theta[3]);
    p_2=p_2+self.Theta[5];
    p_3=tf.multiply(self.Theta[0],self.Theta[4]);
    p_3=p_3+self.Theta[5];
    p_4=tf.multiply(self.Theta[1],self.Theta[4]);
    p_4=p_4+self.Theta[5];
    program_order2=tf.unstack(self.program_order,(self.obj_num-1),1);
    p=tf.multiply(tf.stack([program_order2[0]]*(self.obj_num),1),p_1)+tf.multiply(tf.stack([program_order2[1]]*(self.obj_num),1),p_2)+tf.multiply(tf.stack([program_order2[2]]*(self.obj_num),1),p_3)+tf.multiply(tf.stack([program_order2[3]]*(self.obj_num),1),p_4);
    
    # Currently tf.cond makes problems 
    """
    program_order2=tf.unstack(self.program_order,self.order_num,1);
    for i in range(self.order_num):
      program_order2[i]=tf.unstack(program_order2[i],3,1);
    for i in range(self.order_num):
      for k in range(9):
        for l in range(k+1,9):
          # not=1, and=2, or=3
          p=tf.cond(tf.equal(program_order2[i][0],1)&tf.equal(program_order2[i][1],k),lambda:1-self.Theta[k],lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],1)&tf.equal(program_order2[i][1],-1),lambda:1-p,lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],2)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:tf.multiply(self.Theta[k],self.Theta[l]),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],2)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],-1),lambda:tf.multiply(self.Theta[k],p),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],3)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:self.Theta[k]+self.Theta[l]-tf.multiply(self.Theta[k],self.Theta[l]),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],3)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:self.Theta[k]+p-tf.multiply(self.Theta[k],p),lambda:p);
    """
    return p;
		
  def run_target_nets(self,Theta,program_order):
    Theta=tf.reshape(Theta,[-1,self.obj_num,6]);
    Theta=tf.transpose(Theta,perm=[0,2,1]);
    Theta=tf.unstack(Theta,6,1);
    # temporary ordering
    p_1=tf.multiply(Theta[0],Theta[3]);
    p_1=p_1+Theta[5];
    p_2=tf.multiply(Theta[1],Theta[3]);
    p_2=p_2+Theta[5];
    p_3=tf.multiply(Theta[0],Theta[4]);
    p_3=p_3+Theta[5];
    p_4=tf.multiply(Theta[1],Theta[4]);
    p_4=p_4+Theta[5];
    program_order2=tf.unstack(program_order,(self.obj_num-1),1);
    p=tf.multiply(tf.stack([program_order2[0]]*(self.obj_num),1),p_1)+tf.multiply(tf.stack([program_order2[1]]*(self.obj_num),1),p_2)+tf.multiply(tf.stack([program_order2[2]]*(self.obj_num),1),p_3)+tf.multiply(tf.stack([program_order2[3]]*(self.obj_num),1),p_4);
    
    # Currently tf.cond makes problems 
    """
    # Currently tf.cond makes problems 
    program_order2=tf.unstack(program_order,self.order_num,1);
    for i in range(self.order_num):
      program_order2[i]=tf.unstack(program_order2[i],3,1);
    for i in range(self.order_num):
      for k in range(9):
        for l in range(k+1,9):
          # not=1, and=2, or=3
          p=tf.cond(tf.equal(program_order2[i][0],1)&tf.equal(program_order2[i][1],k),lambda:1-Theta[k],lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],1)&tf.equal(program_order2[i][1],-1),lambda:1-p,lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],2)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:tf.multiply(Theta[k],Theta[l]),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],2)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],-1),lambda:tf.multiply(Theta[k],p),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],3)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:Theta[k]+Theta[l]-tf.multiply(Theta[k],Theta[l]),lambda:p);
          p=tf.cond(tf.equal(program_order2[i][0],3)&tf.equal(program_order2[i][1],k)&tf.equal(program_order2[i][2],l),lambda:Theta[k]+p-tf.multiply(Theta[k],p),lambda:p);
    """
    return p;
