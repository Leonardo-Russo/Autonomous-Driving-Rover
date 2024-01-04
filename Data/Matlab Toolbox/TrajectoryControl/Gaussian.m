clear all

%%% First Gaussian Distribution
mu = [10 30];
sigma1=1;
sigma2=0.5;
corr=0.6;
Sigma = [sigma1^2 sigma1* sigma2* corr; sigma1* sigma2* corr sigma2^2];
x1 = 0:0.2:20;
x2 = 20:0.2:40;
[X1,X2] = meshgrid(x1,x2);
X = [X1(:) X2(:)];
y = mvnpdf(X,mu,Sigma);
y = reshape(y,length(x2),length(x1));
figure(1)
surf(x1,x2,y)
caxis([min(y(:))-0.5*range(y(:)),max(y(:))])
xlim([0 20])
ylim([20 40])
%axis([0 20 20 40 0 0.4])
xlabel('x')
ylabel('y')
zlabel('Probability Density')

%%% Second Gaussian Distribution
mu = [10 30];
sigma1=2;
sigma2=3;
corr=0.1;
Sigma = [sigma1^2 sigma1* sigma2* corr; sigma1* sigma2* corr sigma2^2];
x1 = 0:0.2:20;
x2 = 20:0.2:40;
[X1,X2] = meshgrid(x1,x2);
X = [X1(:) X2(:)];
y = mvnpdf(X,mu,Sigma);
y = reshape(y,length(x2),length(x1));
figure(2)
surf(x1,x2,y)
caxis([min(y(:))-0.5*range(y(:)),max(y(:))])
xlim([0 20])
ylim([20 40])
%axis([0 20 20 40 0 0.4])
xlabel('x')
ylabel('y')
zlabel('Probability Density')

%%% Multiple Gaussian Distributions
mu = [10 30];
sigma1=0.7;
sigma2=1.5;
corr=0.1;
Sigma = [sigma1^2 sigma1* sigma2* corr; sigma1* sigma2* corr sigma2^2];
x1 = 0:0.2:20;
x2 = 20:0.2:40;
[X1,X2] = meshgrid(x1,x2);
X = [X1(:) X2(:)];
y = mvnpdf(X,mu,Sigma);
y = reshape(y,length(x2),length(x1));
mu = [15 27];
sigma1=0.6;
sigma2=1.2;
corr=0.5;
Sigma = [sigma1^2 sigma1* sigma2* corr; sigma1* sigma2* corr sigma2^2];
X = [X1(:) X2(:)];
y1 = mvnpdf(X,mu,Sigma);
y1 = reshape(y1,length(x2),length(x1));
mu = [5 33];
sigma1=1.2;
sigma2=0.9;
corr=0.3;
Sigma = [sigma1^2 sigma1* sigma2* corr; sigma1* sigma2* corr sigma2^2];
X = [X1(:) X2(:)];
y2 = mvnpdf(X,mu,Sigma);
y2 = reshape(y2,length(x2),length(x1));
y3=y2+y1+y;
figure(3)
surf(x1,x2,y3)
%caxis([min(y2(:))-0.5*range(y2(:)),max(y2(:))])
xlim([0 20])
ylim([20 40])
%axis([0 20 20 40 0 0.4])
xlabel('x')
ylabel('y')
zlabel('Probability Density')
