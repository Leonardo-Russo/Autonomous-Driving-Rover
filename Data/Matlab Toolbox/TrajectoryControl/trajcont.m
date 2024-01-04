clear all

%%%%
%% Trajectory Control
%%%%

%%% Moving to a point
%%%% Note: Initially it did not work properly. It required negative Kh, it
%%%% started to work fine when I copied angdiff from common folder. By
%%%% default the toolbox uses the following subroutine:
%%%% /Applications/MATLAB_R2020b.app/toolbox/shared/robotics/robotutils/angdiff.m
%%%% /Applications/MATLAB_R2020b.app/toolbox/shared/robotics/robotutils/+robotics/+internal/angdiff.m  % static method or package function
%%%% In the second subroutine, the difference is done y-x instead of x-y.
sl_drivepoint
xg = [5 5];
x0 = [8 5 pi/2];
r=sim('sl_drivepoint');

%%% Following a line
%%%% It works fine, although in the toolbox is implemented to follow the
%%%% trajectory in the opposite direction. This means +Kd*d and
%%%% atan2(a,-b).
sl_driveline
L = [1 -2 4];
x0 = [8 5 pi/2];
r=sim('sl_driveline');

%%% Following a moving target/trajectory
%%%% It works fine
sl_pursuit
r=sim('sl_pursuit');
q=r.find('y');
t=r.find('t');
for i=1:length(t)-1
    acc(i)=(q(i+1,6)-q(i,6))/(t(i+1)-t(i));
end
    
figure(1)
plot(t,q(:,6))

figure(2)
plot(t(1:length(t)-1),acc)

%%%% Rerun sl_pursuit by zeroing out the integral gain coefficient
r=sim('sl_pursuit');
q1=r.find('y');
t1=r.find('t');
for i=1:length(t1)-1
    acc1(i)=(q1(i+1,6)-q1(i,6))/(t1(i+1)-t1(i));
end

figure(1)
hold on
plot(t1,q1(:,6))

figure(2)
hold on
plot(t1(1:length(t1)-1),acc1)


%%% Moving to a pose
%%%% It works fine, although in the toolbox is implemented to follow the
%%%% trajectory in the opposite direction. This means +Kd*d and
%%%% atan2(a,-b).
sl_drivepose
xg = [5 5 pi/2];
x0 = [9 5 0];
r=sim('sl_drivepose');