clc; clear all; close all;
f = F_oned_v2;
rand('seed', 42);


nPower = 8;
n = 2^nPower; 

% making the signal
t = linspace(0, 1, n);
a = 1/10;
x = 1/(a*sqrt(pi)) * exp(-(t-0.3 ).^2 / a^2);
a = 1/20;
x = x + 1/(a*sqrt(pi)) * exp(-(t-0.7 ).^2 / a^2);


% making sampleAt
sampleAt = zeros(1, n);
sampleAt([1, n/4+1, n/2+1, 3*n/4+1]) = 1;
j = randperm(n);
sampleAt(j(1:10)) = 1;


x = x';
sampleAt = sampleAt';



interestedIn = [];
interestedIn = [interestedIn 1 2 3 4];

A = f.approxWavelet(x, sampleAt, interestedIn);

h = f.haarMatrix(n);

X = h' * A;


%plot(t, x);
%hold on;
%plot(t(1:10), w(1:10), 'g');
hold on;
plot(t(1:10), A(1:10), 'r');

%f.S2imshow(w, 'original wavelet');
