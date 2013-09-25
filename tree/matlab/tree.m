% function funs = makefuns
%   funs.fun1 = @fun1;
% end

% returns a matrix as in 
% w = h x
%
% assumes a column w and column x
clc; clear all; close all;
f = funct;

n = 8; x = reshape(1:n*n, n,n);
sampleAt = rand(n,n);
sampleAt = round(sampleAt);
m = 2;

w = f.approxWavelet(x, sampleAt, m);
wE = f.approxWavelet(x, ones(n,n), log2(n));

% now, scale wavelet





% we can...
%   approx the wavelet
%   
w = reshape(w, 2^m, 2^m);
wE = reshape(wE, n, n);
f.S2imshow(w, 'approx');
f.S2imshow(wE, 'exact');
