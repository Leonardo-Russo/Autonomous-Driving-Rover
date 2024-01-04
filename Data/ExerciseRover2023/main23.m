%% ROVER FINAL EXERCISE (a.a. 2023-2024)
clear
clc
load('exercise.mat')

%% NOTE
% The 2D Cartesian landmarks coordinates are defined by the vectors
% (xLM, yLM). The vectors Xvec and Yvec are used to get georeferenced maps
% (e.g., hazard map).

%%
%%% To compute the row and column indices (i,j) associated with a point of
%%% the map from its Cartesian coordinates (x0,y0), you can use the
%%% following piece of code

mapRes = 10; % m resolution of the map (at the pole)

%%% Example
x0 = 0; % m
y0 = 0; % m

j = (x0 - X(1,1) + mapRes)/mapRes; % column index
i = (Y(1,1) - y0 + mapRes)/mapRes; % row index

%%% Note that X(i,j) = x0, Y(i,j) = y0
X(i,j)
Y(i,j)

%%
%%% Map of the environment
figure()
imshow(map,'XData',Xvec,'YData',Yvec);
set(gca,'Ydir','normal')
axis on
grid on
xlabel('X')
ylabel('Y')

%%
%%% Obstacle map
%%% NOTE: this is the map to be used for the path planning task by using
%%%       the A* algorithm
figure();
imshow(obstacleMap,'XData',Xvec,'YData',Yvec);
hold on
set(gca,'Ydir','normal')


%%
%%% Landamrks
figure()
imshow(map,'XData',Xvec,'YData',Yvec);
set(gca,'Ydir','normal')
hold on
plot(xLM,yLM,'yo','markersize',5,'linewidth',2)


