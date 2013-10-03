clc; clear all; close all;
rand('seed', 42);
f = funct;

nPower = 6;
n = 2^nPower; 


% what level to approx to?
howFar = 4;

% making the signal
x = zeros(n,n); x(n/2+1:n, n/2+1:n)=10; x(5, 4)=10;
x = imread('../tumblr.gif');
x = mean(x, 3);
[n j] = size(x);

% making sampleAt
sampleAt = zeros(n,n);
sampleAt([1, n/2+1, n^2/2+1, n^2/2+1+n/2]) = 1;


threshold = 20;

for m=1:howFar
    display(m)
    w        = f.approxScaleAndReshape(x, sampleAt, m);
    sampleAt = f.sampleInDetail(w, sampleAt, threshold, m);
end

w = f.approxScaleAndReshape(x, sampleAt, m-1);

%% exact
%wE = f.approxWavelet(x, ones(n,n), nPower);
%wE = reshape(wE, n, n);

h = f.haarMatrix(n);
time = h' * w * h;
%timeE = h' * wE * h;

f.S2imshow(time, 'approx');
%f.S2imshow(timeE, 'exact');
f.S2imshow(sampleAt, 'sampleAt');
%%close all;

% 2
p = 1/450;
phi = 0.5;
m = phi * (501 + 1/p) + 167.5
