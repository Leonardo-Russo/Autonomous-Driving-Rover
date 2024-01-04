clear all

%%%%
%% Localization 
%%%%

%%% Dead reckoning
%%% Measurement errors
sigmad = 0.02;        % distance traveled (m)
sigmat = 0.5*pi/180;  % change in heading (rad)
V = [sigmad^2 0; 0 sigmat^2];

%%% Toolbox vehicle superclass
veh = Bicycle('covar',V)

%%% Simulate the motion over one time step
%%% with specified velocity 1 m s^-1 and steering angle of 0.3 rad
odo = veh.step(1, 0.3);                                                     %%% Sample interval default 0.1 s
%%% The reported values are the odometer reading, including noise. The
%%% robot's true configuation is
veh.x'
%%% An estimation through the reported odometry after one time step is
%%% given by:
veh.f([0 0 0], odo)

%%% To simulate a scenario over a long time period 
veh.add_driver( RandomPath(10) )
veh.run()

%%% EKF
veh.Fx( [0,0,0.1], [0.5,0] )
veh.Fv( [0,0,0.1], [0.5,0] )
%%%% To simulate the vehicle and the EKF, we define the covariance matrix
%%%% as follows:
P0 = diag([0.005, 0.005, 0.001].^2);
%%%% and we pass this to the constructor for an EKF object;
ekf = EKF(veh, V, P0);
ekf.run(1000);

figure(1)
veh.plot_xy('k')
hold on
ekf.plot_xy('c')
ekf.plot_ellipse('g')

figure(2)
ekf.plot_P()

%%%% Localization  with a map
map = LandmarkMap(20,10)
%%%% A sensor covariance matrix 
sigmar = 0.02;        % distance traveled (m)
sigmab = 0.5*pi/180;  % change in heading (rad)
W = diag([sigmar^2, sigmab^2]);
%%%% Sensor modeling that accounts for vehicle and map properties
sensor = RangeBearingSensor(veh, map, 'covar', W)
%%%% Range and bearing to a randomly selected visible landmark along with
%%%% its identity
[z,i] = sensor.reading();
%%%% Now let's build an estimator based on odometry and observation of map
%%%% features
map = LandmarkMap(20);
veh = Bicycle('covar',V);
veh.add_driver( RandomPath(map.dim) );
sensor = RangeBearingSensor(veh, map, 'covar', W, 'angle',...
    [-pi/2 pi/2], 'range', 4, 'animate');
ekf = EKF(veh, V, P0, sensor, W, map);
ekf.run(1000)

map.plot()
veh.plot_xy('k')
ekf.plot_xy('--r')
ekf.plot_ellipse('g')