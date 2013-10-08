function f = FoneD
    f.haarMatrix            = @haarMatrix;
    f.haarInd1D             = @haarInd1D;
    f.findNonZero           = @findNonZero;
    f.approxWavelet1D       = @approxWavelet1D;
    f.scaleWavelet          = @scaleWavelet;
    f.approxWaveletAndScale = @approxWaveletAndScale;
end

function h=haarMatrix(n)
    % returns a matrix as in 
    % w = h x
    %
    % assumes a column w and column x

    level = log2(n);

    % init'ing
    h = [1];
    nc = 1/sqrt(2);
    lp = [1 1];
    hp = [1 -1];

    for i=1:level
        e = eye(size(h));
        h = nc * [kron(h, lp); kron(e, hp)];
    end

    % return...
    h = h;
end

function j=haarInd1D(i, n)
    % HAARIND1D
    % i -- what wavelet term are we interested in?
    % n -- the size of the matrix
    h = haarMatrix(n);
    j = find(h(i,:) ~= 0);

    % return...
    j = j;
end

function i=findNonZero(w, threshold)
    % FINDNONZERO
    % sees where we're above some threshold
    i = find(abs(w) >= threshold);
    % return...
    i = i;
end

function w=approxWavelet1D(x, sampleAt, m)
    % approx wavelet
    [n junk] = size(x);
    h = haarMatrix(n);

    % delete where we don't sample
    toDelete = find(sampleAt == 0);
    h(:, toDelete) = [];

    % delete where we're not interested in
    i = 1:n;
    toDelete = find(i > 2^m);
    h(toDelete, :) = [];

    display(h)
    w = h * x(~~sampleAt);
    display(w)
    % return...
    z = zeros(n, 1);
    lenw = length(w);
    z(1:lenw) = w;
    w = z;
end

function w=scaleWavelet(w, sampleAt)
    % see how many samples are in that region. put that sample as (for example)
    % 16x more important -- kind of image inpainting.
    [n j] = size(w);

    % the indices we need to scale
    i = find(w ~= 0);

    for j=1:length(i),
        k      = haarInd1D(i(j), n);
        mm     = sum(sampleAt(k));
        n2     = length(k);
        factor = n2 / mm;
        w(j)   = w(j) * factor;

        display('--------------')
        display(i(j))
        display(n2)
        display(mm)
        display(factor)
        
    end

    % return...
    w = w;
end

function w=approxWaveletAndScale(x, sampleAt, m)
    w = approxWavelet1D(x, sampleAt, m);
    w = scaleWavelet(w, sampleAt);

end
