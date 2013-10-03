clc; clear all; close all;
rand('seed', 42);
f = funct;

nPower = 6;
n = 2^nPower; 



% making the signal
x = zeros(n,n); x(n/2+1:n, n/2+1:n)=10; x(5, 4)=10;
x = imread('../tumblr.gif');
x = mean(x, 3);
[n j] = size(x);


% making sampleAt
sampleAt = zeros(n,n);
sampleAt([1, n/2+1, n^2/2+1, n^2/2+1+n/2]) = 1;


% what level to approx to?
howFar = 4;

% our threshold -- everything below this is set to 0
threshold = 40;

for m=1:howFar,
    w        = f.approxScaleAndReshape(x, sampleAt, m);
    sampleAt = f.sampleInDetail(w, sampleAt, threshold, m);
end

w = f.approxScaleAndReshape(x, sampleAt, m);

h = f.haarMatrix(n);
wE = h * x * h';
time = h' * w * h;

%f.S2imshow(wE, 'exact')
f.S2imshow(w, 'approx w')
f.S2imshow(wE, 'exact w')
f.S2imshow(sampleAt, 'sampled')
f.S2imshow(time, 'time w')
f.S2imshow(x, 'time exact')

